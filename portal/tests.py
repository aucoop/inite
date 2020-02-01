from django.test import TestCase, RequestFactory
import portal.views as my_view

# Create your tests here.

class loginViewTest(TestCase):

  def setUP(self):
    self.factory = RequestFactory()

  def test_view_login_returns_200_if_not_logged():
    response = self.client.get('/loggin/'

  def test_view_login_redirects_if_logged():
