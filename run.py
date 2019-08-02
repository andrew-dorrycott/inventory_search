# Standard imports
import json
import logging
import logging.config

# Third party imports
import flask
import sqlalchemy
import yaml

# Application imports
from models.products import Product


LOGGER = logging.getLogger(__name__)


def load_config():
    with open("config.yaml", "r") as _file:
        return yaml.load(_file, Loader=yaml.FullLoader)


def load_db(config):
    engine = sqlalchemy.create_engine(
        config["postgresql"]["sqlalchemy_uri"].format(**config["postgresql"])
    )
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    return Session()


def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)

    config = load_config()
    logging.config.dictConfig(config["logging"])
    LOGGER.debug("Logging config loaded")

    app.config.from_mapping(config)
    session = load_db(config)

    # Controllers (will be moved later)
    @app.route("/")
    def default():
        return "Default entry, don't mind me"

    @app.route("/test/")
    @app.route("/test/<name>")
    def test(name=None):
        return flask.render_template("test.html", name=flask.escape(name))

    @app.route("/search/<token>")
    @app.route("/search/<field>/<token>")
    def search(token, field=None):
        # Search DB with the provided field and token
        query = session.query(Product)

        filters = None
        if field:
            column = getattr(Product, field)
            LOGGER.debug(1, column)
            if isinstance(column.type, (sqlalchemy.Float, sqlalchemy.Integer)):
                filters = sqlalchemy.and_(getattr(Product, field) == token)
            else:
                filters = sqlalchemy.and_(
                    getattr(Product, field).ilike("%{}%".format(token))
                )
        else:
            for _, column in Product.__dict__.items():
                if (
                    isinstance(
                        column, sqlalchemy.orm.attributes.InstrumentedAttribute
                    )
                    is False
                ):
                    continue  # Not a column attribute

                # This one is doing all ANDs
                if isinstance(
                    column.type, (sqlalchemy.String, sqlalchemy.VARCHAR)
                ):
                    new_filter = sqlalchemy.or_(
                        column.ilike("%{}%".format(token))
                    )
                    if filters is None:
                        filters = new_filter
                    else:
                        filters = filters | new_filter

                elif isinstance(
                    column.type, (sqlalchemy.Float, sqlalchemy.Integer)
                ):
                    if token.isdigit() is False:
                        continue  # Data won't work for this column

                    new_filter = sqlalchemy.or_(column == token)
                    if filters is None:
                        filters = new_filter
                    else:
                        filters = filters | new_filter

        try:
            results = query.filter(filters).all()

            return json.dumps(
                {
                    "results": [item.to_dict() for item in results],
                    "count": len(results),
                }
            )
        except sqlalchemy.exc.DataError:
            session.rollback()
            return json.dumps(
                {"error": "Invalid input for column `{}`".format(field)}
            )
        except Exception as error:
            session.rollback()
            LOGGER.exception(error)
            return json.dumps({"error": "Catastrophic error happened"})

    @app.route("/query")
    def query():
        # Grab all data from post
        results = [{"id": 123, "description": "hard coded test"}]
        return json.dumps({"results": results, "count": len(results)})

    return app


if __name__ == "__main__":
    LOGGER.info("Application starting")
    app = create_app()
    app.run()
