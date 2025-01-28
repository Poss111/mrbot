from appconfig_helper import AppConfigHelper
from leaguetracker.configs.app_configs import AppConfigs
import boto3

class AWSAppConfigs(AppConfigs):
    
    def __init__(self):
        super(AWSAppConfigs, self).__init__()
        print("Loading configurations from AWS AppConfig.")
        self.client = boto3.client('appconfig')
        self.application_id = 'mrbot'
        self.environment_id = 'prod'
        self.configuration_id = 'mrbot'
        self.client = AppConfigHelper(
            appconfig_application=self.application_id,
            appconfig_environment=self.environment_id,
            appconfig_profile=self.configuration_id,
            max_config_age=45
        )
    
    def get_footer_msg(self):
        return self.client.config['footer_msg']
    
    def get_author(self):
        return self.client.config['author']
    
    def get_guild_id(self):
        return self.client.config['discord_guild_id']
    
    def get_app_version(self):
        return self.client.config['app_version']
        