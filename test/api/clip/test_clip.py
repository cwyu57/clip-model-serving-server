class TestClipSearch:
    """Integration tests for /clip/search endpoint."""

    def test_search_success(self, client):
        # TODO: fix this testcase
        """Test that /clip/search returns 200 status code."""
        response = client.post("/clip/search", json={"query": "cat"})
        assert response.status_code == 200
