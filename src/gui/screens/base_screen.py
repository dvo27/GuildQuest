import tkinter as tk

class BaseScreen(tk.Frame):
    """Base class for all screens"""
    
    def __init__(self, parent, app):
        """
        Args:
            parent: Parent widget (container)
            app: Reference to main gq_GUI instance
        """
        super().__init__(parent)
        self.app = app  # Access to app.world_clock, app.users, etc.
        
        self.create_widgets()
    
    def create_widgets(self):
        """Override this in child classes"""
        pass
    
    def navigate_to(self, screen_name):
        """Helper to navigate to another screen"""
        self.app.show_screen(screen_name)