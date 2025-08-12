from sqlalchemy import Column, Boolean, Integer, String, Date, LargeBinary, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    states = relationship("State", back_populates="country")

class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship("Country", back_populates="states")
    cities = relationship("City", back_populates="state")

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship("State", back_populates="cities")


class User(Base):
    __tablename__='userData'

    rollNum = Column(Integer, primary_key=True)
    fullname = Column(String(50))
    fatherName = Column(String(50))
    dob = Column(Date)
    mobNum = Column(String(10), unique=True)
    emailID= Column(String(50), unique=True)
    password= Column(String(18))
    gender = Column(String(10))
    dept = Column(String(100))  # store as comma-separated string
    course = Column(String(50))
    content= Column(String(255))  # store file path instead of binary
    country=Column(Integer)
    state=Column(Integer)
    city=Column(Integer)
    address=Column(String(500))

