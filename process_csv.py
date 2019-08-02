# Standard imports
import csv
import sys

# Third party imports
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import yaml


def load_config():
    with open("config.yaml", "r") as _file:
        return yaml.load(_file, Loader=yaml.FullLoader)


def load_db(config):
    engine = sqlalchemy.create_engine(
        config["postgresql"]["sqlalchemy_uri"].format(**config["postgresql"])
    )
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "Missing CSV file input, example `python3 {} example.csv`".format(
                sys.argv[0]
            )
        )
        sys.exit()

    session = load_db(load_config())

    with open(sys.argv[1], "r") as _file:
        reader = csv.DictReader(_file)
        for row in reader:
            data = {
                key.lower().strip(): value.replace("$", "")
                for key, value in row.items()
            }
            # sqlalchemy insert data
