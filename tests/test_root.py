"""Tests for GET / (root) endpoint"""


class TestRootEndpoint:
    """Tests for the GET / endpoint"""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html.
        
        Arrange: TestClient
        Act: Make GET request to / with allow_redirects=False
        Assert: Response status is 307 (Temporary Redirect) and Location header points to /static/index.html
        """
        # Arrange/Act
        response = client.get("/", allow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
    
    def test_root_redirect_follows_to_static(self, client):
        """
        Test that following the redirect from GET / leads to the static index.html.
        
        Arrange: TestClient
        Act: Make GET request to / with allow_redirects=True (default)
        Assert: Response status is 200 and content contains HTML
        """
        # Arrange/Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        # Check that we get HTML content (basic check)
        content = response.text.lower()
        assert "html" in content or "<!doctype" in content or "head" in content
