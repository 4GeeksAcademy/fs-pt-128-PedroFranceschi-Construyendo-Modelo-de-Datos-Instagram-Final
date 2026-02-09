from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

follower_table = db.Table(
    "follower",
    db.Model.metadata,
    # columnnas de tabla
    Column("user_from_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("user_to_id", Integer, ForeignKey("user.id"), primary_key=True)
) 

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # POR QUE/ DE DONDE VIENE ESTE BLOQUE (REVISE LA DOC Y SOLO ME MUESTRA children: Mapped[List["Child"]] = relationship())

    # relacion back_populates a comments:
    comments: Mapped[list["Comments"]] = relationship(back_populates="user")# aqui tenia "comments"

    follower: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin= id == follower_table.c.user_to_id,
        secondaryjoin= id == follower_table.c.user_from_id, 
        back_populates="following"
    )

    following: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_table,
        primaryjoin= id == follower_table.c.user_from_id,
        secondaryjoin= id ==  follower_table.c.user_to_id,
        back_populates="follower"
    )
    
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
    published_post: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    # SEGUN DOCUMENTACION parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    # now we need the relationship
    user: Mapped["User"] = relationship(back_populates="posts")
    # EL BLOQUE Y ESTA LINEA ME LA DA CHATGPT, en el video javier hace una tabla auxiliar... siempre hay un vinculo bidireccional?

    # "recibimos" la relationship -> linea66
    comments: Mapped[list["Comments"]] = relationship(back_populates="post")

    # "recibimos" la relationship -> linea83
# children: Mapped[List["Child"]] = relationship(back_populates="parent")
    media: Mapped[list["Media"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "publishedPost": self.published_post
        }

class Comments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200), nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    # esto mapped_column(ForeignKey("post.id") = a
    # mapped_column(ForeignKey("tabla_de_la_que_viene_como_primary.id"),

    # create relationship User 1-* comments
    user: Mapped["User"] = relationship(back_populates="comments")
    # por que back_populates="comments" en minuscula y en comillas y no back_populates=Comments -> estamos apuntando a lo que yo cree.

    # create relationship post*-1 User 
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comments": self.comment_text,
            "userId": self.author_id,
            "postId": self.post_id
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[enumerate] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(String(150), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    # relationship 1 post to many media
    post: Mapped["Post"]= relationship(back_populates="media")
 # parent: Mapped["Parent"] = relationship(back_populates="children")

    def serialize(self):
        return {
            "id": self.id,
            "mediaType": self.media_type,
            "url": self.url,
            "postId": self.post_id
        }