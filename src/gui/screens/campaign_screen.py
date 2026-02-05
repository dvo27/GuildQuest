"""
Campaign Management Screen for GuildQuest
Allows creating, viewing, editing, and deleting campaigns
"""

import tkinter as tk
from tkinter import messagebox, ttk
from gui.screens.base_screen import BaseScreen
from models import Campaign
from core import GameTime

class CampaignScreen(BaseScreen):
    def create_widgets(self):
        """Create the campaign management screen"""
        
        # Header bar
        header_frame = tk.Frame(self, bg='#1a1a1a', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Back button
        tk.Button(
            header_frame,
            text="← Back to Main Menu",
            command=lambda: self.navigate_to("main_menu"),
            bg='#3a3a3a',
            font=('Courier', 12),
            relief='flat'
        ).pack(side='left', padx=10, pady=15)
        
        # Title
        tk.Label(
            header_frame,
            text="Campaign Management",
            bg='#1a1a1a',
            fg='white',
            font=('Courier', 16, 'bold')
        ).pack(side='left', padx=15, pady=15)
        
        # World clock
        world_time = self.app.world_clock.get_current_time().get_fulltime()
        tk.Label(
            header_frame,
            text=f"World Clock: {world_time}",
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Courier', 10)
        ).pack(side='right', padx=15, pady=15)
        
        # Main content area
        content_frame = tk.Frame(self, bg='#2b2b2b')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top section: Title and Create button
        top_section = tk.Frame(content_frame, bg='#2b2b2b')
        top_section.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            top_section,
            text=f"{self.app.current_user.username}'s Campaigns",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 20, 'bold')
        ).pack(side='left', padx=10)
        
        tk.Button(
            top_section,
            text="+ Create New Campaign",
            command=self.show_create_campaign_dialog,
            bg='#4a8a4a',
            font=('Courier', 12, 'bold'),
            width=20,
            height=2
        ).pack(side='right')
        
        # Campaigns list section
        self.campaigns_container = tk.Frame(content_frame, bg='#2b2b2b')
        self.campaigns_container.pack(fill='both', expand=True)
        
        # Display campaigns
        self.refresh_campaigns_list()
    
    def refresh_campaigns_list(self):
        """Refresh the list of campaigns"""
        # Clear existing widgets
        for widget in self.campaigns_container.winfo_children():
            widget.destroy()
        
        campaigns = self.app.current_user.campaigns
        
        if not campaigns:
            # No campaigns message
            tk.Label(
                self.campaigns_container,
                text="No campaigns yet! Create your first campaign to get started.",
                bg='#2b2b2b',
                fg='#888888',
                font=('Arial', 14)
            ).pack(pady=50)
        else:
            # Create scrollable frame for campaigns
            canvas = tk.Canvas(self.campaigns_container, bg='#2b2b2b', highlightthickness=0)
            scrollbar = tk.Scrollbar(self.campaigns_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Display each campaign
            for idx, campaign in enumerate(campaigns):
                self.create_campaign_card(scrollable_frame, campaign, idx)
    
    def create_campaign_card(self, parent, campaign, idx):
        """Create a card widget for a campaign"""
        # Card frame
        card = tk.Frame(parent, bg='#3a3a3a', relief='raised', bd=2)
        card.pack(fill='x', pady=10, padx=5)
        
        # Main content frame
        content = tk.Frame(card, bg='#3a3a3a')
        content.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Top row: Title and status
        top_row = tk.Frame(content, bg='#3a3a3a')
        top_row.pack(fill='x', pady=(0, 5))
        
        # Campaign title
        title_label = tk.Label(
            top_row,
            text=campaign.title,
            bg='#3a3a3a',
            fg='white',
            font=('Courier', 16, 'bold'),
            wraplength=600,
            justify='left',
            anchor='w'
        )
        title_label.pack(side='left', fill='x', expand=True)
        
        # Status badge
        status_color = '#4a8a4a' if campaign.activity else '#8a4a4a'
        status_text = 'Active' if campaign.activity else 'Archived'
        status_badge = tk.Label(
            top_row,
            text=status_text,
            bg=status_color,
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=2
        )
        status_badge.pack(side='left', padx=10)
        
        # Info row
        info_row = tk.Frame(content, bg='#3a3a3a')
        info_row.pack(fill='x', pady=5)
        
        info_text = f"🏰 Realm: {campaign.c_realm.name}  |  📅 Started: {campaign.time.get_fulltime()}  |  📋 Quests: {len(campaign.quests)}"
        tk.Label(
            info_row,
            text=info_text,
            bg='#3a3a3a',
            fg='#cccccc',
            font=('Arial', 10)
        ).pack(side='left')
        
        # Buttons row
        button_row = tk.Frame(content, bg='#3a3a3a')
        button_row.pack(fill='x', pady=(10))
        
        button_config = {
            'font': ('Arial', 10),
            'width': 12,
            'height': 1,
            'relief': 'flat',
            'bd': 0,
            'highlightthickness': 0 
        }
        
        # View/Manage Quests button
        tk.Button(
            button_row,
            text="Manage Quests",
            command=lambda c=campaign, i=idx: self.show_quest_management(c, i),
            bg='#4a7a8a',
            **button_config
        ).pack(side='left', padx=5)
        
        # Rename button
        tk.Button(
            button_row,
            text="Rename",
            command=lambda c=campaign: self.show_rename_dialog(c),
            bg='#4a4a4a',
            **button_config
        ).pack(side='left', padx=5)
        
        # Toggle Active/Archive button
        toggle_text = "Archive" if campaign.activity else "Activate"
        tk.Button(
            button_row,
            text=toggle_text,
            command=lambda c=campaign: self.toggle_campaign_status(c),
            bg='#4a4a4a',
            **button_config
        ).pack(side='left', padx=5)
        
        # Delete button
        tk.Button(
            button_row,
            text="Delete",
            command=lambda i=idx: self.delete_campaign(i),
            bg='#8a4a4a',
            **button_config
        ).pack(side='left', padx=5)
    
    def show_create_campaign_dialog(self):
        """Show dialog to create a new campaign"""
        dialog = tk.Toplevel(self.app)
        dialog.title("Create New Campaign")
        dialog.geometry("500x400")
        dialog.configure(bg='#2b2b2b')
        dialog.grab_set()  # Make dialog modal
        
        # Title
        tk.Label(
            dialog,
            text="Create New Campaign",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 18, 'bold')
        ).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='#2b2b2b')
        form_frame.pack(pady=10, padx=40, fill='both', expand=True)
        
        # Campaign name
        tk.Label(
            form_frame,
            text="Campaign Name:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        name_entry = tk.Entry(form_frame, width=30, font=('Arial', 12))
        name_entry.grid(row=0, column=1, sticky='ew', pady=10, padx=(10, 0))
        name_entry.focus()
        
        # Realm selection
        tk.Label(
            form_frame,
            text="Starting Realm:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        realm_var = tk.StringVar(dialog)
        realm_names = list(self.app.realms.keys())
        realm_var.set(realm_names[0])  # Default to first realm
        
        realm_dropdown = tk.OptionMenu(form_frame, realm_var, *realm_names)
        realm_dropdown.config(bg='#4a4a4a', fg='white', font=('Courier', 11), width=25)
        realm_dropdown.grid(row=1, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        # Realm description
        realm_desc_label = tk.Label(
            form_frame,
            text=self.app.realms[realm_var.get()].desc,
            bg='#2b2b2b',
            fg='#888888',
            font=('Courier', 9),
            wraplength=350,
            justify='left'
        )
        realm_desc_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=(0, 10))
        
        # Update description when realm changes
        def update_realm_desc(*args):
            realm_desc_label.config(text=self.app.realms[realm_var.get()].desc)
        
        realm_var.trace_add('write', update_realm_desc)
        
        # Timeline view preference
        tk.Label(
            form_frame,
            text="Default Timeline View:",
            bg='#2b2b2b',
            font=('Courier', 12)
        ).grid(row=3, column=0, sticky='w', pady=10)
        
        timeline_var = tk.StringVar(dialog)
        timeline_options = ["day", "week", "month", "year"]
        timeline_var.set("day")
        
        timeline_dropdown = tk.OptionMenu(form_frame, timeline_var, *timeline_options)
        timeline_dropdown.config(bg='#4a4a4a', font=('Courier', 11), width=25)
        timeline_dropdown.grid(row=3, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        def do_create():
            name = name_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Campaign name cannot be empty!")
                return
            
            # Get selected realm
            selected_realm = self.app.realms[realm_var.get()]
            
            # Get current time from world clock
            current_time = self.app.world_clock.get_current_time()
            
            # Create campaign using User's method
            self.app.current_user.create_camp(
                c_name=name,
                activity=True,
                time=current_time,
                realm=selected_realm,
                events_display=timeline_var.get(),
                quests=[],
                permitted_users=[self.app.current_user],
                edit_users=[self.app.current_user]
            )
            
            messagebox.showinfo("Success", f"Campaign '{name}' created!")
            dialog.destroy()
            
            # Refresh the campaigns list
            self.refresh_campaigns_list()
            
            # Refresh main menu to update campaign count
            if "main_menu" in self.app.screens:
                self.app.screens["main_menu"].destroy()
                del self.app.screens["main_menu"]
        
        # Bind Enter key
        name_entry.bind('<Return>', lambda e: do_create())
        
        tk.Button(
            button_frame,
            text="Create Campaign",
            command=do_create,
            bg='#4a8a4a',
            font=('Courier', 12),
            width=15
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg='#4a4a4a',
            font=('Courier', 12),
            width=15
        ).pack(side='left', padx=5)
    
    def show_rename_dialog(self, campaign):
        """Show dialog to rename a campaign"""
        dialog = tk.Toplevel(self.app)
        dialog.title("Rename Campaign")
        dialog.geometry("400x250")
        dialog.configure(bg='#2b2b2b')
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Rename Campaign",
            bg='#2b2b2b',
            font=('Courier', 16, 'bold')
        ).pack(pady=20)
        
        tk.Label(
            dialog,
            text=f"Current name: {campaign.title}",
            bg='#2b2b2b',
            font=('Courier', 10)
        ).pack(pady=5)
        
        tk.Label(
            dialog,
            text="New name:",
            bg='#2b2b2b',
            font=('Courier', 12)
        ).pack(pady=5)
        
        name_entry = tk.Entry(dialog, width=30, font=('Arial', 12))
        name_entry.insert(0, campaign.title)
        name_entry.pack(pady=10)
        name_entry.focus()
        name_entry.select_range(0, tk.END)  # Select all text
        
        def do_rename():
            new_name = name_entry.get().strip()
            
            if not new_name:
                messagebox.showerror("Error", "Name cannot be empty!")
                return
            
            campaign.rename(new_name)
            messagebox.showinfo("Success", f"Campaign renamed to '{new_name}'!")
            dialog.destroy()
            
            # Refresh the campaigns list
            self.refresh_campaigns_list()
        
        name_entry.bind('<Return>', lambda e: do_rename())
        
        button_frame = tk.Frame(dialog, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Rename",
            command=do_rename,
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
    
    def toggle_campaign_status(self, campaign):
        """Toggle campaign between active and archived"""
        campaign.change_act()
        status = "active" if campaign.activity else "archived"
        messagebox.showinfo("Success", f"Campaign is now {status}!")
        
        # Refresh the campaigns list
        self.refresh_campaigns_list()
    
    def delete_campaign(self, campaign_idx):
        """Delete a campaign"""
        campaign = self.app.current_user.campaigns[campaign_idx]
        
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{campaign.title}'?\n\nThis will delete all {len(campaign.quests)} quest(s) in this campaign.\n\nThis action cannot be undone!"
        ):
            self.app.current_user.delete_camp(campaign_idx)
            messagebox.showinfo("Success", "Campaign deleted!")
            
            # Refresh the campaigns list
            self.refresh_campaigns_list()
            
            # Refresh main menu to update campaign count
            if "main_menu" in self.app.screens:
                self.app.screens["main_menu"].destroy()
                del self.app.screens["main_menu"]
    
    def show_quest_management(self, campaign, campaign_idx):
        """Navigate to quest management for this campaign"""
        # Import here to avoid circular import
        from gui.screens.quest_screen import QuestScreen
        
        # Create a unique key for this campaign's quest screen
        screen_key = f"quest_{campaign_idx}"
        
        # If screen exists, remove it to force refresh
        if screen_key in self.app.screens:
            self.app.screens[screen_key].destroy()
            del self.app.screens[screen_key]
        
        # Create new quest screen
        quest_screen = QuestScreen(self.app.container, self.app, campaign, campaign_idx)
        self.app.screens[screen_key] = quest_screen
        
        # Hide current screen
        if self.app.current_screen and self.app.current_screen in self.app.screens:
            self.app.screens[self.app.current_screen].pack_forget()
        
        # Show quest screen
        quest_screen.pack(fill='both', expand=True)
        self.app.current_screen = screen_key