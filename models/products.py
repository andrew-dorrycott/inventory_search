# Third party imports
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, nullable=False
    )
    description = sqlalchemy.Column(sqlalchemy.String)
    lastsold = sqlalchemy.Column(sqlalchemy.Date)
    shelflife = sqlalchemy.Column(sqlalchemy.String)
    department = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Float)
    unit = sqlalchemy.Column(sqlalchemy.String)
    xfor = sqlalchemy.Column(sqlalchemy.Integer)
    cost = sqlalchemy.Column(sqlalchemy.Float)

    def __repr__(self):
        return "<Product(id='{id}', description='{description}')>".format(
            **self.__dict__
        )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {
            "ID": self.id,
            "Description": self.description,
            "lastSold": self.lastsold.strftime("%Y-%m-%d"),
            "ShelfLife": self.shelflife,
            "Department": self.department,
            "Price": self.price,
            "Unit": self.unit,
            "xFor": self.xfor,
            "Cost": self.cost,
        }
