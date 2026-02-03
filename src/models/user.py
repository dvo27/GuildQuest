from models import Campaign, User_Settings, Character, Realm, Quest_Event
from core import Game_Time


class User:
    def __init__(self, username: str,
                 number_of_campaigns: int,
                 user_settings: User_Settings,
                 campaigns: list[Campaign] = None,
                 characters: list[Character] = None):

        self.username = username
        self.number_of_campaigns = number_of_campaigns if number_of_campaigns is not None else len(campaigns)
        self.user_settings = user_settings
        self.campaigns = campaigns if campaigns is not None else []
        self.characters = characters if characters is not None else []

    def create_camp(self, c_name: str,
                    activity: bool,
                    time: Game_Time,
                    realm: Realm,
                    events_display: str,
                    quests: list[Quest_Event],
                    permitted_users: list, # should be list of users and same for edit_users
                    edit_users: list) -> None:

        # do we need quests, perm_users, and edit users here if they are default to None?
        new_camp = Campaign(c_name, activity, time, realm, events_display, quests, permitted_users, edit_users)
        
        self.campaigns.append(new_camp)


    def update_camp(self, c_num: int, name: str, change_act_status: bool) -> None:
        if c_num < 0 or c_num >= len(self.campaigns):
            raise IndexError("Quest index out of range")

        camp = self.campaigns[c_num]

        if name is not None:
            camp.rename(name)

        if not change_act_status:
            camp.change_act()

    def delete_camp(self, c_num: int) -> None:
        if c_num < 0 or c_num >= len(self.campaigns):
            raise IndexError("Quest index out of range")

        self.campaigns.pop(c_num)
