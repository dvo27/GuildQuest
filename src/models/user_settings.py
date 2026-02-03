from models import Realm
from dataclasses import dataclass

@dataclass
class User_Settings:
    time_display: str
    switch_time: bool
    current_realm: Realm
    
    def set_display(self, s:str) -> None:
        pass
    
    def set_theme(self) -> None:
        pass
    
    def set_curr_theme(self, r: Realm) -> None:
        pass