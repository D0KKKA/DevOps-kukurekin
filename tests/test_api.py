import unittest

from fastapi.testclient import TestClient

from app.main import app, reset_catalog


class FoodSurplusApiTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_catalog()
        self.client = TestClient(app)

    def test_root_displays_student_information(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["student"]["name"], "Danil")
        self.assertEqual(response.json()["student"]["student_id"], "37554")

    def test_reservation_reduces_available_quantity(self) -> None:
        response = self.client.post(
            "/offers/bakery-bread-001/reserve", json={"quantity": 3}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["remaining_quantity"], 9)

    def test_reservation_prevents_overselling(self) -> None:
        response = self.client.post(
            "/offers/bakery-bread-001/reserve", json={"quantity": 13}
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "Insufficient available quantity")
