"""Service class for interacting with Riot's DDragon API"""
from datetime import datetime
import requests
import structlog

from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.models.riot_ddragon_champions import RiotDDragonChampions

class RiotDDragonService:
    """Service class for interacting with Riot's DDragon API"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self._versions_cache = {
            'data': None,
            'timestamp': None
        }

    def _send_request(self, endpoint, method="GET", params=None, data=None, headers=None):
        """Send a request to the Riot DDragon API"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.request(method, url, params=params, data=data, headers=headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_error:
            raise requests.exceptions.RequestException(f"Error sending request to {url}: {http_error}") from http_error
        except Exception as e:
            raise requests.exceptions.RequestException(f"Error processing response from {url}: {e}") from e

    async def retrieve_champion_list(self, riot_ddragon_version=None) -> RiotDDragonChampions:
        """Retrieve a list of champions from Riot's DDragon API"""
        await self.retrieve_available_versions()
        version = self._versions_cache.get('data')[0]
        if riot_ddragon_version is not None:
            if riot_ddragon_version not in self._versions_cache.get('data'):
                raise ValueError(f"Version {riot_ddragon_version} is not available from Riot's DDragon API")
            version = riot_ddragon_version
        log = structlog.get_logger()
        log.info(f"Retrieving champion list from Riot's DDragon API for version {version}...")
        json = self._send_request(f"cdn/{version}/data/en_US/champion.json")
        return RiotDDragonChampions(**json)
    
    async def retrieve_champion(self, champion_id: str, riot_ddragon_version=None) -> RiotDDragonChampion:
        """Retrieve a champion from Riot's DDragon API"""
        await self.retrieve_available_versions()
        version = self._versions_cache.get('data')[0]
        if riot_ddragon_version is not None:
            if riot_ddragon_version not in self._versions_cache.get('data'):
                raise ValueError(f"Version {riot_ddragon_version} is not available from Riot's DDragon API")
            version = riot_ddragon_version
        log = structlog.get_logger()
        log.info(f"Retrieving champion {champion_id} from Riot's DDragon API for version {version}...")
        json = self._send_request(f"cdn/{version}/data/en_US/champion/{champion_id}.json")
        return RiotDDragonChampion(**json)
    
    async def retrieve_available_versions(self) -> list:
        """Retrieve a list of available versions from Riot's DDragon API"""
        if self._versions_cache['timestamp'] is None or (datetime.now() - self._versions_cache['timestamp']).days > 10:
            versions = self._send_request("api/versions.json")
            self._versions_cache = {
                'data': versions,
                'timestamp': datetime.now()
            }
        return self._versions_cache['data']
    
