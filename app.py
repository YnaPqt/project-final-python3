from models import initialize_database
from Projet_Final_Python3.anime_functions import(
    create_anime,
    list_anime,
    update_anime,
    delete_anime
)

def main_menu():
    while True:
        print("\n === ANIME DATABASE ===")
        print("1. Create Anime")
        print("2. View list Anime")
        print("3. Update Anime")
        print("4. Delete Anime")
        print("5. Exit")

        choice = input("Choice: ")

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