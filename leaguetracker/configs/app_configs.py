from abc import ABC, abstractmethod

class AppConfigs(ABC):
    """An interface for Mr Bot's application configurations."""
    
    @abstractmethod
    def get_footer_msg(self):
        """Returns the footer message for the embeds."""
        pass
    
    @abstractmethod
    def get_author(self):
        """Returns the author for the embeds."""
        pass
    
    @abstractmethod
    def get_guild_id(self):
        """Returns the guild id."""
        pass