from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fecha_suscripcion: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id: Mapped[int] = mapped_column (primary_key=True)
    planet_name: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[str] = mapped_column(String(120), nullable=False)
    galaxy: Mapped[str] = mapped_column(String(120), nullable=False)


    def serialize(self):
        return{
            "id": self.id,
            "planet_name": self.planet_name,
            "population": self.population,
            "galaxy": self.galaxy
        }


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_name: Mapped[str] = mapped_column(String(120), nullable=False)
    character_last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[str] = mapped_column(String(60), nullable=False)
    planet_born: Mapped[str] = mapped_column(String(120), nullable=False)




class Vehicles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_name: Mapped[str] = mapped_column(String(120), nullable=False)
    surface: Mapped[str] = mapped_column(String(120), nullable=False)
    size: Mapped[str] = mapped_column(String(120), nullable=False)




class Favorites(db.Model):
    planet_from_id: Mapped
    character_from_id: Mapped
    vehicle_from_id: Mapped