from models.category import Category
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from rich.prompt import Prompt
from rich.console import Console

# Create tables if they don't exist
Category.create_table()
Ingredient.create_table()
Recipe.create_table()
RecipeIngredient.create_table()

# Category:


def create_category():
    console = Console()

    name = Prompt.ask("[blue]Enter the name of the category[/blue]")
    category = Category(name)
    category.save()
    console.print()
    console.print(f"[magenta]Category '{name}' created successfully.[/magenta]")


def delete_category():
    console = Console()

    name = Prompt.ask("[blue]Enter the name of the category to delete[/blue]")
    category = Category.find_by_name(name)
    console.print()
    if category:
        category.delete()
        console.print(f"[magenta]Category '{name}' deleted successfully![/magenta]")
    else:
        console.print(f"[red]Category '{name}' not found.[/red]")


def display_all_categories():
    console = Console()

    categories = Category.get_all()
    if categories:
        console.print("[white]All Categories:[/white]")
        console.print()
        for category in categories:
            console.print(f"[magenta]- {category.name}[/magenta]")
    else:
        console.print()
        console.print("[red]No categories found.[/red]")


def category_by_id():
    console = Console()

    id_ = Prompt.ask("[blue]Enter the category's id[/blue]")
    console.print()
    category = Category.find_by_id(id_)
    if category:
        console.print(f"[magenta]Category: {category.name}[/magenta]")
    else:
        console.print(f"[red]Category {id_} not found[/red]")


def update_category():
    console = Console()
    id_ = Prompt.ask("[blue]Enter the category id[/blue]")
    if category := Category.find_by_id(id_):
        try:
            name = Prompt.ask("[blue]Enter the new category name[/blue]")
            category.name = name
            category.update()
            console.print()
            console.print(f"[magenta]Category '{name}' successfully updated![/magenta]")

        except Exception as exc:
            console.print()
            console.print(f"[red]Error updating category:[/red] {exc}")
    else:
        console.print()
        console.print(f"[red]Category {id_} not found[/red]")


if __name__ == "__main__":
    update_category()


# Ingredient:


def create_ingredient():
    console = Console()

    name = Prompt.ask("[blue]Enter the name of the ingredient[/blue]")
    ingredient = Ingredient(name)
    ingredient.save()
    console.print()
    console.print(f"[magenta]Ingredient '{name}' created successfully.[/magenta]")


def delete_ingredient():
    console = Console()

    name = Prompt.ask("[blue]Enter the name of the ingredient to delete[/blue]")
    ingredient = Ingredient.find_by_name(name)
    console.print()
    if ingredient:
        ingredient.delete()
        console.print(f"[magenta]Ingredient '{name}' deleted successfully![/magenta]")
    else:
        console.print(f"[red]Ingredient '{name}' not found.[/red]")


def display_all_ingredients():
    console = Console()

    ingredients = Ingredient.get_all()
    if ingredients:
        console.print("[white]All Ingredients:[/white]")
        console.print()
        for ingredient in ingredients:
            console.print(f"[magenta]- {ingredient.name}[/magenta]")
    else:
        console.print()
        console.print("[red]No ingredients found.[/red]")


def ingredient_by_id():
    console = Console()

    id_ = Prompt.ask("[blue]Enter the ingredient's id[/blue]")
    ingredient = Ingredient.find_by_id(id_)
    console.print()
    if ingredient:
        console.print(f"[magenta]Ingredient: {ingredient.name}[/magenta]")
    else:
        console.print(f"[red]Ingredient {id_} not found[/red]")


def update_ingredient():
    console = Console()

    id_ = Prompt.ask("[blue]Enter the ingredient id[/blue]")

    if ingredient := Ingredient.find_by_id(id_):
        try:
            name = Prompt.ask("[blue]Enter the new ingredient name[/blue]")
            ingredient.name = name
            ingredient.update()
            console.print()
            console.print("[magenta]Ingredient successfully updated![/magenta]")

        except Exception as exc:
            console.print()
            console.print("[red]Error updating ingredient[/red]", exc)
    else:
        console.print()
        console.print(f"[red]Ingredient {id_} not found[/red]")


# Recipe:


def create_recipe():
    console = Console()

    title = Prompt.ask("[blue]Enter the title of the recipe[/blue]")
    instructions = Prompt.ask("[blue]Enter the instructions for the recipe[/blue]")
    category_id = Prompt.ask("[blue]Enter the category ID for the recipe[/blue]")
    category = Category.find_by_id(category_id)

    if category:
        ingredients_input = Prompt.ask(
            "[blue]Enter the ingredients for the recipe (comma-separated)[/blue]"
        )
        ingredients_list = [
            ingredient.strip() for ingredient in ingredients_input.split(",")
        ]

        saved_ingredient_ids = []
        for ingredient_name in ingredients_list:
            existing_ingredient = Ingredient.find_by_name(ingredient_name)

            if existing_ingredient:
                ingredient_id = existing_ingredient.id
            else:
                new_ingredient = Ingredient(ingredient_name)
                new_ingredient.save()
                ingredient_id = new_ingredient.id

            saved_ingredient_ids.append(ingredient_id)
        recipe = Recipe(title, instructions, category, ingredients_list, None)
        recipe.save()
        for ingredient_id in saved_ingredient_ids:
            RecipeIngredient(recipe, Ingredient.find_by_id(ingredient_id)).save()
        console.print()
        console.print(f"[magenta]Recipe '{title}' created successfully.[/magenta]")
    else:
        console.print()
        console.print(f"[red]Category with ID {category_id} not found[/red]")


def delete_recipe():
    console = Console()

    title = Prompt.ask("[bold blue]Enter the title of the recipe to delete[/bold blue]")
    recipe = Recipe.find_by_title(title)
    if recipe:
        recipe.delete()
        console.print()
        console.print(f"[magenta]Recipe '{title}' successfully deleted.[/magenta]")
    else:
        console.print()
        console.print(f"[red]Recipe '{title}' not found.[/red]")


def display_all_recipes():
    console = Console()

    recipes = Recipe.get_all()
    if recipes:
        console.print("[white]All Recipes:[/white]")
        console.print()
        for recipe in recipes:
            console.print(f"[magenta]Title:[/magenta] [blue]{recipe.title}[/blue]")
            console.print(
                f"[magenta]Instructions:[/magenta] [blue]{recipe.instructions}[/blue]"
            )
            console.print(
                f"[magenta]Category:[/magenta] [blue]{recipe.category.name if recipe.category else 'Uncategorized'}[/blue]"
            )
            console.print(f"[magenta]Ingredients:[/magenta]")
            for ingredient in recipe.ingredients:
                console.print(f"[blue]- {ingredient}[/blue]")
            console.print()
    else:
        console.print()
        console.print(f"[red]No recipes found.[/red]")


def recipe_by_id():
    console = Console()

    id_ = Prompt.ask("[blue]Enter the recipe's id[/blue]")
    console.print()

    recipe = Recipe.find_by_id(id_)

    if recipe:
        console.print("[white]Recipe Details:[/white]")
        console.print()
        console.print(f"[magenta]Title:[/magenta] [blue]{recipe.title}[/blue]")
        console.print(
            f"[magenta]Instructions:[/magenta] [blue]{recipe.instructions}[/blue]"
        )
        console.print(
            f"[magenta]Category:[/magenta] [blue]{recipe.category.name if recipe.category else 'Uncategorized'}[/blue]"
        )
        console.print(f"[magenta]Ingredients:[/magenta]")
        for ingredient in recipe.ingredients:
            console.print(f"[blue]- {ingredient}[/blue]")
    else:
        console.print(f"[red]Recipe {id_} not found[/red]")


def update_recipe():
    console = Console()

    id_ = Prompt.ask("[blue]Enter the recipe id[/blue]")
    recipe = Recipe.find_by_id(id_)

    if recipe:
        try:
            title = Prompt.ask("[blue]Enter the new recipe title[/blue]")
            instructions = Prompt.ask("[blue]Enter the new instructions[/blue]")
            category_id = Prompt.ask("[blue]Enter the new category ID[/blue]")
            category = Category.find_by_id(category_id)

            if category:
                recipe.title = title
                recipe.instructions = instructions
                recipe.category = category

                ingredients_input = Prompt.ask(
                    "[blue]Enter the updated ingredients (comma-separated)[/blue]"
                )
                ingredients_list = [
                    ingredient.strip() for ingredient in ingredients_input.split(",")
                ]

                console.print()

                saved_ingredient_ids = []
                for ingredient_name in ingredients_list:
                    existing_ingredient = Ingredient.find_by_name(ingredient_name)

                    if existing_ingredient:
                        ingredient_id = existing_ingredient.id
                    else:
                        new_ingredient = Ingredient(ingredient_name)
                        new_ingredient.save()
                        ingredient_id = new_ingredient.id

                    saved_ingredient_ids.append(ingredient_id)

                RecipeIngredient.delete_by_recipe_id(recipe.id)

                for ingredient_id in saved_ingredient_ids:
                    RecipeIngredient(
                        recipe, Ingredient.find_by_id(ingredient_id)
                    ).save()

                recipe.update()

                console.print(f"[magenta]Recipe successfully updated![/magenta]")

            else:
                console.print()
                console.print(f"[red]Category with ID {category_id} not found[/red]")

        except Exception as exc:
            console.print()
            console.print(f"[red]Error updating recipe: {exc}[/red]")
    else:
        console.print()
        console.print(f"[red]Recipe {id_} not found[/red]")


# RecipeIngredient:


def ingredient_by_recipe_id():
    console = Console()

    recipe_id = Prompt.ask("[blue]Enter the recipe's id[/blue]")
    ingredients = RecipeIngredient.find_by_recipe_id(recipe_id)

    console.print()
    if ingredients:
        console.print(
            f"[magenta]Ingredients for recipe {recipe_id}:[/magenta] {', '.join(ingredients)}"
        )
    else:
        console.print(f"[red]No ingredients found for recipe {recipe_id}[/red]")


# Program:


def exit_program():
    console = Console()

    console.print("[magenta]Thanks for cooking with us today, chef![/magenta]")
    console.print()
    exit()
