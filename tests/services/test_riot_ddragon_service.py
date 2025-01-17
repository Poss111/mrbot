"""Module for testing the get champion command"""
import os
import sys
from unittest.mock import patch
import pytest
from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.models.riot_ddragon_champions import RiotDDragonChampions
from leaguetracker.services.riot_ddragon_service import RiotDDragonService

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.examples.data import champions_sample_payload, indepth_aatrox_sample_payload_json

latest_version = "14.24.1"
base_url = "https://localhost:8080"

# This method will be used by the mock to replace requests.get
def mocked_test_get_list_of_champions_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if args[1] == f'{base_url}/api/versions.json':
        return MockResponse([latest_version], 200)
    elif args[1] == f"{base_url}/cdn/{latest_version}/data/en_US/champion.json":
        return MockResponse(champions_sample_payload, 200)

    return MockResponse(None, 404)

# This method will be used by the mock to replace requests.get
def mocked_get_list_of_champions_should_return_exception_if_version_passed_is_not_valid_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if args[1] == f'{base_url}/api/versions.json':
        return MockResponse([latest_version], 200)
    elif args[1] == f"{base_url}/cdn/{latest_version}/data/en_US/champion.json":
        return MockResponse(champions_sample_payload, 200)

    return MockResponse(None, 404)

# This method will be used by the mock to replace requests.get
def mocked_test_get_list_of_champions_responds_w_not_200_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if args[1] == f'{base_url}/api/versions.json':
        return MockResponse([latest_version], 200)
    elif args[1] == f"{base_url}/cdn/{latest_version}/data/en_US/champion.json":
        return MockResponse(champions_sample_payload, 404)

    return MockResponse(None, 404)
        
# This method will be used by the mock to replace requests.get
def mocked_test_get_champion_use_latest_version_if_not_provided_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if args[1] == f'{base_url}/api/versions.json':
        return MockResponse([latest_version], 200)
    elif args[1] == f"{base_url}/cdn/{latest_version}/data/en_US/champion/Aatrox.json":
        return MockResponse(indepth_aatrox_sample_payload_json, 200)

    return MockResponse(None, 404)

def mocked_test_get_champion_should_throw_an_exception_if_version_is_not_valid_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if args[1] == f'{base_url}/api/versions.json':
        return MockResponse([latest_version], 200)
    elif args[1] == f"{base_url}/cdn/{latest_version}/data/en_US/champion/Aatrox.json":
        return MockResponse(indepth_aatrox_sample_payload_json, 200)

    return MockResponse(None, 404)

def mocked_test_get_available_versions_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if args[1] == f'{base_url}/api/versions.json':
        return MockResponse([latest_version], 200)

    return MockResponse(None, 404)

def mocked_test_get_available_versions_responds_w_not_200_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            pass

    if args[1] == f'{base_url}/api/versions.json':
        return MockResponse([latest_version], 404)

    return MockResponse(None, 404)

class TestGetListOfChampions:
    """Test class for the get champion command"""

    @pytest.mark.asyncio
    @patch('requests.request', side_effect=mocked_test_get_list_of_champions_request)
    async def test_get_list_of_champions_use_latest_version_if_not_provided(self, mock_request):
        """Test retrieving list of champions from Riots DDragon API"""
        service = RiotDDragonService(base_url)
        service._versions_cache = {
            'data': [latest_version],
            'timestamp': None
        }
        # Execute the ping command
        response = await service.retrieve_champion_list()

        mock_request.assert_any_call(
            "GET",
            f"{base_url}/api/versions.json",
            params=None,
            data=None,
            headers=None,
            timeout=5
        )
        mock_request.assert_any_call(
            "GET",
            f"{base_url}/cdn/{latest_version}/data/en_US/champion.json",
            params=None,
            data=None,
            headers=None,
            timeout=5
        )
        
        # Assert the expected interaction response
        assert response is not None
        assert response == RiotDDragonChampions(**champions_sample_payload)
        
    @pytest.mark.asyncio
    @patch('requests.request', side_effect=mocked_get_list_of_champions_should_return_exception_if_version_passed_is_not_valid_request)
    async def test_get_list_of_champions_should_return_exception_if_version_passed_is_not_valid(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        
        base = "https://localhost:8080"
        service = RiotDDragonService(base)
        version_to_run_with = "14.23.1"
        service._versions_cache = {
            'data': [latest_version, "14.22.1"],
            'timestamp': None
        }
        # Execute the ping command
        try:
            await service.retrieve_champion_list(version_to_run_with)
            assert False, "Should have raised an exception"
        except Exception as e:
            assert str(e) == f"Version {version_to_run_with} is not available from Riot's DDragon API"
        
    @pytest.mark.asyncio
    @patch('requests.request', side_effect=mocked_test_get_list_of_champions_responds_w_not_200_request)
    async def test_get_list_of_champions_responds_w_not_200(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        base = "https://localhost:8080"
        service = RiotDDragonService(base)
        service._versions_cache = {
            'data': [latest_version],
            'timestamp': None
        }
        
        # Execute the ping command
        try:
            response = await service.retrieve_champion_list()
        except Exception as e:
            assert str(e) == "Error sending request to https://localhost:8080/cdn/14.24.1/data/en_US/champion.json: 404"
        
        mock_response.assert_any_call(
            "GET", 
            f"{base}/cdn/{latest_version}/data/en_US/champion.json",
            params=None, 
            data=None, 
            headers=None, 
            timeout=5
        )
    
    class TestGetChampion:
        
        @pytest.mark.asyncio
        @patch('requests.request', side_effect=mocked_test_get_champion_use_latest_version_if_not_provided_request)
        async def test_get_champion_use_latest_version_if_not_provided(self, mock_response):
            """Test retrieving list of champions from Riots DDragon API"""
            base = "https://localhost:8080"
            service = RiotDDragonService(base)
            service._versions_cache = {
                'data': [latest_version],
                'timestamp': None
            }
            # Execute the ping command
            champion_to_search_for = "Aatrox"
            response = await service.retrieve_champion(champion_to_search_for)
            
            mock_response.assert_any_call(
                "GET",
                f"{base}/cdn/{latest_version}/data/en_US/champion/{champion_to_search_for}.json", 
                params=None, 
                data=None, 
                headers=None, 
                timeout=5
            )
            
            # Assert the expected interaction response
            assert response is not None
            assert response == RiotDDragonChampion(**indepth_aatrox_sample_payload_json)
        
        @pytest.mark.asyncio
        @patch('requests.request', side_effect=mocked_test_get_champion_should_throw_an_exception_if_version_is_not_valid_request)
        async def test_get_champion_should_throw_an_exception_if_version_is_not_valid(self, mock_response):
            """Test retrieving list of champions from Riots DDragon API"""
            base = "https://localhost:8080"
            service = RiotDDragonService(base)
            latest_version = "14.24.1"
            service._versions_cache = {
                'data': [latest_version, "14.22.1"],
                'timestamp': None
            }
            # Execute the ping command
            champion_to_search_for = "Aatrox"
            try:
                await service.retrieve_champion(champion_to_search_for, "14.23.1")
                assert False, "Should have raised an exception"
            except Exception as e:
                assert str(e) == f"Version 14.23.1 is not available from Riot's DDragon API"
        
    class TestGetVersion:
        
        @pytest.mark.asyncio
        @patch('requests.request', side_effect=mocked_test_get_available_versions_request)
        async def test_get_available_versions(self, mock_response):
            """Test retrieving list of versions from Riots DDragon API"""
            base = "https://localhost:8080"
            service = RiotDDragonService(base)
            # Execute the ping command
            response = await service.retrieve_available_versions()
            
            mock_response.assert_any_call(
                "GET", 
                f"{base}/api/versions.json",
                params=None,
                data=None,
                headers=None,
                timeout=5
            )
            
            # Assert the expected interaction response
            assert response is not None
            assert response == [latest_version]
            assert service._versions_cache['data'] == [latest_version]
            assert service._versions_cache['timestamp'] is not None
            
        @pytest.mark.asyncio
        @patch('requests.request', side_effect=mocked_test_get_available_versions_responds_w_not_200_request)
        async def test_get_available_versions_responds_w_not_200(self, mock_response):
            """Test retrieving list of versions from Riots DDragon API"""
            base = "https://localhost:8080"
            service = RiotDDragonService(base)
            # Execute the ping command
            try:
                response = await service.retrieve_available_versions()
            except Exception as e:
                assert str(e) == "Error sending request to https://localhost:8080/api/versions.json: 404"
            
            mock_response.assert_any_call(
                "GET", 
                f"{base}/api/versions.json",
                params=None,
                data=None,
                headers=None,
                timeout=5
            )
            
        @pytest.mark.asyncio
        @patch('requests.request', side_effect=mocked_test_get_available_versions_request)
        async def test_get_available_versions_cache_response_if_cached(self, mock_response):
            """Test retrieving list of versions from Riots DDragon API"""
            base = "https://localhost:8080"
            service = RiotDDragonService(base)
            # Execute the ping command
            response = await service.retrieve_available_versions()
            response = await service.retrieve_available_versions()
            
            mock_response.assert_called_once_with(
                "GET", 
                f"{base}/api/versions.json",
                params=None,
                data=None,
                headers=None,
                timeout=5
            )
            
            # Assert the expected interaction response
            assert response is not None
            assert response == [latest_version]