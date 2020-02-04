from portal import models

class Seeder:

  @staticmethod
  def create_fake_registry(IP='127.0.0.1'):
    return models.Registre.objects.create(ip=IP)
