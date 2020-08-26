from django.conf import settings
from django.test import TestCase, RequestFactory

from portal import models
from portal import public_views
from portal.tests.test_utils import Seeder

from rest_framework import status
from unittest.case import skip
import base64


# Create your tests here.

class PublicResources(TestCase):

  def setUP(self):
    self.factory = RequestFactory()

  def test_registration_GETNotRegistered_200(self):
    response = self.client.get('/registration')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTemplateUsed(response, 'registration.html')

  def test_registration_GETRegistered_302(self):
    self.registry  = Seeder.create_fake_registry()
    response = self.client.get('/registration', REMOTE_ADDR=self.registry.ip)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)

  @skip("implement")
  def test_view_login_POST_not_logged(self):
    obj = Seeder.generate_fake_user()
    response = self.client.post('/registration', obj, format='json')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertTemplateNotUsed(response, 'registration.html')
    self.assertRedirects(response, '/resources')
    u = models.Usuari.objects.get(nom=obj['fname'],
                                  cognom=obj['lname'],
                                  edat=obj['edat'],
                                  resideix_a=obj['lloc_r'],
                                  sexe=obj['sexe'],
                                  email=obj['email'])
  
  @skip("implement")
  def test_view_resources_no_logged(self):
    response = self.client.get('/resources')
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertTemplateNotUsed(response, 'resources.html')
    self.assertRedirects(response, '/registration')

  @skip("implement")
  def test_canvi_de_password_retrieve(self):
    vell = settings.BASICAUTH_USERS
    nou = {'test':'test'}
    data =  {'user':'test', 'passwd':'test'}
    username =list(vell.keys())[0]
    password = vell[username]
    auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + str(base64.b64encode(('%s:%s' % (username,password)).encode('utf-8')), "utf-8"), 
    }
    response = self.client.post('/chpasswd',data, **auth_headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(settings.BASICAUTH_USERS,nou)
    data = {'user':username, 'passwd': password}
    auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + str(base64.b64encode(('%s:%s' % (username,password)).encode('utf-8')), "utf-8"), 
    }
    response = self.client.post('/chpasswd',data)
    self.assertEqual(settings.BASICAUTH_USERS,vell)
    

  @skip("implement")
  def test_view_retrieve_no_athenticated(self):
    auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + str(base64.b64encode('frewfrewfre:frewfrew'.encode('utf-8'))), 
    }
    c = self.client
    response = c.get('/retrieve', **auth_headers)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  @skip("implement")
  def test_view_retrieve_authenticated(self):
    username =list( settings.BASICAUTH_USERS.keys())[0]
    password = settings.BASICAUTH_USERS[username]
    auth_headers = {
    'HTTP_AUTHORIZATION': 'Basic ' + str(base64.b64encode(('%s:%s' % (username,password)).encode('utf-8')), "utf-8"), 
    }
    c = self.client
    response = c.get('/retrieve', **auth_headers)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  @skip("implement")
  def test_view_retrieve_frontend(self):
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

  @skip("implement")
  def test_view_login_redirect_if_logged(self):
    self.ip = Seeder.create_fake_registry().ip
    response = self.client.get('/registration',REMOTE_ADDR=self.ip)
    self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    self.assertTemplateNotUsed(response, 'registration.html')
    self.assertRedirects(response, '/resources')
