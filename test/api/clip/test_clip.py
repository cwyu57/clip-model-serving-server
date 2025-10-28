from urllib.parse import quote


class TestClipSearch:
    """Integration tests for /clip/search endpoint."""

    def test_search_success(self, client):
        """Test that /clip/search returns 200 status code."""
        response = client.post("/clip/search?query=cat")
        assert response.status_code == 200
