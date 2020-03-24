from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients api """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving ingredients """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the private available ingredients api """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='django.test@mailinator.com',
            password='Pass_2020'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Test that ingredients are listed"""
        Ingredient.objects.create(user=self.user, name='Onion')
        Ingredient.objects.create(user=self.user, name='Porc meat')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredents lister are belong to the user """
        user2 = get_user_model().objects.create_user(
            email='other.django.test@mailinator.com',
            password='Pass_2020'
        )
        Ingredient.objects.create(user=user2, name='Rice')
        ing = Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ing.name)

    def test_create_ingredient_successful(self):
        """Test creating ingredient succesful"""
        payload = {
            'name': 'Test ingredient'
        }

        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """test creating an invalid ingredient"""
        payload = {
            'name': ''
        }

        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_ingredients_assigned_to_recipe(self):
        """Test filtering ingredients by those assigned to a recipe"""
        ing1 = Ingredient.objects.create(user=self.user, name='Eggs')
        ing2 = Ingredient.objects.create(user=self.user, name='Salt')
        recipe = Recipe.objects.create(
            title='Coriander eggs on toasts',
            time_minutes=10,
            price=5,
            user=self.user
        )
        recipe.ingredients.add(ing1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ing1)
        serializer2 = IngredientSerializer(ing2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_ingredients_assigned_unique(self):
        """Test filter ingred by those assigned to a recipe not duplacated"""
        ing = Ingredient.objects.create(user=self.user, name='Eggs')
        Ingredient.objects.create(user=self.user, name='Salt')
        recipe1 = Recipe.objects.create(
            title='Coriander eggs on toasts',
            time_minutes=10,
            price=3.00,
            user=self.user
        )
        recipe1.ingredients.add(ing)
        recipe2 = Recipe.objects.create(
            title='Omelette',
            time_minutes=10,
            price=2.00,
            user=self.user
        )
        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
