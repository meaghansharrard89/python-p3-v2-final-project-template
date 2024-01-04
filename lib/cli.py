from rich.console import Console
from rich.table import Table

from helpers import (
    exit_program,
    create_category,
    delete_category,
    display_all_categories,
    update_category,
    category_by_id,
    create_ingredient,
    delete_ingredient,
    display_all_ingredients,
    ingredient_by_id,
    update_ingredient,
    create_recipe,
    delete_recipe,
    display_all_recipes,
    recipe_by_id,
    update_recipe,
    ingredient_by_recipe_id,
)


def display_logo():
    console = Console()

    top_line = """
**********************************************
    """
    logo = """
 _____ _                                        
|_   _| |                                       
  | | | |__   ___                               
  | | | '_ \ / _ \\                              
  | | | | | |  __/                              
 _____|_| |_|\\___| _    _                 _     
/  __ \           | |  | |               | |    
| /  \/ ___   ___ | | _| |__   ___   ___ | | __ 
| |    / _ \ / _ \| |/ | '_ \ / _ \ / _ \| |/ / 
| \__/| (_) | (_) |   <| |_) | (_) | (_) |   <  
 _____/____/ \___/|_|\_|_.__/_\___/ ____/|_|\_\ 
/  __ | |                   (_)    | |          
| /  \| |__  _ __ ___  _ __  _  ___| | ___ ___  
| |   | '_ \| '__/ _ \| '_ \| |/ __| |/ _ / __| 
| \__/| | | | | | (_) | | | | | (__| |  __\__ \\ 
 \____|_| |_|_|  \___/|_| |_|_|\___|_|\___|___/ 

"""

    bottom_line = """

***********************************************
    
     A CLI project by Meaghan Sharrard

***********************************************

"""
    console.print(top_line, style="magenta")
    console.print(logo, style="bold green")
    console.print(bottom_line, style="magenta")


def main():
    console = Console()

    logo = True
    while True:
        if logo is True:
            display_logo()
            logo = False

        menu()
        choice = input("> ")
        console.print()
        if choice == "0":
            exit_program()
        elif choice == "1":
            create_recipe()
        elif choice == "2":
            display_all_recipes()
        elif choice == "3":
            recipe_by_id()
        elif choice == "4":
            update_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "6":
            create_ingredient()
        elif choice == "7":
            display_all_ingredients()
        elif choice == "8":
            ingredient_by_id()
        elif choice == "9":
            update_ingredient()
        elif choice == "10":
            ingredient_by_recipe_id()
        elif choice == "11":
            delete_ingredient()
        elif choice == "12":
            create_category()
        elif choice == "13":
            display_all_categories()
        elif choice == "14":
            category_by_id()
        elif choice == "15":
            update_category()
        elif choice == "16":
            delete_category()
        else:
            print("Invalid choice")


def menu():
    console = Console()

    options = [
        "Kitchen's closed",
        "Create a new recipe",
        "Display all recipes",
        "Find a recipe by ID",
        "Update an existing recipe",
        "Delete a recipe",
        "Add a new ingredient",
        "Display all ingredients",
        "Find an ingredient by ID",
        "Update an existing ingredient",
        "Find ingredients by recipe ID",
        "Delete an ingredient",
        "Add a new category",
        "Display all categories",
        "Find a category by ID",
        "Update an existing category",
        "Delete a category",
    ]

    console.print()

    for index, option in enumerate(options):
        # Use different colors for numbers and options
        number_style = "magenta"
        option_style = "green"

        console.print(f"[{index}]", style=number_style, end=" ")
        console.print(option, style=option_style)

        if index == 16:
            console.print()  # This adds a line break


if __name__ == "__main__":
    main()
