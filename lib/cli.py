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
            create_recipe()
        elif choice == "2":
            delete_recipe()
        elif choice == "3":
            display_all_recipes()
        elif choice == "4":
            create_ingredient()
        elif choice == "5":
            delete_ingredient()
        elif choice == "6":
            display_all_ingredients()
        elif choice == "7":
            create_category()
        elif choice == "8":
            delete_category()
        elif choice == "9":
            display_all_categories()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Create a new recipe")
    print("2. Delete a recipe")
    print("3. Display all recipes")
    print("4. Add a new ingredient")
    print("5. Delete an ingredient")
    print("6. Display all ingredients")
    print("7. Add a new category")
    print("8. Delete a category")
    print("9. Display all categories")


if __name__ == "__main__":
    main()
