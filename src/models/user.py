from models import Campaign, User_Settings, Character

class User:
    def __init__(self, username: str, number_of_campaigns: int, campaigns: list[Campaign], user_settings: User_Settings,
                 characters: list[Character]):
        self.username = username
        self.number_of_campaigns = number_of_campaigns
        self.campaigns = campaigns
        self.user_settings = user_settings
        self.characters = characters
        
    def create_camp(self) -> None:
        pass
    
    def update_camp(self, c_num: int) -> None:
        pass

    def delete_camp(self, c_num: int) -> None:
        pass