from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
 
db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )#POR QUE/ DE DONDE VIENE ESTE BLOQUE (REVISE LA DOC Y SOLO ME MUESTRA children: Mapped[List["Child"]] = relationship())

    # password: Mapped[str] = mapped_column(nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "userName": self.user_name,
            "name": self.name,
            "lastName": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    #SEGUN DOCUMENTACION parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
    #EL BLOQUE Y ESTA LINEA ME LA DA CHATGPT


    def serialize(self):
        return {
            "id": self.id,
            "userId": self.user_id,
        }