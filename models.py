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
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
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
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    owner = relationship("User", back_populates="pets")

class Diet(Base):
    __tablename__ = "diets"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("pets.id"))
    food_type = Column(String)
    amount_per_day = Column(Integer)
    feeding_frequency = Column(Integer)
    treats = Column(String)
    allergies = Column(String, default=None)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    owner = relationship("Pet", back_populates="diets")

class MedicalInfo(Base):
    __tablename__ = "medicalinfo"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("pets.id"))
    microchip_number = Column(String, default="")
    vaccinations = Column(String)
    last_vet_apt = Column(Date)
    past_injuries = Column(String)
    medications = Column(String)
    allergies = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    owner = relationship("Pet", back_populates="medicalinfo")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("pets.id"))
    title = Column(String)
    start_date_time_utc = Column(DateTime, default=datetime.utcnow())
    end_date_time_utc = Column(DateTime, default=datetime.utcnow())
    is_all_day = Column(Boolean)
    is_reocurring = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    owner = relationship("User", back_populates="pets")
