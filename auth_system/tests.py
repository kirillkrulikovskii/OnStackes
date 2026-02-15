from django.test import TestCase
from django.contrib.auth import get_user_model; User = get_user_model()
from django.utils import timezone

class AccountTest(TestCase):
    def setUp(self) -> None:
        a1 = User.objects.create(
            username="AccountTest1", password="12345678",
            date_birth=timezone.now().date() 
        )
        a2 = User.objects.create(
            username="AccountTest2", password="12345678",
            date_birth=timezone.datetime(2009, 10, 21).date() 
        )
        a3 = User.objects.create(
            username="AccountTest3", password="12345678",
            date_birth=timezone.datetime(2000, 2, 15).date() 
        )
        self.accounts = [
            a1,a2,a3
        ]



"""
Now timezone is 2/12/2026
AccountTest1 is 0 years old  Today is 2/12/2026
AccountTest2 is 16 years old date of birth is 10/21/2009
AccountTest2 is 25 years old date of birth is 2/15/2000

"""
