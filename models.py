import peewee

db = peewee.SqliteDatabase("anime.db")


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Studio(BaseModel):
    studio_name = peewee.CharField(unique=True, null=False)

    def __str__(self):
        return f"Studio: {self.studio_name}"


class Anime(BaseModel):
    title = peewee.CharField(unique=True, null=False)
    studio = peewee.ForeignKeyField(Studio, backref='animes', on_delete="CASCADE")
    release_year = peewee.IntegerField(null=False)
    description = peewee.TextField(null=True)

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Character(BaseModel):
    character_name = peewee.CharField(null=False)
    anime = peewee.ForeignKeyField(Anime, backref='characters', on_delete="CASCADE")


class Genre(BaseModel):
    genre_name = peewee.CharField(unique=True, null=False)

    def __str__(self):
        return self.genre_name


class AnimeGenre(BaseModel):
    anime = peewee.ForeignKeyField(Anime, backref='anime_genres',on_delete="CASCADE")
    genre = peewee.ForeignKeyField(Genre, backref='genre_animes',on_delete="CASCADE")

    class Meta:
        primary_key = peewee.CompositeKey('anime', 'genre')



def initialize_database():
    db.connect()
    db.create_tables(
        [Studio, Anime, Character,Genre, AnimeGenre],
        safe=True
    )