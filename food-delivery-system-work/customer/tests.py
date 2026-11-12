from django.test import TestCase
from django.urls import reverse


class CustomerPageTests(TestCase):

    def test_menu_opens(self):
        response = self.client.get(reverse("customer:menu"))

        self.assertEqual(response.status_code, 200)

    def test_profile_opens(self):
        response = self.client.get(reverse("customer:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer/profile.html")

    def test_favorites_opens(self):
        response = self.client.get(reverse("customer:favorites"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer/favorites.html")

    def test_unknown_page_returns_404(self):
        response = self.client.get("/this-page-does-not-exist/")

        self.assertEqual(response.status_code, 404)