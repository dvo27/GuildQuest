from dataclasses import dataclass
from .Realm import Realm

@dataclass
class User_Settings:
    time_display: str = '12hr'
    switch_theme: bool = False
    current_realm: Realm = None

    def set_display(self, s:str) -> None:
        self.time_display = s

    def set_theme(self) -> None:
        pass
    
    def set_curr_realm(self, r: Realm) -> None:
        pass