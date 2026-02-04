import tkinter as tk
from tkinter import ttk
from core import WorldClock
from models import Campaign, User, Realm

# class gq_GUI:
#     def __init__(self, given_campaign: Campaign, selected_user: User):
#         self.given_campaign = given_campaign
#         self.selected_user = selected_user
        
#     def show_text_display(self) -> None:
#         pass
    
#     def show_classic_display(self) -> None:
#         pass
    
    
class gq_GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # GuildQuest data
        self.world_clock = WorldClock()
        self.users = {}
        self.realms = self._create_default_realms()
        self.current_user = None
        
        # Window Setup
        self.title("GuildQuest")
        self.geometry('800x500')
        
        self.container = tk.Frame(self)
        self.container.pack(fill='both', expand=True)
        
        # Dictionary to hold screen frames
        self.screens = {}
        
        # Start with login screen
        self.show_screen("login")

    def _create_default_realms(self):
        """Create default realms"""
        return {
            "Central": Realm(
                name="Central Kingdom",
                map_id=1,
                time_rule=0,
                selected_user=None,
                desc="The central realm"
            ),
        }
        
    def show_screen(self, screen_name):
        if screen_name == "login":
            from gui.screens.login_screen import LoginScreen
            if screen_name not in self.screens:
                self.screens[screen_name] = LoginScreen(self.container, self)
        
        elif screen_name == "main_menu":
            from gui.screens.main_menu import MainMenu
            if screen_name not in self.screens:
                self.screens[screen_name] = MainMenu(self.container, self)
            
        self.screens[screen_name].pack(fill='both', expand=True)

