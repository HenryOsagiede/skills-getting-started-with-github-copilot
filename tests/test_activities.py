"""Tests for GET /activities endpoint"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all 9 activities with correct structure.
        
        Arrange: TestClient and expected activity count
        Act: Make GET request to /activities
        Assert: Response status is 200 and all 9 activities are returned with correct fields
        """
        # Arrange
        expected_activity_count = 9
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        
        # Verify each activity has the required fields
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
    
    def test_get_activities_response_structure(self, client, valid_activity_names):
        """
        Test that GET /activities returns all activities with expected names.
        
        Arrange: TestClient and list of expected activity names
        Act: Make GET request to /activities
        Assert: All expected activity names are in the response
        """
        # Arrange
        expected_activities = set(valid_activity_names)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        returned_activities = set(response.json().keys())
        assert returned_activities == expected_activities
    
    def test_get_activities_participants_is_list(self, client):
        """
        Test that participants field is a list of strings (emails).
        
        Arrange: TestClient
        Act: Make GET request to /activities
        Assert: All participants are strings (email addresses)
        """
        # Arrange/Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        
        for activity_data in activities.values():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email format check
