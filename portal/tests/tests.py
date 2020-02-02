from django.test import TestCase, RequestFactory
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

  def test_view_login_redirect_if_logged(self):
    self.ip = Seeder.create_fake_registry().ip
    response = self.client.get('/login',REMOTE_ADDR=self.ip)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertTemplateUsed(response, 'index.html')
