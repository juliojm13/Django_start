from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command
from django.conf import settings


class TestUserManagement(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('fill_db')
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser('django1', 'test@tt.com', 'superuser')
        self.user = ShopUser.objects.create_user('nodjango', 'test2@tt.com', 'nosuperuser')
        self.user_with_first_name = ShopUser.objects.create_user('justuser', 'jme@tt.com', 'justme',
                                                                 first_name='Justme')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username='django1', password='superuser')

        # login
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)
        self.assertEqual(response.context['title'], 'вход')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.superuser)

    def test_cart_login_redirect(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.url, '/auth/login/?next=/cart/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='django1', password='superuser')

        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['cart']), [])
        self.assertEqual(response.request['PATH_INFO'], '/cart/')

    def test_user_logout(self):
        self.client.login(username='django1', password='superuser')

        # login
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['user'].is_anonymous)

        # logout
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '21',
            'city': 'Москва'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        new_user = ShopUser.objects.get(username=new_user_data['username'])
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        # данные нового пользователя
        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertContains(response, text=new_user_data['first_name'], status_code=200)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '15',
            'city': 'Москва'}
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды!')

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'cartapp')
