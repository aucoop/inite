from portal import models

class Seeder:

  @staticmethod
  def create_fake_registry(IP='666'):
    return models.Registre.objects.create(ip=IP)
