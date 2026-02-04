import tkinter as tk
from tkinter import ttk
from .base_screen import BaseScreen

class MainMenu(BaseScreen):
    def create_widgets(self):
        self.init_ascii_label()
        # Buttons
        login_button = tk.Button(self, text="Login")
        register_button = tk.Button(self, text="Register")
        exit_button = tk.Button(self, text="Exit", command=self.app.destroy)

        # Display buttons
        login_button.pack()
        register_button.pack()
        exit_button.pack()

    def init_ascii_label(self):
        # classic art?
        guild_quest_art = r"""
           ______      _ __    __   ____                  __ 
          / ____/_  __(_) /___/ /  / __ \__  _____  _____/ /_
         / / __/ / / / / / __  /  / / / / / / / _ \/ ___/ __/
        / /_/ / /_/ / / / /_/ /  / /_/ / /_/ /  __(__  ) /_  
        \____/\__,_/_/_/\__,_/   \___\_\__,_/\___/____/\__/                                        
        """
        style = ttk.Style()
        style.configure('Custom.TLabel', font='TkFixedFont')
        guild_quest_ascii_label = ttk.Label(self,
                                            text=guild_quest_art,
                                            justify=tk.LEFT,
                                            background='white',
                                            foreground='white',
                                            style='Custom.TLabel')
        guild_quest_ascii_label.pack()