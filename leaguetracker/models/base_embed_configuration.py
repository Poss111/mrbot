from pydantic import BaseModel


class BaseEmbedConfiguration:
    footer: str
    author: str
    
    def __init__(self, footer: str, author: str):
        self.footer = footer
        self.author = author