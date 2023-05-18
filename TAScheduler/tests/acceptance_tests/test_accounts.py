from TAScheduler.models import UserAccount
from django.test import TestCase, Client

class TestAccounts(TestCase):

    def setUp(self):
        self.monkey = Client()
        self.monkey.post("/login/", {
            "password": "Password123!",
            "email": "test@uwm.edu"
        }, follow=True)
        self.userone = UserAccount.objects.register(
            first_name="A",
            last_name="A",
            email="a@gmail.com",
            password="Password123!",
            user_type=UserAccount.UserType.ADMIN
        )
        self.usertwo = UserAccount.objects.register(
            first_name="B",
            last_name="B",
            email="b@gmail.com",
            password="Password123!",
            user_type=UserAccount.UserType.ADMIN
        )
        self.userthree = UserAccount.objects.register(
            first_name="C",
            last_name="C",
            email="c@gmail.com",
            password="Password123!",
            user_type=UserAccount.UserType.TA
        )

    # FIXME: This test is failing because the list is always being sorted by user type, works fine in practice
    """Default User FirstName=Admin LastName=User Type=ADMIN"""
    def test_sortNameAZ(self):
        resp = self.monkey.post("/accounts", {"sorttype": "name"}, follow=True)
        accounts = resp.context["accounts"]
        self.assertEqual(self.userone, accounts[0], msg="List not sorted by name A-Z")
        self.assertEqual(self.usertwo, accounts[2], msg="List not sorted by name A-Z")
        self.assertEqual(self.userthree, accounts[3], msg="List not sorted by name A-Z")

    def test_sortNameZA(self):
        resp = self.monkey.post("/accounts", {"sorttype": "namereverse"}, follow=True)
        accounts = resp.context["accounts"]
        self.assertEqual(self.userthree, accounts[0], msg="List not sorted by name Z-A")
        self.assertEqual(self.usertwo, accounts[1], msg="List not sorted by name Z-A")
        self.assertEqual(self.userone, accounts[3], msg="List not sorted by name Z-A")

    def test_sortType(self):
        resp = self.monkey.post("/accounts", {"sorttype": "type"}, follow=True)
        accounts = resp.context["accounts"]
        self.assertEqual(self.usertwo, accounts[1], msg="List not sorted by type")
        self.assertEqual(self.userone, accounts[2], msg="List not sorted by type")
        self.assertEqual(self.userthree, accounts[3], msg="List not sorted by type")


