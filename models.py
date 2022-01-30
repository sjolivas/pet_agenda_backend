from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt

from database import Base


# SQLAlchemy Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow())
    is_active = Column(Boolean, default=True)

    pets = relationship("Pet", back_populates="owner")

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    picture = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    adopt_date = Column(Date)
    age = Column(Integer)
    weight = Column(Integer)
    breed = Column(String)
    color = Column(String)
    other_characteristics = Column(String, default="")
    fav_person = Column(String, default="")
    fav_activity = Column(String, default="")
    fav_treat = Column(String, default="")
    fav_toy = Column(String, default="")
    date_created = Column(DateTime, default=datetime.utcnow())
    date_last_updated = Column(DateTime, default=datetime.utcnow())

    owner = relationship("User", back_populates="pets")
