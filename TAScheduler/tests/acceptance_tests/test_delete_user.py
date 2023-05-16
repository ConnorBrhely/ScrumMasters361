from TAScheduler.models import UserAccount
from django.test import TestCase, Client


class TestDeleteUser(TestCase):

    def setUp(self):
        self.monkey = Client()
        self.monkey.post("/login/", {
            "password": "Password123!",
            "email": "test@uwm.edu"
        }, follow=True)
        self.account = UserAccount.objects.register(
            first_name="Test",
            last_name="Account",
            email="newtest@uwm.edu",
            password="Password123!",
            user_type="INSTRUCTOR")

    def test_successfulDelete(self):
        self.assertEqual(2, UserAccount.objects.count(), msg="Are not two objects before deletetion")
        resp = self.monkey.post(f"/delete_user?username={self.account.user.username}", {
            "confirmdelete": "newtest@uwm.edu",
            "editaccount": "newtest@uwm.edu"
        }, follow=True)
        self.assertEqual(1, UserAccount.objects.count(), msg="User not deleted")

    def test_uncheckedDelete(self):
        self.assertEqual(2, UserAccount.objects.count(), msg="Are not two objects before attempted deletion")
        resp = self.monkey.post(f"/delete_user?username={self.account.user.username}", {
            "confirmdelete": "donotdelete",
            "editaccount": "newtest@uwm.com"
        }, follow=True)
        self.assertEqual(2, UserAccount.objects.count(),
                         msg="Should be two accounts when box is not checked (no deletetion should occur)")
