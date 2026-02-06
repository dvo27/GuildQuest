"""
Main Menu Screen for GuildQuest
"""

import tkinter as tk
from tkinter import messagebox
from gui.screens.base_screen import BaseScreen

class MainMenu(BaseScreen):
    def create_widgets(self):
        """
        Create the main menu screen
        """
        
        # TOP LEVEL:
        # Header bar
        header_frame = tk.Frame(self, bg='#1a1a1a', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # User info on left
        tk.Label(
            header_frame,
            text=f"GuildQuest - {self.app.current_user.username}",
            bg='#1a1a1a',
            fg='white',
            font=('Courier', 16, 'bold')
        ).pack(side='left', padx=20, pady=15)
        
        # World clock on right
        world_time = self.app.world_clock.get_current_time().get_fulltime()
        tk.Label(
            header_frame,
            text=f"World Clock: {world_time}",
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Courier', 12)
        ).pack(side='right', padx=20, pady=15)
        
        # MAIN MENU LABEL AREA
        content_frame = tk.Frame(self, bg='#2b2b2b')
        content_frame.pack(fill='both', expand=True)
        
        # Title
        tk.Label(
            content_frame,
            text="Main Menu",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 28, 'bold')
        ).pack(pady=20)
        
        # Subtitle with campaign count
        num_campaigns = len(self.app.current_user.campaigns)
        num_characters = len(self.app.current_user.characters)
        
        tk.Label(
            content_frame,
            text=f"Campaigns: {num_campaigns} | Characters: {num_characters}",
            bg='#2b2b2b',
            fg='#888888',
            font=('Courier', 12)
        ).pack()
        
        # BUTTONS AREA 
        # Menu buttons container
        button_container = tk.Frame(content_frame, bg='#2b2b2b')
        button_container.pack(pady=30)
        
        # Button configuration
        button_config = {
            'width': 30,
            'height': 2,
            'bg': '#4a4a4a',
            'font': ('Courier', 12),
            'activebackground': '#5a5a5a',
            'activeforeground': 'white'
        }
        
        # Campaign Management
        tk.Button(
            button_container,
            text="Campaign Management",
            command=lambda: self.navigate_to("campaign"),
            **button_config
        ).pack(pady=8)
        
        # Character Management
        tk.Button(
            button_container,
            text="Character Management",
            command=self.show_character_management,
            **button_config
        ).pack(pady=8)
        
        # Realm Information
        tk.Button(
            button_container,
            text="Realm Information",
            command=self.show_realm_info,
            **button_config
        ).pack(pady=8)
        
        # World Clock Management
        tk.Button(
            button_container,
            text="Advance World Clock",
            command=self.show_clock_advance,
            **button_config
        ).pack(pady=8)
        
        # Settings
        tk.Button(
            button_container,
            text="Settings",
            command=self.show_settings,
            **button_config
        ).pack(pady=8)
        
        # Logout
        tk.Button(
            button_container,
            text="Logout",
            command=self.logout,
            width=30,
            height=2,
            bg='#8a4a4a',
            font=('Courier', 12),
            activebackground='#9a5a5a'
        ).pack(pady=8)
    
    def show_character_management(self):
        """
        Navigate to character management screen
        """
        
        self.navigate_to("character")
    
    # SHOW AVAILABLE REALMS WINDOW
    def show_realm_info(self):
        """
        Show realm information dialog
        """
        
        dialog = tk.Toplevel(self.app)
        dialog.title("Realm Information")
        dialog.geometry("600x700")
        dialog.configure(bg='#2b2b2b')
        
        # Title
        tk.Label(
            dialog,
            text="Available Realms",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 18, 'bold')
        ).pack(pady=20)
        
        # Current world time
        world_time = self.app.world_clock.get_current_time()
        tk.Label(
            dialog,
            text=f"Current World Clock: {world_time.get_fulltime()}",
            bg='#2b2b2b',
            fg='#00ff00',
            font=('Courier', 12)
        ).pack(pady=10)
        
        # Realms container
        realms_frame = tk.Frame(dialog, bg='#2b2b2b')
        realms_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Display each realm
        for realm_name, realm in self.app.realms.items():
            realm_frame = tk.Frame(realms_frame, bg='#3a3a3a', relief='ridge', bd=2)
            realm_frame.pack(fill='x', pady=10)
            
            # Realm name
            tk.Label(
                realm_frame,
                text=f"🏰 {realm.name}",
                bg='#3a3a3a',
                fg='white',
                font=('Arial', 14, 'bold')
            ).pack(anchor='w', padx=15, pady=(10, 5))
            
            # Description
            tk.Label(
                realm_frame,
                text=realm.desc,
                bg='#3a3a3a',
                fg='#cccccc',
                font=('Arial', 10),
                wraplength=500
            ).pack(anchor='w', padx=15, pady=5)
            
            # Time offset info
            offset_hours = realm.time_rule // 60
            offset_mins = realm.time_rule % 60
            
            if realm.time_rule == 0:
                offset_text = "Same as World Clock"
            elif realm.time_rule > 0:
                offset_text = f"{offset_hours}h {offset_mins}m ahead"
            else:
                offset_text = f"{abs(offset_hours)}h {abs(offset_mins)}m behind"
            
            tk.Label(
                realm_frame,
                text=f"Time Offset: {offset_text}",
                bg='#3a3a3a',
                fg='#888888',
                font=('Arial', 10)
            ).pack(anchor='w', padx=15, pady=5)
            
            # Current local time in this realm
            from utils import convert_to_realm_time
            local_time = convert_to_realm_time(world_time, realm)
            
            tk.Label(
                realm_frame,
                text=f"Current Local Time: {local_time.get_fulltime()}",
                bg='#3a3a3a',
                fg='#00ff00',
                font=('Courier', 10)
            ).pack(anchor='w', padx=15, pady=(5, 10))
        
        # Close button
        tk.Button(
            dialog,
            text="Close",
            command=dialog.destroy,
            bg='#4a4a4a',
            font=('Courier', 12),
            width=15
        ).pack(pady=15)
    
    # SHOW ADVANCE CLOCK WINDOW
    def show_clock_advance(self):
        """
        Show dialog to advance world clock
        """
        
        dialog = tk.Toplevel(self.app)
        dialog.title("Advance World Clock")
        dialog.geometry("400x500")
        dialog.configure(bg='#2b2b2b')
        
        # Title
        tk.Label(
            dialog,
            text="Advance World Clock",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 16, 'bold')
        ).pack(pady=20)
        
        # Current time
        current_time = self.app.world_clock.get_current_time()
        tk.Label(
            dialog,
            text=f"Current: {current_time.get_fulltime()}",
            bg='#2b2b2b',
            fg='#00ff00',
            font=('Courier', 12)
        ).pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(dialog, bg='#2b2b2b')
        input_frame.pack(pady=20)
        
        # Days
        tk.Label(input_frame, text="Days:", bg='#2b2b2b', fg='white', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
        days_entry = tk.Entry(input_frame, width=10, font=('Arial', 12))
        days_entry.insert(0, "0")
        days_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Hours
        tk.Label(input_frame, text="Hours:", bg='#2b2b2b', fg='white', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        hours_entry = tk.Entry(input_frame, width=10, font=('Arial', 12))
        hours_entry.insert(0, "0")
        hours_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Minutes
        tk.Label(input_frame, text="Minutes:", bg='#2b2b2b', fg='white', font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
        minutes_entry = tk.Entry(input_frame, width=10, font=('Arial', 12))
        minutes_entry.insert(0, "0")
        minutes_entry.grid(row=2, column=1, padx=10, pady=5)
        
        def do_advance():
            try:
                days = int(days_entry.get())
                hours = int(hours_entry.get())
                minutes = int(minutes_entry.get())
                
                if days < 0 or hours < 0 or minutes < 0:
                    messagebox.showerror("Error", "Values cannot be negative!")
                    return
                
                self.app.world_clock.advance(days=days, hours=hours, minutes=minutes)
                new_time = self.app.world_clock.get_current_time()
                
                messagebox.showinfo("Success", f"Clock advanced!\nNew time: {new_time.get_fulltime()}")
                dialog.destroy()
                
                # Refresh the main menu to show updated time
                self.app.refresh_screen("main_menu")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Advance",
            command=do_advance,
            bg='#4a4a4a',
            font=('Courier', 12),
            width=12
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg='#4a4a4a',
            font=('Courier', 12),
            width=12
        ).pack(side='left', padx=5)
    
    def show_settings(self):
        """
        Placeholder for settings
        """
        messagebox.showinfo("Coming Soon", "Settings feature coming soon!")
    
    def logout(self):
        """
        Logout and return to login screen
        """
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.app.current_user = None
            self.navigate_to("login")