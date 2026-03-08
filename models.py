import peewee

# Connexion à la base de données SQLite
db = peewee.SqliteDatabase("anime.db")

# =======================================================
# Modele de base : tous les modèles héritent de BaseModel
# pour la même connexion à la base de données.
# =======================================================
class BaseModel(peewee.Model):
    class Meta:
        database = db

# =======================================================
# Création class Studio
# =======================================================
class Studio(BaseModel):
    studio_name = peewee.CharField(unique=True, null=False)

    def __str__(self):
        return f"Studio: {self.studio_name}"

# =======================================================
# Création class Anime
# =======================================================
class Anime(BaseModel):
    title = peewee.CharField(unique=True, null=False)
    
    # Relation vers le studio avec une clé étrangère
    studio = peewee.ForeignKeyField(Studio, backref='animes', on_delete="CASCADE")
    
    # Année de sortie
    release_year = peewee.IntegerField(null=False)
    
    # Description faculative
    description = peewee.TextField(null=True)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

# =======================================================
# Création class Character
# Contient les personnages
# =======================================================
class Character(BaseModel):
    character_name = peewee.CharField(null=False)
    
    # Relation vers Anime
    anime = peewee.ForeignKeyField(Anime, backref='characters', on_delete="CASCADE")

# =======================================================
# Création class Genre
# Contient les genres d'anime (Action, Fantasy..)
# =======================================================
class Genre(BaseModel):
    genre_name = peewee.CharField(unique=True, null=False)

    def __str__(self):
        return self.genre_name


# =======================================================
# Création class Animegenre
# Permet d'associer plusieurs genres à un animé
# =======================================================
class AnimeGenre(BaseModel):
    anime = peewee.ForeignKeyField(Anime, backref='anime_genres',on_delete="CASCADE")
    genre = peewee.ForeignKeyField(Genre, backref='genre_animes',on_delete="CASCADE")

    class Meta:
        # clé primaire composée pour éviter les doublons anime/genre
        primary_key = peewee.CompositeKey('anime', 'genre')


# ========================================================
# Initialisation de la base de données
# Créer les tables si elles n'existent pas
# ========================================================
def initialize_database():
    db.connect()
    db.create_tables(
        [Studio, Anime, Character,Genre, AnimeGenre],
        safe=True
    )