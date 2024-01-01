# lib/cli.py

from helpers import (
    exit_program,
    create_category,
    delete_category,
    display_all_categories,
    update_category,
    category_by_name,
    category_by_id,
    create_ingredient,
    delete_ingredient,
    display_all_ingredients,
    ingredient_by_name,
    ingredient_by_id,
    update_ingredient,
    ingredient_by_recipe_id,
    create_recipe,
    delete_recipe,
    display_all_recipes,
    recipe_by_title,
    recipe_by_id,
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
            recipe_by_title()
        elif choice == "5":
            recipe_by_id()
        elif choice == "6":
            create_ingredient()
        elif choice == "7":
            delete_ingredient()
        elif choice == "8":
            display_all_ingredients()
        elif choice == "9":
            ingredient_by_name()
        elif choice == "10":
            ingredient_by_id()
        elif choice == "11":
            ingredient_by_recipe_id()
        elif choice == "12":
            update_ingredient()
        elif choice == "13":
            create_category()
        elif choice == "14":
            delete_category()
        elif choice == "15":
            display_all_categories()
        elif choice == "16":
            category_by_name()
        elif choice == "17":
            category_by_id()
        elif choice == "18":
            update_category()
        else:
            print("Invalid choice")


def menu():
    print("Start cookin', chef!")
    print("0. Kitchen's closed")
    print("1. Create a new recipe")
    print("2. Delete a recipe")
    print("3. Display all recipes")
    print("4. Find a recipe by title")
    print("5. Find a recipe by ID")
    print("6. Add a new ingredient")
    print("7. Delete an ingredient")
    print("8. Display all ingredients")
    print("9. Find recipe(s) by the ingredient name")
    print("10. Find an ingredient by ID")
    print("11. Find ingredient(s) by recipe ID")
    print("12. Update an existing ingredient")
    print("13. Add a new category")
    print("14. Delete a category")
    print("15. Display all categories")
    print("16. Find recipe(s) by the category name")
    print("17. Find a category by ID")
    print("18. Update an existing category")


if __name__ == "__main__":
    main()
