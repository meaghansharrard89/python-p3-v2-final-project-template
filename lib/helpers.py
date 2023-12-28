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

    # Prompt user for recipe_ids if they are associated with recipes
    recipe_id_input = input(
        "Enter the IDs of the recipes to associate with (comma-separated, leave blank for none): "
    )

    if recipe_id_input:
        recipe_ids = [int(id.strip()) for id in recipe_id_input.split(",")]
        valid_recipe_ids = []

        for recipe_id in recipe_ids:
            recipe = Recipe.find_by_id(recipe_id)
            if recipe:
                valid_recipe_ids.append(recipe_id)
            else:
                print(f"Recipe with ID {recipe_id} not found.")

        if valid_recipe_ids:
            # Create the category without saving it first
            category = Category(name)

            # Associate the category with recipes
            for valid_recipe_id in valid_recipe_ids:
                recipe = Recipe.find_by_id(valid_recipe_id)
                recipe.associate_category(category, valid_recipe_id)

            # Save the category after associating it with recipes
            category.save()

            # Use the valid_recipe_ids directly, not recipe_id
            recipe_titles = [
                Recipe.find_by_id(recipe_id).title for recipe_id in valid_recipe_ids
            ]
            print(
                f"Category '{name}' created and associated with recipes: {', '.join(recipe_titles)}."
            )
        else:
            print(
                "No valid recipes found. Category will be created without associations."
            )
    else:
        # If not associated with any recipes, create the category without recipe_ids
        category = Category(name)
        category.save()
        print(f"Category '{name}' created successfully.")


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


def category_by_name():
    name = input("Enter the category name: ")

    # Find the recipe_ids associated with the category
    recipe_ids = Category.find_recipe_id_by_name(name)

    if recipe_ids is not None:
        if isinstance(recipe_ids, int):
            # If there's only one recipe_id, convert it to a list
            recipe_ids_list = [recipe_ids]
        else:
            # If there are multiple recipe_ids, split the string into a list
            recipe_ids_list = [int(id.strip()) for id in recipe_ids.split(",")]

        # Print the category name
        print(f"Category: {name}")

        # Print the titles of associated recipes
        for recipe_id in recipe_ids_list:
            recipe = Recipe.find_by_id(recipe_id)
            if recipe:
                print(f"  Recipe Title: {recipe.title}")
            else:
                print(f"  Recipe with ID {recipe_id} not found")
    else:
        print(f"No category found with the name {name}")


def category_by_id():
    # use a trailing underscore not to override the built-in id function
    id_ = input("Enter the category's id: ")
    category = Category.find_by_id(id_)
    print(category.name) if category else print(f"Category {id_} not found")


# Ingredient:


def create_ingredient():
    name = input("Enter the name of the ingredient: ")

    # Prompt user for recipe_ids if they are associated with recipes
    recipe_id_input = input(
        "Enter the IDs of the recipes to associate with (comma-separated, leave blank for none): "
    )

    if recipe_id_input:
        recipe_ids = [int(id.strip()) for id in recipe_id_input.split(",")]
        valid_recipe_ids = []

        for recipe_id in recipe_ids:
            recipe = Recipe.find_by_id(recipe_id)
            if recipe:
                valid_recipe_ids.append(recipe_id)
            else:
                print(f"Recipe with ID {recipe_id} not found.")

        if valid_recipe_ids:
            # Create the ingredient without saving it first
            ingredient = Ingredient(name)

            # Associate the ingredient with recipes
            for valid_recipe_id in valid_recipe_ids:
                recipe = Recipe.find_by_id(valid_recipe_id)
                recipe.associate_ingredient(ingredient, valid_recipe_id)

            # Save the ingredient after associating it with recipes
            ingredient.save()

            # Use the valid_recipe_ids directly, not recipe_id
            recipe_titles = [
                Recipe.find_by_id(recipe_id).title for recipe_id in valid_recipe_ids
            ]
            print(
                f"Ingredient '{name}' created and associated with recipes: {', '.join(recipe_titles)}."
            )
        else:
            print(
                "No valid recipes found. Ingredient will be created without associations."
            )
    else:
        # If not associated with any recipes, create the ingredient without recipe_ids
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


def ingredient_by_name():
    name = input("Enter the ingredient's name: ")

    # Find the recipe_ids associated with the ingredient
    recipe_ids = Ingredient.find_recipe_id_by_name(name)

    if recipe_ids is not None:
        if isinstance(recipe_ids, int):
            # If there's only one recipe_id, convert it to a list
            recipe_ids_list = [recipe_ids]
        else:
            # If there are multiple recipe_ids, split the string into a list
            recipe_ids_list = [int(id.strip()) for id in recipe_ids.split(",")]

        # Print the ingredient's name
        print(f"Ingredient: {name}")

        # Print the titles of associated recipes
        for recipe_id in recipe_ids_list:
            recipe = Recipe.find_by_id(recipe_id)
            if recipe:
                print(f"  Recipe Title: {recipe.title}")
            else:
                print(f"  Recipe with ID {recipe_id} not found")
    else:
        print(f"No ingredient found with the name {name}")


def ingredient_by_id():
    # use a trailing underscore not to override the built-in id function
    id_ = input("Enter the ingredient's id: ")
    ingredient = Ingredient.find_by_id(id_)
    print(ingredient.name) if ingredient else print(f"Ingredient {id_} not found")


# Recipe:


def create_recipe():
    # Prompt user for recipe details
    title = input("Enter the title of the recipe: ")

    # Allow the user to add ingredients
    ingredients = input(
        "Enter the ingredients for the recipe (comma-separated): "
    ).split(",")

    instructions = input("Enter the instructions for the recipe: ")

    if not instructions.strip():
        print("Instructions must be a non-empty string.")
        return

    # Prompt user for category
    category_name = input("Enter the category for the recipe: ")

    # Create a new recipe instance
    recipe = Recipe(title, instructions, ingredients, category_name)

    # Save the recipe
    recipe.save()

    print(
        f"Recipe '{title}' created successfully with ingredients, instructions, and category '{category_name}'!"
    )


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
            print(f"Title: {recipe.title}")
            print(f"Ingredients: {recipe.ingredients}")
            print(f"Instructions: {recipe.instructions}")
            print(f"Category: {recipe.category}")
    else:
        print("No recipes found.")


def recipe_by_title():
    name = input("Enter the recipe's title: ")
    recipe = Recipe.find_by_title(name)
    print(recipe) if recipe else print(f"Recipe {name} not found")


def recipe_by_id():
    # use a trailing underscore not to override the built-in id function
    id_ = input("Enter the recipe's id: ")
    recipe = Recipe.find_by_id(id_)
    print(recipe.title) if recipe else print(f"Recipe {id_} not found")


# Program:


def exit_program():
    print("Thanks for cooking with us today, chef!")
    exit()
