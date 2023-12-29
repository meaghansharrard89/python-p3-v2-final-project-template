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

<ul>
    <li><b>0- Kitchen's closed:</b> closes the menu and brings users back to the program files.</li>
    <li><b>1- Create a new recipe:</b> enter the title, ingredients, instructions, and category to create a new recipe.</li>
    <li><b>2- Delete a recipe:</b> enter the title of the recipe to delete.</li>
    <li><b>3- Display all recipes:</b> displays all recipes and associated information.</li>
    <li><b>4- Find a recipe by title:</b> returns the recipe object after searching by recipe title.</li>
    <li><b>5- Find a recipe by ID:</b> returns the recipe title after searching by recipe ID.</li>
    <li><b>6- Add a new ingredient:</b> add a new ingredient by entering the name and recipe ID(s) the ingredient is associated with (recipe ID is optional).</li>
    <li><b>7- Delete an ingredient:</b> enter the name of the ingredient to delete.</li>
    <li><b>8- Display all ingredients:</b> displays all ingredients.</li>
    <li><b>9- Find recipe(s) by the ingredient name:</b> display the associated recipe title(s) by searching for an ingredient name.</li>
    <li><b>10- Find an ingredient by ID:</b> returns the ingredient name after searching by ingredient ID.</li>
    <li><b>11- Update an existing ingredient:</b> update an ingredient's name and/or recipe ID(s).</li>
    <li><b>12- Add a new category:</b> add a new category by entering the name and recipe ID(s) the category is associated with (recipe ID is optional).</li>
    <li><b>13- Delete a category:</b> enter the name of the category to delete.</li>
    <li><b>14- Display all categories:</b> displays all categories.</li>
    <li><b>15- Find recipe(s) by the category name:</b> display the associated recipe title(s) by searching for a category name.</li>
    <li><b>16- Find a category by ID:</b> returns the category name after searching by category ID.</li>
    <li><b>17- Update an existing category:</b> update a category's name and/or recipe ID(s).</li>
</ul>

<h2>Program Information</h2>

```console

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

<h3>category.py</h3>

Category contains an ID column, category name column (breakfast, lunch, etc.) and a recipe ID column, which is connected to recipes in recipe.py.

<h3>ingredient.py</h3>

Ingredient contains an ID column, ingredient name column (salt, butter, etc.) and a recipe ID column, which is connected to recipes in recipe.py.

<h3>recipes.py</h3>

Recipe contains five columns: ID, title, ingredients, instructions, and category.

<h3>cli.py</h3>

Imports functions from helper.py and organizes them in a way that matches what the user sees in their terminal.

<h3>helpers.py</h3>

These functions allow the user to interact with the database with the help of functions imported from category.py, recipe.py, and ingredient.py.
