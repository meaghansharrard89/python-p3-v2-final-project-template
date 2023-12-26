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
    ingredient = Ingredient(name)
    ingredient.save()
    print(f"Ingredient '{name}' created successfully!")


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
    title = input("Enter the title of the recipe: ")
    instructions = input("Enter the instructions for the recipe: ")
    recipe = Recipe(title, instructions)
    recipe.save()
    print(f"Recipe '{title}' created successfully!")


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
            print(f"- Title: {recipe.title}")
            print(f"  Instructions: {recipe.instructions}")
            print()
    else:
        print("No recipes found.")


# Program:


def exit_program():
    print("Goodbye!")
    exit()
