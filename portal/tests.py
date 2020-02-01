from django.test import TestCase, RequestFactory
from rest_framework import status
import portal.views as my_view


# Create your tests here.

class loginViewTest(TestCase):

  def setUP(self):
    self.factory = RequestFactory()

  def test_view_login_returns_200_if_not_logged(self):
    response = self.client.get('/login')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.asserTemplateUsed(response, '/login.html')

  def test_view_resources_redirects_if_logged(self):
    response = self.client.get('/resources')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.asserTemplateUsed(response, '/login.html')
  #def test_view_resources_redirects_if_logged(self):
  #def test_view_resources_redirects_if_logged(self):
  #def test_view_resources_redirects_if_logged(self):
