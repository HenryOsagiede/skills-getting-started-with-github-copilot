"""Tests for signup/unregister endpoints (POST and DELETE /activities/{activity_name}/signup)"""

import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, sample_email, valid_activity_names):
        """
        Test successful signup for an activity.
        
        Arrange: TestClient, test email, valid activity name
        Act: Make POST request to /activities/{activity}/signup?email={email}
        Assert: Response status is 200 and confirmation message is returned
        """
        # Arrange
        activity = valid_activity_names[0]  # Use first activity (Chess Club)
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert activity in data["message"]
    
    def test_signup_invalid_activity(self, client, sample_email):
        """
        Test signup fails for non-existent activity.
        
        Arrange: TestClient, test email, invalid activity name
        Act: Make POST request to non-existent activity
        Assert: Response status is 404 (Not Found)
        """
        # Arrange
        invalid_activity = "Non-Existent Club"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_signup_duplicate_registration(self, client, sample_email, valid_activity_names):
        """
        Test signup fails when student is already registered.
        
        Arrange: TestClient, valid activity that already has participants
        Act: First signup succeeds, second signup with same email fails
        Assert: First response is 200, second response is 400 with error message
        """
        # Arrange
        activity = valid_activity_names[0]
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        
        # Act - Duplicate signup
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        data = response2.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""
    
    def test_unregister_success(self, client, sample_email, valid_activity_names):
        """
        Test successful unregister from an activity.
        
        Arrange: TestClient, test email, student already signed up
        Act: Make DELETE request to /activities/{activity}/signup?email={email}
        Assert: Response status is 200 and confirmation message is returned
        """
        # Arrange
        activity = valid_activity_names[0]
        
        # First sign up
        client.post(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        
        # Act - Unregister
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
    
    def test_unregister_invalid_activity(self, client, sample_email):
        """
        Test unregister fails for non-existent activity.
        
        Arrange: TestClient, test email, invalid activity name
        Act: Make DELETE request to non-existent activity
        Assert: Response status is 404 (Not Found)
        """
        # Arrange
        invalid_activity = "Non-Existent Club"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_unregister_not_registered(self, client, sample_email, valid_activity_names):
        """
        Test unregister fails when student is not registered.
        
        Arrange: TestClient, valid activity, email that was never registered
        Act: Make DELETE request
        Assert: Response status is 400 with error message
        """
        # Arrange
        activity = valid_activity_names[0]
        unregistered_email = "never.registered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": unregistered_email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"]


class TestSignupUnregisterFlow:
    """Integration tests for signup and unregister flows"""
    
    def test_signup_and_unregister_roundtrip(self, client, sample_email, valid_activity_names):
        """
        Test complete flow: signup, verify registration, then unregister.
        
        Arrange: TestClient, test email, valid activity
        Act: 
            1. Sign up for activity
            2. Get activities and verify participant count increased
            3. Unregister from activity
            4. Get activities and verify participant count decreased
        Assert: All operations successful and participant count changes as expected
        """
        # Arrange
        activity = valid_activity_names[0]
        
        # Act 1 - Get initial participant count
        response_initial = client.get("/activities")
        initial_count = len(response_initial.json()[activity]["participants"])
        
        # Act 2 - Sign up
        response_signup = client.post(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        
        # Act 3 - Get activities and verify count increased
        response_after_signup = client.get("/activities")
        after_signup_count = len(response_after_signup.json()[activity]["participants"])
        
        # Act 4 - Unregister
        response_unregister = client.delete(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        
        # Act 5 - Get activities and verify count decreased
        response_after_unregister = client.get("/activities")
        after_unregister_count = len(response_after_unregister.json()[activity]["participants"])
        
        # Assert
        assert response_signup.status_code == 200
        assert response_unregister.status_code == 200
        assert after_signup_count == initial_count + 1
        assert after_unregister_count == initial_count
        assert sample_email in response_after_signup.json()[activity]["participants"]
        assert sample_email not in response_after_unregister.json()[activity]["participants"]
    
    def test_signup_multiple_activities(self, client, sample_email, valid_activity_names):
        """
        Test that a student can sign up for multiple activities.
        
        Arrange: TestClient, test email, multiple activity names
        Act: Sign up for first 3 activities
        Assert: All signups successful and participant lists updated correctly
        """
        # Arrange
        activities_to_join = valid_activity_names[:3]
        
        # Act & Assert
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": sample_email}
            )
            assert response.status_code == 200
        
        # Verify student is in all activities
        response = client.get("/activities")
        for activity in activities_to_join:
            assert sample_email in response.json()[activity]["participants"]
