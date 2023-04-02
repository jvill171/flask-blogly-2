from unittest import TestCase

from app import app
from models import db, User, DEFAULT_IMAGE_URL

# Use a test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Generate real errors rather than HTML error pages
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskTests(TestCase):
    '''Test flask app's routes'''

    def setUp(self):
        '''Add sample user'''

        User.query.delete()

        user = User(first_name='Ftest', last_name='Ltest')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        '''Clean up any transactions'''
        db.session.rollback()

    def test_users_page(self):
        '''Test /user route content'''
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Ftest Ltest', html)

    def test_newUser(self):
        '''Test /user/new route content, through GET method'''
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a user', html)

    def test_do_newUser(self):
        '''Test /user/new route content, through POST method'''
        with app.test_client() as client:
            d = {'first':'Fnew', 'last':'Lnew', 'image':f'DEFAULT_IMAGE_URL'}

            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fnew Lnew', html)

    def test_userDetails(self):
        '''Test /users/<int:user_id> route content'''
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(DEFAULT_IMAGE_URL, html)
            self.assertIn('Ftest Ltest', html)

    def test_editUser(self):
        '''Test /users/<int:user_id>/edit route content, through GET method'''
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input type="text" class="form-control" name="first" value="Ftest">', html)
            self.assertIn('<input type="text" class="form-control" name="last" value="Ltest">', html)
            self.assertIn(f'<input type="text" class="form-control" name="image" value="{DEFAULT_IMAGE_URL}">', html)
            
    def test_do_editUser(self):
        '''Test /users/<int:user_id>/edit route content, through POST method'''
        with app.test_client() as client:
            d = {'first':'Fedit', 'last':'Ledit', 'image':f'DEFAULT_IMAGE_URL'}

            resp = client.post(f'/users/{self.user_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fedit Ledit', html)

    def test_do_deleteUser(self):
        '''Test /users/<int:user_id>/delete route content, through POST method'''
        with app.test_client() as client:

            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            # Check that the Users page has loaded, but no user exists in the displayed list
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)
            self.assertIn('<ul>', html)
            self.assertNotIn('<li>', html)