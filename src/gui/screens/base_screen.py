import tkinter as tk
from core.Observer import Observer

class BaseScreen(tk.Frame, Observer):
    """Base class for all screens"""

    def __init__(self, parent, app):
        """
        Args:
            parent: Parent widget (container)
            app: Reference to main gq_GUI instance
        """
        super().__init__(parent)
        self.app = app  # Access to app.world_clock, app.users, etc.

        # *****NEW IMPLEMENTAION FOR A3*****
        # Attach on creation
        self.app.attach(self)

        # Auto-detach when the widget is destroyed
        self.bind("<Destroy>", self._on_destroy)

        self.create_widgets()
    
    # *****NEW IMPLEMENTAION FOR A3*****
    def _on_destroy(self, event):
        # Tkinter fires Destroy events for many child widgets too; guard it:
        if event.widget is self:
            try:
                self.app.detach(self)
            except Exception:
                pass

    # *****NEW IMPLEMENTAION FOR A3*****
    def update(self, subject, event: str, data: dict) -> None:
        """Default: do nothing. Each screen decides what to handle."""
        return

    def create_widgets(self):
        """Override this in child classes"""
        pass

    def navigate_to(self, screen_name):
        """Helper to navigate to another screen"""
        self.app.show_screen(screen_name)
