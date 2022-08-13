from django.test import TestCase
from .models import Profile
from django.shortcuts import reverse

class LibraryTestCase(TestCase):
  def test_dashboard(self):
    Profile.objects.create_user("test11","user11@gmail.com","MugoYA23?")
    self.client.login(username='test11', password='MugoYA23?')
    response=self.client.get('/dashbord')
    self.assertEqual(response.status_code, 200)
  
