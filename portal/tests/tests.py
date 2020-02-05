from django.test import TestCase, RequestFactory
from unittest.case import skip
from rest_framework import status
import portal.views as my_view

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

  @skip("implement")
  def test_view_resources_logged(self):
    pass

  @skip("implement")
  def test_view_resources_no_logged(self):
    pass

  @skip("implement")
  def test_view_retrieve_athenticated(self):
    pass

  @skip("implement")
  def test_view_retrieve_no_authenticated(self):
    pass

  @skip("implement")
  def test_view_retrieve_frontend(self):
    pass

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
