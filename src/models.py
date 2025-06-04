from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_name: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[str] = mapped_column(String(120), nullable=False)
    galaxy: Mapped[str] = mapped_column(String(120), nullable=False)
    imagen_url: Mapped[str] = mapped_column(String(200))

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "population": self.population,
            "galaxy": self.galaxy,
            "imagen_url": self.imagen_url
        }


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_name: Mapped[str] = mapped_column(String(120), nullable=False)
    character_last_name: Mapped[str] = mapped_column(
        String(120), nullable=False)
    age: Mapped[str] = mapped_column(String(60), nullable=False)
    planet_born: Mapped[str] = mapped_column(String(120), nullable=False)
    imagen_url: Mapped[str] = mapped_column(String(200))

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "character_last_name": self.character_last_name,
            "age": self.age,
            "planet_born": self.planet_born,
            "imagen_url": self.imagen_url
        }


class Vehicles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_name: Mapped[str] = mapped_column(String(120), nullable=False)
    surface: Mapped[str] = mapped_column(String(120), nullable=False)
    size: Mapped[str] = mapped_column(String(120), nullable=False)
    imagen_url: Mapped[str] = mapped_column(String(200))

    def serialize(self):
        return {
            "id": self.id,
            "vehicle_name": self.vehicle_name,
            "surface": self.surface,
            "size": self.size,
            "imagen_url": self.imagen_url
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_from_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    character_from_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    vehicle_from_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites")
    planet: Mapped["Planets"] = relationship("Planets", foreign_keys=[planet_from_id])
    character: Mapped["Characters"] = relationship("Characters", foreign_keys=[character_from_id])
    vehicle: Mapped["Vehicles"] = relationship("Vehicles", foreign_keys=[vehicle_from_id])

    def serialize(self):
        return{
            "id": self.id,
            "planet": self.planet.serialize() if self.planet else None,
            "character": self.character.serialize() if self.character else None,
            "vehicle": self.vehicle.serialize() if self.vehicle else None
        }

