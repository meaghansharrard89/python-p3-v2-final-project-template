from models.category import Category
from models.ingredient import Ingredient
from models.recipe import Recipe

# Create tables if they don't exist
Category.create_table()
Ingredient.create_table()
Recipe.create_table()

# Category:


def create_category():
    name = input("Enter the name of the category: ")
    category = Category(name)
    category.save()
    print(f"Category '{name}' created successfully!")


def delete_category():
    name = input("Enter the name of the category to delete: ")
    category = Category.find_by_name(name)
    if category:
        category.delete()
        print(f"Category '{name}' deleted successfully!")
    else:
        print(f"Category '{name}' not found.")


def display_all_categories():
    categories = Category.get_all()
    if categories:
        print("All Categories:")
        for category in categories:
            print(f"- {category.name}")
    else:
        print("No categories found.")


# Ingredient:


def create_ingredient():
    name = input("Enter the name of the ingredient: ")

    # Prompt user for recipe_id only if it's associated with a recipe
    recipe_id_input = input(
        "Enter the ID of the recipe to associate with (leave blank for none): "
    )

    if recipe_id_input:
        try:
            recipe_id = int(recipe_id_input)
        except ValueError:
            print("Invalid recipe ID. Please enter a valid integer.")
            return

        recipe = Recipe.find_by_id(recipe_id)

        if recipe:
            ingredient = Ingredient(name, recipe_id)
            ingredient.save()
            recipe.associate_ingredient(ingredient)
            print(
                f"Ingredient '{name}' created and associated with recipe '{recipe.name}'."
            )
        else:
            print(f"Recipe with ID {recipe_id} not found.")
    else:
        # If not associated with a recipe, create the ingredient without a recipe_id
        ingredient = Ingredient(name)
        ingredient.save()
        print(f"Ingredient '{name}' created successfully.")


def delete_ingredient():
    name = input("Enter the name of the ingredient to delete: ")
    ingredient = Ingredient.find_by_name(name)
    if ingredient:
        ingredient.delete()
        print(f"Ingredient '{name}' deleted successfully!")
    else:
        print(f"Ingredient '{name}' not found.")


def display_all_ingredients():
    ingredients = Ingredient.get_all()
    if ingredients:
        print("All Ingredients:")
        for ingredient in ingredients:
            print(f"- {ingredient.name}")
    else:
        print("No ingredients found.")


# Recipe:


def create_recipe():
    # Create a new recipe instance
    title = input("Enter the title of the recipe: ")
    # Allow the user to add ingredients
    ingredients = []
    while True:
        ingredient_name = input("Enter an ingredient name (leave blank to finish): ")
        if not ingredient_name:
            break
        ingredients.append(ingredient_name)
    instructions = input("Enter the instructions for the recipe: ")

    if (
        not instructions.strip()
    ):  # Check if the string is empty or contains only whitespace
        print("Instructions must be a non-empty string.")
        return  # Exit the function without creating the Recipe object

    recipe = Recipe(title, instructions)

    # Add ingredients to the recipe
    for ingredient_name in ingredients:
        recipe.add_ingredient(ingredient_name)

    # Save the recipe
    recipe.save()

    print(f"Recipe '{title}' created successfully with ingredients and instructions!")


def delete_recipe():
    title = input("Enter the title of the recipe to delete: ")
    recipe = Recipe.find_by_title(title)
    if recipe:
        recipe.delete()
        print(f"Recipe '{title}' deleted successfully!")
    else:
        print(f"Recipe '{title}' not found.")


def display_all_recipes():
    recipes = Recipe.get_all()
    if recipes:
        print("All Recipes:")
        for recipe in recipes:
            print(f"Title: {recipe.name}")
            print(f"Category: {recipe.category}")
            print(f"Ingredients: {recipe.ingredients}")
            print(f"Instructions: {recipe.instructions}")
    else:
        print("No recipes found.")


# Program:


def exit_program():
    print("Goodbye!")
    exit()
