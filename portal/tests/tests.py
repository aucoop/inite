from django.test import TestCase, RequestFactory
from unittest.case import skip
from rest_framework import status
import portal.views as my_view
from django.conf import settings

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

  @skip("implement")
  def test_view_login_POST_not_logged(self):
    pass
  
  @skip("implement")
  def test_view_login_POST_logged(self):
    pass
  
  @skip("implement")
  def test_home_redirect_login_logged(self):
    pass

  @skip("implement")
  def test_home_redirect_login_no_logged(self):
    pass

  @skip("implement")
  def test_view_resources_logged(self):
    pass

  @skip("implement")
  def test_view_resources_no_logged(self):
    pass

  @skip("implement")
  def test_view_retrieve_no_athenticated(self):
    username = settings.BASICAUTH_USERS.keys()[0]
    password = setting.BASICAUTH_USERS[username]
    auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('frewfrewfre:frewfrew'), 
    }
    c = self.client
    response = c.get('/retrieve', **auth_headers)
    self.assertEqual(response.status_code, status.HTTP_)

  @skip("implement")
  def test_view_retrieve_authenticated(self):
    username = settings.BASICAUTH_USERS.keys()[0]
    password = setting.BASICAUTH_USERS[username]
    auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('%s:%s' % (username,password) ), 
    }
    c = self.client
    response = c.get('/retrieve', **auth_headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)


  @skip("implement")
  def test_view_retrieve_frontend(self):
    response = self.client.get('/statistics')
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

  def test_view_login_redirect_if_logged(self):
    self.ip = Seeder.create_fake_registry().ip
    response = self.client.get('/login',REMOTE_ADDR=self.ip)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertTemplateNotUsed(response, 'login.html')
    self.assertRedirects(response, '/resources')
