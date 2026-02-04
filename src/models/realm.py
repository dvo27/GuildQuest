from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import User

@dataclass
class Realm:
    name: str
    map_id: int
    time_rule: int
    selected_user: 'User'
    desc: str = "N/A"
        
    def set_desc(self, text: str) -> None:
        self.desc = text
    
    def change_name(self, text: str) -> None:
        self.name = text
        
    def change_time_rule(self, time: int) -> None:
        self.time_rule = time