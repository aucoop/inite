from portal import models
import random, string

class Seeder:

  @staticmethod
  def create_fake_registry(IP='127.0.0.1'):
    return models.Registre.objects.create(ip=IP)
 
  @staticmethod
  def generate_random_string(size=5, chars=string.ascii_uppercase+string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

  @staticmethod
  def generate_random_number(minim=4, maxim=90):
    return random.randint(minim, maxim)

  @staticmethod
  def generate_fake_user():
    return { 'fname': generate_random_string(), 
             'lname': generate_random_string(), 
             'lloc_r': generate_random_string(), 
             'sexe': generate_random_string(), 
             'email': generate_random_string(), 
             'edat': generate_random_number(),
             'policy': 'on' }
        
