# Import de la fonction qui initialise la base de données
from models import initialize_database

# Import des fonctions CRUD définies dans le fichier anime_modules.py
from anime_modules import(
    create_anime,
    list_anime,
    update_anime,
    delete_anime
)

# =============================================
# Menu Principal de l'application
# La fonction affiche un menu en CLI et permet de choisir une opération
def main_menu():

    # Boucle while pour maintenir l'application active
    # et de choisir une opération
    while True:
        print("\n === ANIME DATABASE ===")
        print("1. Create Anime")
        print("2. View list Anime")
        print("3. Update Anime")
        print("4. Delete Anime")
        print("5. Exit")

        # Choisir une option
        choice = input("Choice: ")

        # Choix d"opération qui fait appel la fonction correspondante
        if choice == "1":
            create_anime()
        elif choice =="2":
            list_anime()
        elif choice == "3":
            update_anime()
        elif choice == "4":
            delete_anime()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__== "__main__":
    initialize_database()
    main_menu()