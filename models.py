from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
# from passlib.hash import bcrypt

from database import Base


# SQLAlchemy Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    date_created = Column(DateTime, default=datetime.utcnow())
    is_active = Column(Boolean, default=True)

    pets = relationship("Pet", back_populates="owner")

class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(String)
    adopt_date = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow())
    date_last_updated = Column(DateTime, default=datetime.utcnow())

    owner = relationship("User", back_populates="pets")
