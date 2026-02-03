from typing import Optional
from core import Game_Time
from .Realm import Realm
from .User import User
from .Quest_Event import Quest_Event


class Campaign:
    def __init__(self,
                 title: str,
                 activity: bool,
                 time: Game_Time,
                 c_realm: Realm,
                 events_display: str,
                 quests: list[Quest_Event] = None,
                 permitted_users: list[User] = None,
                 edit_users: list[User] = None
                 ):
        self.title = title
        self.activity = activity
        self.time = time
        self.c_realm = c_realm
        self.events_display = events_display
        self.quests = quests if quests is not None else []
        self.permitted_users = permitted_users if permitted_users is not None else []
        self.edit_users = edit_users if edit_users is not None else []

    def start_campaign(self) -> None:
        """ 
        Starts the campaign by setting the activity status to True
        """
        self.activity = True

    def rename(self, name: str) -> None:
        """
        Renames the campaign based on the given new name

        Args:
            name (str): New name to rename campaign
        """
        self.title = name

    def change_act(self) -> None:
        """
        Changes the activity status to the opposite state.
        """
        self.activity = not self.activity

    def delete_camp(self) -> None:
        """
        Deletes the campaign.
        """
        # handle fr after storage implementation
        self.activity = False
        self.quests.clear()
        self.permitted_users.clear()
        self.edit_users.clear()

    def change_camp_realm(self, cho_realm: Realm) -> None:
        """
        Changes the current realm of the campaign.

        Args:
            cho_realm (Realm): New realm to change current realm to.
        """
        self.c_realm = cho_realm

    def create_quest(self, name: str, 
                     time: Game_Time, 
                     ch_realm: Realm, 
                     start_time: str, 
                     end_time: str = "N/A") -> Quest_Event:
        
        """
        Creates a new quest object to add to a Campaign's list of quests

        Returns:
            Quest_Event: Quest_Event object we created
        """
        
        q = Quest_Event(name, ch_realm, time, start_time, end_time)
        self.quests.append(q)
        return q

    def update_quest(self, q_num: int, *, name: Optional[str] = None, start_time: Optional[str] = None, realm: Optional[Realm] = None) -> None:
        """
        Updates a quest's info based on the given optional keyword arguments

        Args:
            q_num (int): Quest index 
            realm (Optional[Realm]): New Realm to change quest to. Defaults to None.
            name (Optional[str], optional): New quest name to rename. Defaults to None.
            start_time (Optional[str], optional): New start time for the quest. Defaults to None.
        """
        # q_num is an index for now; later replace with quest_id
        if q_num < 0 or q_num >= len(self.quests):
            raise IndexError("Quest index out of range")
        
        quest = self.quests[q_num]
        
        if name is not None:
            quest.set_name(name)
            
        if start_time is not None:
            quest.set_starttime(start_time)
            
        if realm is not None:
            quest.set_realm(realm)

    def delete_quest(self, q_num: int) -> None:
        """
        Removes a Quest_Event from a Campaign's quests list

        Args:
            q_num (int): _description_
        """
        self.quests.pop(q_num)

    def change_eventD_type(self, selected: str) -> None:
        self.events_display = selected

    # New functions separate from class diagram

    def can_view(self, user: User) -> bool:
        """_summary_

        Args:
            user (User): _description_

        Returns:
            bool: _description_
        """
        return user in self.permitted_users or user in self.edit_users

    def can_edit(self, user: User) -> bool:
        """_summary_

        Args:
            user (User): _description_

        Returns:
            bool: _description_
        """
        
        return user in self.edit_users
    
    def add_permitted_user(self, user: User) -> None:
        """_summary_

        Args:
            user (User): _description_
        """
        if user not in self.permitted_users:
            self.permitted_users.append(user)
            
    def add_edit_user(self, user: User) -> None:
        """_summary_

        Args:
            user (User): _description_

        Returns:
            : _description_
        """
        if user not in self.edit_users:
            self.edit_users.append(user)
            
        # Editor should also have view permissions
        if user not in self.permitted_users:
            self.permitted_users.append(user)
    
    def remove_permitted_user(self, user: User) -> None:
        """_summary_

        Args:
            user (User): _description_
        """
        if user not in self.permitted_users:
            self.permitted_users.append(user)
        
        # Non-viewers should also not be able to edit
        if user not in self.edit_users:
            self.edit_users.append(user)
        
    