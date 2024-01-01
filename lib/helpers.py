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

    # Prompt user for recipe IDs if they are associated with the category
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
    # Find the recipe IDs associated with the category name
    name = input("Enter the category name: ")
    recipe_ids = Category.find_recipe_id_by_name(name)

    if recipe_ids is not None:
        if isinstance(recipe_ids, int):
            # If there's only one recipe ID, convert it to a list
            recipe_ids_list = [recipe_ids]
        else:
            # If there are multiple recipe IDs, split the string into a list
            recipe_ids_list = [int(id.strip()) for id in recipe_ids.split(",")]

        print(f"Category: {name}")

        for recipe_id in recipe_ids_list:
            recipe = Recipe.find_by_id(recipe_id)
            if recipe:
                print(f"  Recipe Title: {recipe.title}")
            else:
                print(f"  Recipe with ID {recipe_id} not found")
    else:
        print(f"No category found with the name {name}")


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

            recipe_ids_input = input("Enter the new recipe ID(s): ")
            recipe_ids = (
                [int(id_.strip()) for id_ in recipe_ids_input.split(",")]
                if recipe_ids_input
                else []
            )

            # Save the recipe IDs before updating the category
            category.recipe_id = recipe_ids
            category.update_recipe_ids()
            category.update()

            print(f"Category successfully updated!\nCategory: {category.name}")

            if recipe_ids:
                for recipe_id in recipe_ids:
                    recipe = Recipe.find_by_id(recipe_id)
                    if recipe:
                        print(f"Recipe Title: {recipe.title}")
                    else:
                        print(f"Recipe with ID {recipe_id} not found")

        except Exception as exc:
            print("Error updating category:", exc)
    else:
        print(f"Category {id_} not found")


# Ingredient:


def create_ingredient():
    name = input("Enter the name of the ingredient: ")
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
        # If not associated with any recipes, create the ingredient without recipe IDs
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
    # Find the recipe ID(s) associated with the ingredient name
    name = input("Enter the ingredient's name: ")
    recipe_ids = Ingredient.find_recipe_id_by_name(name)
    if recipe_ids is not None:
        if isinstance(recipe_ids, int):
            # If there's only one recipe ID, convert it to a list
            recipe_ids_list = [recipe_ids]
        else:
            # If there are multiple recipe IDs, split the string into a list
            recipe_ids_list = [int(id.strip()) for id in recipe_ids.split(",")]
        print(f"Ingredient: {name}")

        for recipe_id in recipe_ids_list:
            recipe = Recipe.find_by_id(recipe_id)
            if recipe:
                print(f"  Recipe Title: {recipe.title}")
            else:
                print(f"  Recipe with ID {recipe_id} not found")
    else:
        print(f"No ingredient found with the name {name}")


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

            recipe_ids_input = input("Enter the new recipe ID(s): ")
            recipe_ids = (
                [int(id_.strip()) for id_ in recipe_ids_input.split(",")]
                if recipe_ids_input
                else []
            )

            # Save the recipe IDs before updating the ingredient
            ingredient.recipe_id = recipe_ids
            ingredient.update_recipe_ids()
            ingredient.update()

            print(f"Ingredient successfully updated!\nIngredient: {ingredient.name}")

            if recipe_ids:
                for recipe_id in recipe_ids:
                    recipe = Recipe.find_by_id(recipe_id)
                    if recipe:
                        print(f"Recipe Title: {recipe.title}")
                    else:
                        print(f"Recipe with ID {recipe_id} not found")

        except Exception as exc:
            print("Error updating ingredient:", exc)
    else:
        print(f"Ingredient {id_} not found")


# IN PROGRESS
def ingredient_by_recipe_id():
    recipe_id = input("Enter the recipe ID: ")

    # Find the ingredient names associated with the recipe ID
    ingredient_names = Ingredient.find_recipe_id_by_name(recipe_id)

    if ingredient_names is not None:
        if isinstance(ingredient_names, str):
            # If there's only one ingredient name, convert it to a list
            ingredient_names_list = [ingredient_names]
        else:
            # If there are multiple ingredient names, split the string into a list
            ingredient_names_list = [
                name.strip() for name in ingredient_names.split(",")
            ]

        # Print the recipe's ID
        print(f"Recipe ID: {recipe_id}")

        # Print the names of associated ingredients
        for ingredient_name in ingredient_names_list:
            ingredient = Ingredient.find_by_name(ingredient_name)
            if ingredient:
                print(f"  Ingredient Name: {ingredient_name}")
            else:
                print(f"  Ingredient with name {ingredient_name} not found")
    else:
        print(f"No ingredients found for the recipe with ID {recipe_id}")


# Recipe:


def create_recipe():
    title = input("Enter the title of the recipe: ")
    ingredients = input(
        "Enter the ingredients for the recipe (comma-separated): "
    ).split(",")
    instructions = input("Enter the instructions for the recipe: ")
    if not instructions.strip():
        print("Instructions must be a non-empty string.")
        return
    category_name = input("Enter the category for the recipe: ")
    recipe = Recipe(title, instructions, ingredients, category_name)
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
    # Find recipe by title
    name = input("Enter the recipe's title: ")
    recipe = Recipe.find_by_title(name)
    print(recipe) if recipe else print(f"Recipe {name} not found")


def recipe_by_id():
    # Find recipe by ID
    id_ = input("Enter the recipe's id: ")
    recipe = Recipe.find_by_id(id_)
    print(recipe.title) if recipe else print(f"Recipe {id_} not found")


# Program:


def exit_program():
    print("Thanks for cooking with us today, chef!")
    exit()
