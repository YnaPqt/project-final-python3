import pytest
from peewee import IntegrityError
from models import (
    db,
    Studio,
    Anime,
    Character,
    Episode,
    Genre,
    AnimeGenre,
    VoiceActor,
)


# ==========================
# FIXTURE : Base temporaire
# ==========================

@pytest.fixture(scope="function")
def test_db():
    """
    Initialise une base SQLite en mémoire
    avant chaque test.
    """
    db.init(":memory:")
    db.connect()
    db.create_tables([
        Studio, Anime, Character,
        Episode, Genre, AnimeGenre, VoiceActor
    ])

    yield

    db.drop_tables([
        Studio, Anime, Character,
        Episode, Genre, AnimeGenre, VoiceActor
    ])
    db.close()


# ==========================
# TESTS STUDIO
# ==========================

def test_create_studio(test_db):
    studio = Studio.create(studio_name="MAPPA")
    assert studio.id is not None
    assert studio.studio_name == "MAPPA"


def test_duplicate_studio(test_db):
    Studio.create(studio_name="MAPPA")

    with pytest.raises(IntegrityError):
        Studio.create(studio_name="MAPPA")


def test_update_studio(test_db):
    studio = Studio.create(studio_name="Bones")
    studio.studio_name = "Bones Studio"
    studio.save()

    updated = Studio.get_by_id(studio.id)
    assert updated.studio_name == "Bones Studio"


def test_delete_studio(test_db):
    studio = Studio.create(studio_name="Ufotable")
    studio_id = studio.id

    studio.delete_instance()

    deleted = Studio.get_or_none(Studio.id == studio_id)
    assert deleted is None


# ==========================
# TESTS ANIME
# ==========================

def test_create_anime(test_db):
    studio = Studio.create(studio_name="Toei")
    anime = Anime.create(
        title="One Piece",
        studio=studio,
        release_year=1999,
        description="Pirate adventure"
    )

    assert anime.title == "One Piece"
    assert anime.studio.id == studio.id


def test_anime_unique_title(test_db):
    studio = Studio.create(studio_name="Trigger")

    Anime.create(
        title="Kill la Kill",
        studio=studio,
        release_year=2013,
        description="Action anime"
    )

    with pytest.raises(IntegrityError):
        Anime.create(
            title="Kill la Kill",
            studio=studio,
            release_year=2013,
            description="Duplicate"
        )


# ==========================
# TESTS RELATIONS
# ==========================

def test_character_creation(test_db):
    studio = Studio.create(studio_name="A-1 Pictures")
    anime = Anime.create(
        title="Sword Art Online",
        studio=studio,
        release_year=2012,
        description="VR MMORPG"
    )

    character = Character.create(
        character_name="Kirito",
        anime=anime
    )

    assert character.anime.title == "Sword Art Online"


def test_episode_creation(test_db):
    studio = Studio.create(studio_name="Madhouse")
    anime = Anime.create(
        title="Death Note",
        studio=studio,
        release_year=2006,
        description="Psychological thriller"
    )

    episode = Episode.create(
        episode_number=1,
        title="Rebirth",
        anime=anime,
        release_date="2006-10-03"
    )

    assert episode.episode_number == 1
    assert episode.anime.title == "Death Note"


def test_genre_relationship(test_db):
    studio = Studio.create(studio_name="MAPPA")
    anime = Anime.create(
        title="Jujutsu Kaisen",
        studio=studio,
        release_year=2020,
        description="Curses and sorcerers"
    )

    genre = Genre.create(genre_name="Action")

    AnimeGenre.create(anime=anime, genre=genre)

    assert anime.anime_genres.count() == 1
    assert genre.genre_animes.count() == 1


def test_voice_actor(test_db):
    studio = Studio.create(studio_name="Pierrot")
    anime = Anime.create(
        title="Naruto",
        studio=studio,
        release_year=2002,
        description="Ninja story"
    )

    character = Character.create(
        character_name="Naruto Uzumaki",
        anime=anime
    )

    actor = VoiceActor.create(
        actor_name="Junko Takeuchi",
        character=character
    )

    assert actor.character.character_name == "Naruto Uzumaki"