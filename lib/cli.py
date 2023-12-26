# lib/cli.py

from helpers import (
    exit_program,
    create_category,
    delete_category,
    display_all_categories,
    create_ingredient,
    delete_ingredient,
    display_all_ingredients,
    create_recipe,
    delete_recipe,
    display_all_recipes,
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            create_category()
        elif choice == "2":
            delete_category()
        elif choice == "3":
            display_all_categories()
        elif choice == "4":
            create_ingredient()
        elif choice == "5":
            delete_ingredient()
        elif choice == "6":
            display_all_ingredients()
        elif choice == "7":
            create_recipe()
        elif choice == "8":
            delete_recipe()
        elif choice == "9":
            display_all_recipes()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Create a category")
    print("2. Delete a category")
    print("3. Display all categories")
    print("4. Create ingredient")
    print("5. Delete an ingredient")
    print("6. Display all ingredients")
    print("7. Create a recipe")
    print("8. Delete a recipe")
    print("9. Display all recipes")


if __name__ == "__main__":
    main()
