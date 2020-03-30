Welcome to the recipe-app-api wiki!
Developed usinf DRF and Docker Compose

This api allows to perform CRUD operations over a Recipe, and uses custom user to authenticate.
* Users can create any recipe
* Users can list all the recipes
* Users can update/delete their own recipes



# User
## Properties (custom)
* Email
* Password
* Is_Active
* Is_Staff

## Methods:
* create: api/user/create
* details: api/user/me
* login: api/user/token

# Recipe
## Properties
* id
* title
* time (cooking time in minutes)
* price (cost of the ingredients needed)
* image (url of the image)
* tags (list of tags)
* ingredients (list of ingredients)

* A recipe can have many tags
* A recipe can have many ingredients

## Methods
* create: api/recipe/recipes/ - POST (authentication required)
* update: (authentication required)
* * api/recipe/recipes/{id}/ PUT  - updates the entire recipe with id={id}
* * api/recipe/recipes/{id}/ PATCH - partially updates the recipe with id={id}
* delete: api/recipe/recipes/{id}/ DELETE (authentication required) - deletes the recipe with id={id}
* list: api/recipe/recipes/ GET - return the list of all recipes in the system
* upload-image: api/recipe/recipes/{id}/upload-image POST - upload an image for the recipe with id={id}

# Tags
## Properites
* id
* name

## Methods
* list: api/recipe/tags GET - list all tags in the system
* create: api/recipe/tags POST - add new tag to the system

# Ingredients
## Properties
* id
* name

## Methods
* list: api/recipe/ingredients GET - list all ingredients in the system
* create: api/recipe/ingredients POST - add new ingredient to the system
