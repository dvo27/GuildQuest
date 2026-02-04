from dataclasses import dataclass
from .Realm import Realm

@dataclass
class User_Settings:
    time_display: str = '12hr'  # make time_display into enum ('12hr' and '24hr')
    switch_time: bool = False
    current_realm: Realm = None

    def set_display(self, s:str) -> None:
        # if s not in valid displays throw error

        self.time_display = s

    def set_theme(self) -> None:
        pass
    
    def set_curr_theme(self, r: Realm) -> None:
        pass