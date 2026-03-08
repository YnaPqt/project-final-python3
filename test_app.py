import pytest
from peewee import IntegrityError

from models import db, Studio, Anime, Character, Genre, AnimeGenre


# =====================================================
# FIXTURE : BASE DE DONNÉES TEMPORAIRE
# =====================================================

@pytest.fixture(scope="function")
def test_db():
    """
    Initialise une base SQLite en mémoire avant chaque test
    et la supprime après le test.
    """

    db.init(":memory:")
    db.connect()

    db.create_tables([
        Studio,
        Anime,
        Character,
        Genre,
        AnimeGenre
    ])

    yield

    db.drop_tables([
        Studio,
        Anime,
        Character,
        Genre,
        AnimeGenre
    ])

    db.close()


# =====================================================
# TEST : CREATION STUDIO
# =====================================================

def test_create_studio(test_db):

    studio = Studio.create(studio_name="MAPPA")

    assert studio.id is not None
    assert studio.studio_name == "MAPPA"


# =====================================================
# TEST : CREATION ANIME
# =====================================================

def test_create_anime(test_db):

    studio = Studio.create(studio_name="Bones")

    anime = Anime.create(
        title="Fullmetal Alchemist",
        studio=studio,
        release_year=2003,
        description="Alchemy adventure"
    )

    assert anime.title == "Fullmetal Alchemist"
    assert anime.studio.studio_name == "Bones"


# =====================================================
# TEST : AJOUT PERSONNAGES
# =====================================================

def test_add_characters(test_db):

    studio = Studio.create(studio_name="Pierrot")

    anime = Anime.create(
        title="Naruto",
        studio=studio,
        release_year=2002,
        description="Ninja story"
    )

    Character.create(character_name="Naruto", anime=anime)
    Character.create(character_name="Sasuke", anime=anime)

    characters = Character.select().where(Character.anime == anime)

    assert characters.count() == 2


# =====================================================
# TEST : AJOUT GENRE
# =====================================================

def test_add_genre(test_db):

    studio = Studio.create(studio_name="Madhouse")

    anime = Anime.create(
        title="Death Note",
        studio=studio,
        release_year=2006,
        description="Psychological thriller"
    )

    genre = Genre.create(genre_name="Thriller")

    AnimeGenre.create(anime=anime, genre=genre)

    relations = AnimeGenre.select().where(AnimeGenre.anime == anime)

    assert relations.count() == 1


# =====================================================
# TEST : CONTRAINTE UNIQUE SUR LE TITRE
# =====================================================

def test_unique_anime_title(test_db):

    studio = Studio.create(studio_name="Trigger")

    Anime.create(
        title="Kill la Kill",
        studio=studio,
        release_year=2013,
        description="Action"
    )

    with pytest.raises(IntegrityError):

        Anime.create(
            title="Kill la Kill",
            studio=studio,
            release_year=2013,
            description="Duplicate"
        )


# =====================================================
# TEST : SUPPRESSION CASCADE
# =====================================================

def test_delete_anime_cascade(test_db):

    studio = Studio.create(studio_name="Toei")

    anime = Anime.create(
        title="One Piece",
        studio=studio,
        release_year=1999,
        description="Pirate adventure"
    )

    Character.create(character_name="Luffy", anime=anime)

    genre = Genre.create(genre_name="Adventure")

    AnimeGenre.create(anime=anime, genre=genre)

    anime.delete_instance(recursive=True)

    assert Anime.select().count() == 0
    assert Character.select().count() == 0
    assert AnimeGenre.select().count() == 0