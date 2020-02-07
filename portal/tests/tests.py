from django.test import TestCase, RequestFactory
from unittest.case import skip
from rest_framework import status
import portal.views as my_view
from django.conf import settings
import base64
from portal import models
from portal.tests.test_utils import Seeder


# Create your tests here.

class loginViewTest(TestCase):

  def setUP(self):
    self.factory = RequestFactory()

  def test_view_login_returns_200_if_not_logged(self):
    response = self.client.get('/login')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'login.html')

  def test_view_login_302_redirect_if_logged(self):
    self.ip = Seeder.create_fake_registry().ip
    response = self.client.get('/login',REMOTE_ADDR=self.ip)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertTemplateNotUsed(response, 'login.html')
    self.assertRedirects(response, '/resources')

  @skip("implement")
  def test_view_login_POST_not_logged(self):
    obj = Seeder.generate_fake_user()
    response = self.client.post('/login', obj, format='json')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertTemplateNotUsed(response, 'login.html')
    self.assertRedirects(response, '/resources')
    u = models.Usuari.objects.get(nom=obj['fname'], cognom=obj['lname'], edat=obj['edat'], resideix_a=obj['lloc_r'], nascut_a=obj['lloc_n'], email=obj['email'])
  
  @skip("implement")
  def test_view_login_POST_logged(self):
    pass
  
  @skip("implement")
  def test_home_redirect_login_logged(self):
    pass

  @skip("implement")
  def test_home_redirect_login_no_logged(self):
    pass

  def test_view_resources_logged(self):
    self.ip = Seeder.create_fake_registry().ip
    response = self.client.get('/resources',REMOTE_ADDR=self.ip)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_view_resources_no_logged(self):
    response = self.client.get('/resources')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertTemplateNotUsed(response, 'resources.html')
    self.assertRedirects(response, '/login')


  def test_view_retrieve_no_athenticated(self):
    response = self.client.get('/retrieve')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  @skip("implement")
  def test_view_retrieve_authenticated(self):
    pass
    username =
    password = settings.BASICAUTH_USERS[username]
    auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + str(base64.b64encode(('%s:%s' % (username,password)).encode('utf-8')), "utf-8"), 
    }
    c = self.client
    response = c.get('/retrieve', **auth_headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_view_statistics_200_OK(self):
    response = self.client.get('/statistics')
    auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + str(base64.b64encode(('%s:%s' % (username,password)).encode('utf-8')), "utf-8"), 
    }
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'statistics.html')

  @skip("implement")
  def test_proxy_wikipedia(self):
    pass

  @skip("implement")
  def test_proxy_moodle(self):
    pass

  @skip("implement")
  def test_proxy_khanacademy(self):
    pass

