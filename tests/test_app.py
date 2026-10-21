import unittest
from app import app, shortest_path, prim_mst, BUILDINGS

class CampusAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    def test_health(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)
    def test_buildings_count(self):
        self.assertEqual(len(self.client.get("/api/buildings").get_json()), 16)
    def test_same_node_path(self):
        self.assertEqual(shortest_path(0, 0)["distance"], 0)
    def test_shortest_path_api(self):
        response = self.client.get("/api/shortest-path?source=0&destination=15")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.get_json()["distance"], 0)
    def test_invalid_index(self):
        self.assertEqual(self.client.get("/api/shortest-path?source=99&destination=1").status_code, 400)
    def test_mst_edges(self):
        result = prim_mst()
        self.assertTrue(result["connected"])
        self.assertEqual(len(result["edges"]), len(BUILDINGS) - 1)

if __name__ == "__main__":
    unittest.main()
