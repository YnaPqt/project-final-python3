import tkinter as tk
from tkinter import ttk, messagebox

from models import *
from peewee import IntegrityError


# ============================
# WINDOW
# ============================

root = tk.Tk()
root.title("Anime Database Manager")
root.geometry("1050x600")
root.configure(padx=10, pady=10)


# ============================
# MAIN FRAME
# ============================

input_frame = ttk.LabelFrame(root, text="Anime Information")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

table_frame = ttk.LabelFrame(root, text="Anime List")
table_frame.grid(row=1, column=0, padx=10, pady=10)


# ============================
# INPUT FIELDS
# ============================

labels = ["Title", "Studio", "Release Year", "Description", "Characters", "Genres"]
entries = {}

for i, label in enumerate(labels):

    ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)

    entry = ttk.Entry(input_frame, width=40)
    entry.grid(row=i, column=1, pady=5)

    entries[label] = entry


# ============================
# CLEAR INPUT FIELDS
# ============================

def clear_fields():

    for entry in entries.values():
        entry.delete(0, tk.END)


# ============================
# CREATE BUTTON
# prépare un nouvel enregistrement
# ============================

def create_anime_gui():
    clear_fields()


# ============================
# ADD ANIME
# ajoute l'anime dans la base
# ============================

def add_anime():

    title = entries["Title"].get()
    studio_name = entries["Studio"].get()
    year = entries["Release Year"].get()
    description = entries["Description"].get()
    characters = entries["Characters"].get()
    genres = entries["Genres"].get()

    try:
        year = int(year)
    except:
        messagebox.showerror("Error", "Release year must be a number")
        return

    try:

        studio, _ = Studio.get_or_create(studio_name=studio_name)

        anime = Anime.create(
            title=title,
            studio=studio,
            release_year=year,
            description=description
        )

        char_list = [c.strip() for c in characters.split(",") if c.strip()]

        for c in char_list:
            Character.create(character_name=c, anime=anime)

        genre_list = [g.strip() for g in genres.split(",") if g.strip()]

        for g in genre_list:
            genre, _ = Genre.get_or_create(genre_name=g)
            AnimeGenre.create(anime=anime, genre=genre)

        messagebox.showinfo("Success", "Anime added successfully")

        refresh_table()
        clear_fields()

    except IntegrityError:
        messagebox.showerror("Error", "Anime already exists")


# ============================
# TABLE VIEW
# ============================

columns = ("ID", "Title", "Studio", "Year", "Description","Genre","Characters")

tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)

tree.column("ID", width=50)
tree.column("Title", width=150)
tree.column("Studio", width=100)
tree.column("Year", width=70)
tree.column("Description", width=250)
tree.column("Genre", width=150)
tree.column("Characters", width=150)

tree.grid(row=0, column=0)


# ============================
# REFRESH TABLE
# ============================

def refresh_table():

    # Supprime les lignes existantes
    for row in tree.get_children():
        tree.delete(row)

    # Parcourt tous les animes
    for anime in Anime.select():

        # Récupère les personnages liés
        characters = ", ".join([c.character_name for c in anime.characters])

        # Récupère les genres liés
        genres = ", ".join([ag.genre.genre_name for ag in anime.anime_genres])

        # Insère les données dans la table
        tree.insert("", "end", values=(
            anime.id,
            anime.title,
            anime.studio.studio_name,
            anime.release_year,
            anime.description,
            genres,
            characters
        ))
def fill_fields(event):

    selected = tree.selection()

    if not selected:
        return

    item = tree.item(selected[0])
    anime_id = item["values"][0]

    anime = Anime.get_by_id(anime_id)

    clear_fields()

    entries["Title"].insert(0, anime.title)
    entries["Studio"].insert(0, anime.studio.studio_name)
    entries["Release Year"].insert(0, anime.release_year)
    entries["Description"].insert(0, anime.description if anime.description else "")

    characters = ", ".join([c.character_name for c in anime.characters])
    entries["Characters"].insert(0, characters)

    genres = ", ".join([ag.genre.genre_name for ag in anime.anime_genres])
    entries["Genres"].insert(0, genres)

tree.bind("<<TreeviewSelect>>", fill_fields)   
# ============================
# DELETE
# ============================

def delete_anime():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select an anime first")
        return

    item = tree.item(selected[0])
    anime_id = item["values"][0]

    anime = Anime.get_by_id(anime_id)

    anime.delete_instance(recursive=True)

    refresh_table()

def update_anime():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select an anime first")
        return

    item = tree.item(selected[0])
    anime_id = item["values"][0]

    anime = Anime.get_by_id(anime_id)

    title = entries["Title"].get()
    studio_name = entries["Studio"].get()
    year = entries["Release Year"].get()
    description = entries["Description"].get()
    characters = entries["Characters"].get()
    genres = entries["Genres"].get()

    try:
        year = int(year)
    except:
        messagebox.showerror("Error", "Release year must be a number")
        return

    try:

        studio, _ = Studio.get_or_create(studio_name=studio_name)

        anime.title = title
        anime.studio = studio
        anime.release_year = year
        anime.description = description
        anime.save()

        # Replace characters
        Character.delete().where(Character.anime == anime).execute()

        char_list = [c.strip() for c in characters.split(",") if c.strip()]
        for c in char_list:
            Character.create(character_name=c, anime=anime)

        # Replace genres
        AnimeGenre.delete().where(AnimeGenre.anime == anime).execute()

        genre_list = [g.strip() for g in genres.split(",") if g.strip()]
        for g in genre_list:
            genre, _ = Genre.get_or_create(genre_name=g)
            AnimeGenre.create(anime=anime, genre=genre)

        messagebox.showinfo("Success", "Anime updated successfully")

        refresh_table()

    except IntegrityError:
        messagebox.showerror("Error", "Anime title already exists")


# ============================
# BUTTON FRAME
# ============================

button_frame = ttk.Frame(input_frame)
button_frame.grid(row=6, column=0, columnspan=2, pady=10)


ttk.Button(button_frame, text="Create Anime", command=create_anime_gui).grid(row=0, column=0, padx=5)

ttk.Button(button_frame, text="Add Anime", command=add_anime).grid(row=0, column=1, padx=5)

ttk.Button(button_frame, text="Update Anime", command=update_anime).grid(row=0, column=2, padx=5)

ttk.Button(button_frame, text="Delete Anime", command=delete_anime).grid(row=0, column=3, padx=5)

ttk.Button(button_frame, text="Refresh List", command=refresh_table).grid(row=0, column=4, padx=5)


# ============================
# INITIALIZE DATABASE
# ============================

initialize_database()
refresh_table()


# ============================
# START APP
# ============================

root.mainloop()