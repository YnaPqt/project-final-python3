from models import *
import peewee
import pandas as pd
from peewee import IntegrityError


# CREATE

def create_anime():
    print("\n --- CREATE ANIME---")

    title = input("Title: ")
    studio_name = input("Studio: ")
    release_year = input("Release Year: ")
    description = input("Description: ")
    characters_input = input("Characters ( comma separated): ")
    genres_input = input("Genres (comma separated): ")

    try:
        release_year = int(release_year)
    except ValueError:
        print("Invalide year.")
        return
    
    with db.atomic():
        try:
            studio, _ = Studio.get_or_create(studio_name=studio_name)

            anime = Anime.create(
                title = title,
                studio = studio,
                release_year=release_year,
                description=description
            )

            characters = [c.strip() for c in characters_input.split(",") if c.strip()]
            for char in characters:
                Character.create(character_name = char, anime=anime)
            
            genres = [g.strip() for g in genres_input.split(",")  if g.strip()]
            for genre_name in genres:
                genre, _ = Genre.get_or_create(genre_name=genre_name)
                AnimeGenre.create(anime=anime, genre=genre)
            
            print("Anime created")

        except IntegrityError:
            print("Anime already exists.")
        

# Read Data
def list_anime():
    data = []
    
    for anime in Anime.select():
        characters = ",".join([c.character_name for c in anime.characters])
        genres = ",".join([ag.genre.genre_name for ag in anime.anime_genres])

        data.append({
            "ID": anime.id,
            "Title": anime.title,
            "Studio": anime.studio.studio_name,
            "Release year": anime.release_year,
            "Description": anime.description,
            "Genres": genres
        })
    
    if not data:
        print("No anime found.")
        return
    
    df = pd.DataFrame(data)
    print(df)

# UPDATE DATABASE
def update_anime():
    list_anime()

    try:
        anime_id = int(input("Anime ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return
    
    anime = Anime.get_or_none(Anime.id == anime_id)
    if not anime:
        print("Anime not found.")
        return
    
    print("\n Leave blank, if you don't want to modify.")

    new_title = input("New title: ")
    new_year = input("New release year: ")
    new_description = input("New description: ")
    new_characters = input("New characters (comma separated): ")
    new_genres = input("New genres (comma separated): ")

    try:
        with db.atomic():

            # Update main fields
            if new_title:
                anime.title = new_title
            
            if new_year:
                try:
                    anime.release_year = int(new_year)
                except ValueError:
                    print("Invalide year.")
                    return
                
            if new_description:
                anime.description = new_description

            anime.save()
    
            # Replace characters if needed

            if new_characters:
                Character.delete().where(Character.anime == anime).execute()

                characters = [c.strip() for c in new_characters.split(",") if c.strip()]
                for char in characters:
                    Character.create(character_name = char, anime=anime)

            # Replace genres if needed
            if new_genres:
                AnimeGenre.delete().where(AnimeGenre.anime == anime).execute()

                genres = [g.strip() for g in new_genres.split(",") if g.strip()]
                for genre_name in genres:
                    genre, _ = Genre.get_or_create(genre_name = genre_name)
                    AnimeGenre.create(anime=anime, genre=genre)
        
        print("Anime updated successfully.")

    except IntegrityError:
        print("Update failed (possible duplicate).")


# DELETE DATA
def delete_anime():
    list_anime()

    try:
        anime_id = int(input("Anime ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    
    anime = Anime.get_or_none(Anime.id == anime_id)
    if not anime:
        print("Anime not found.")
        return
    
    confirm = input("Are you sure to delete (Y/N)?: ")
    if confirm.lower()=="y":
        anime.delete_instance(recursive = True)
        print("Anime deleted")