<h1><b>🌟Introducing: The Cookbook Chronicles - Your Epic Culinary Odyssey!🌟</b></h1>

Ahoy there, Culinary Captains! Embark on a gastronomic journey like never before with The Cookbook Chronicles. This isn't just a recipe organizer; it's your passport to a world of flavors, a digital haven for your culinary escapades!

Here's why The Cookbook Chronicles is the ultimate companion for your kitchen adventures:

<h2><b>🍽️ Unleash Your Culinary Creativity:</b></h2>

Dive into a realm where creating new recipes is a joyous celebration of flavors and innovation.

<h2><b>🔥 Ingredient Extravaganza:</b></h2>

Uncover the secrets of your dishes by exploring the intricate dance of ingredients and categories in each recipe.

<h2><b>✨ Power Over Delete and Update:</b></h2>

Fear not the culinary missteps! Exercise your chef's prerogative to delete/update recipes, ingredients, or categories with the swipe of a digital spatula.

Let The Cookbook Chronicles be your culinary compass, steering you towards a symphony of taste that echoes with your kitchen prowess! Happy Cooking!

<h1>Project Details</h1>

<h2>Getting Started:</h2>

To start this program, please follow the instructions below:

1. Navigate to the folder that holds all program files.
2. Type “pipenv install” and press enter to install necessary dependencies.
3. Type “pipenv shell” and press enter to start the virtual environment.
4. Run "python lib/cli.py" to start the program.

<h2>Using this Program</h2>

Explore the program through these different menu options:

0- Kitchen's closed: closes the menu and brings users back to the program files.
1- Create a new recipe: enter the title, ingredients, instructions, and category to create a new recipe.
2- Delete a recipe: enter the title of the recipe to delete.
3- Display all recipes: displays all recipes and associated information.
4- Find a recipe by title: returns the recipe object after searching by recipe title.
5- Find a recipe by ID: returns the recipe title after searching by recipe ID.
6- Add a new ingredient: add a new ingredient by entering the name and recipe ID(s) the ingredient is associated with (recipe ID is optional).
7- Delete an ingredient: enter the name of the ingredient to delete.
8- Display all ingredients: displays all ingredients.
9- Find recipe(s) by the ingredient name: display the associated recipe title(s) by searching for an ingredient name.
10- Find an ingredient by ID: returns the ingredient name after searching by ingredient ID.
11- Update an existing ingredient: update an ingredient's name and/or recipe ID(s).
12- Add a new category: add a new category by entering the name and recipe ID(s) the category is associated with (recipe ID is optional).
13- Delete a category: enter the name of the category to delete.
14- Display all categories: displays all categories.
15- Find recipe(s) by the category name: display the associated recipe title(s) by searching for a category name.
16- Find a category by ID: returns the category name after searching by category ID.
17- Update an existing category: update a category's name and/or recipe ID(s).

<h2>Program Information</h2>

```console
.
└── lib
    ├── models
        ├── __init__.py
        ├── category.py
        └── ingredient.py
        ├── recipe.py
    ├── cli.py
    ├── debug.py
    ├── helpers.py
├── Pipfile
├── Pipfile.lock
├── README.md
```
