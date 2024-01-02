from models.category import Category
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient

# Create tables if they don't exist
Category.create_table()
Ingredient.create_table()
Recipe.create_table()
RecipeIngredient.create_table()

# Category:


def create_category():
    name = input("Enter the name of the category: ")
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


def category_by_id():
    # Find the category by ID
    id_ = input("Enter the category's id: ")
    category = Category.find_by_id(id_)
    print(category.name) if category else print(f"Category {id_} not found")


def update_category():
    # Update the category
    id_ = input("Enter the category id: ")
    if category := Category.find_by_id(id_):
        try:
            name = input("Enter the new category name: ")
            category.name = name
            category.update()

            print(f"Category successfully updated!\nCategory: {category.name}")

        except Exception as exc:
            print("Error updating category:", exc)
    else:
        print(f"Category {id_} not found")


# Ingredient:


def create_ingredient():
    name = input("Enter the name of the ingredient: ")
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


def ingredient_by_id():
    # Find ingredient by ID
    id_ = input("Enter the ingredient's id: ")
    ingredient = Ingredient.find_by_id(id_)
    print(ingredient.name) if ingredient else print(f"Ingredient {id_} not found")


def update_ingredient():
    # Update ingredient
    id_ = input("Enter the ingredient id: ")
    if ingredient := Ingredient.find_by_id(id_):
        try:
            name = input("Enter the new ingredient name: ")
            ingredient.name = name
            ingredient.update()

            print(f"Ingredient successfully updated!\nIngredient: {ingredient.name}")

        except Exception as exc:
            print("Error updating ingredient:", exc)
    else:
        print(f"Ingredient {id_} not found")


# Recipe:


def create_recipe():
    title = input("Enter the title of the recipe: ")
    instructions = input("Enter the instructions for the recipe: ")
    category_id = input("Enter the category ID for the recipe: ")

    # Check if the provided category ID exists
    category = Category.find_by_id(category_id)

    if category:
        ingredients_input = input(
            "Enter the ingredients for the recipe (comma-separated): "
        )
        ingredients_list = [
            ingredient.strip() for ingredient in ingredients_input.split(",")
        ]

        # Check and save ingredients
        saved_ingredient_ids = []
        for ingredient_name in ingredients_list:
            existing_ingredient = Ingredient.find_by_name(ingredient_name)

            if existing_ingredient:
                # Use the existing ingredient ID
                ingredient_id = existing_ingredient.id
            else:
                # Create and save a new ingredient
                new_ingredient = Ingredient(ingredient_name)
                new_ingredient.save()
                ingredient_id = new_ingredient.id

            saved_ingredient_ids.append(ingredient_id)

        # Create the recipe without saving it first
        recipe = Recipe(title, instructions, category, ingredients_list, None)

        # Save the recipe
        recipe.save()

        # Add the recipe and ingredient associations to RecipeIngredient
        for ingredient_id in saved_ingredient_ids:
            RecipeIngredient(recipe, Ingredient.find_by_id(ingredient_id)).save()

        print(f"Recipe '{title}' created successfully.")
    else:
        print(f"Category with ID {category_id} not found")


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
            print(f"Instructions: {recipe.instructions}")
            print(
                f"Category: {recipe.category.name if recipe.category else 'Uncategorized'}"
            )
            print(f"Ingredients: {recipe.ingredients}")
    else:
        print("No recipes found.")


def recipe_by_id():
    # Find recipe by ID
    id_ = input("Enter the recipe's id: ")
    recipe = Recipe.find_by_id(id_)
    print(recipe.title) if recipe else print(f"Recipe {id_} not found")


def update_recipe():
    # Update recipe
    id_ = input("Enter the recipe id: ")
    if recipe := Recipe.find_by_id(id_):
        try:
            title = input("Enter the new recipe title: ")
            instructions = input("Enter the new instructions: ")
            category_id = input("Enter the new category ID: ")

            # Check if the provided category ID exists
            category = Category.find_by_id(category_id)
            if category:
                # Update recipe attributes
                recipe.title = title
                recipe.instructions = instructions
                recipe.category = category

                # Update ingredients separately
                ingredients_input = input(
                    "Enter the updated ingredients (comma-separated): "
                )
                ingredients_list = [
                    ingredient.strip() for ingredient in ingredients_input.split(",")
                ]

                # Check and save ingredients
                saved_ingredient_ids = []
                for ingredient_name in ingredients_list:
                    existing_ingredient = Ingredient.find_by_name(ingredient_name)

                    if existing_ingredient:
                        # Use the existing ingredient ID
                        ingredient_id = existing_ingredient.id
                    else:
                        # Create and save a new ingredient
                        new_ingredient = Ingredient(ingredient_name)
                        new_ingredient.save()
                        ingredient_id = new_ingredient.id

                    saved_ingredient_ids.append(ingredient_id)

                # Delete existing recipe-ingredient associations
                RecipeIngredient.delete_by_recipe_id(recipe.id)

                # Add the updated recipe and ingredient associations to RecipeIngredient
                for ingredient_id in saved_ingredient_ids:
                    RecipeIngredient(
                        recipe, Ingredient.find_by_id(ingredient_id)
                    ).save()

                # Update the recipe in the database after updating both attributes and ingredients
                recipe.ingredients = ingredients_list
                recipe.update()

                print(f"Recipe successfully updated!\nRecipe: {recipe.title}")

            else:
                print(f"Category with ID {category_id} not found")

        except Exception as exc:
            print("Error updating recipe:", exc)
    else:
        print(f"Recipe {id_} not found")


# Program:


def exit_program():
    print("Thanks for cooking with us today, chef!")
    exit()
