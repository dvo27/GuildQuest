"""
Character management screen for GuildQuest: Allows creating, viewing, editing, and deleting characters and their inventory
"""

import tkinter as tk
from tkinter import messagebox, ttk
from gui.screens.base_screen import BaseScreen
from models import Character, Item

class CharacterScreen(BaseScreen):
    def create_widgets(self):
        """
        Create the character management screen
        """
        
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
            relief='flat',
            highlightthickness=0
        ).pack(side='left', padx=20, pady=15)
        
        # Title
        tk.Label(
            header_frame,
            text="Character Management",
            bg='#1a1a1a',
            fg='white',
            font=('Courier', 16, 'bold')
        ).pack(side='left', padx=20, pady=15)
        
        # World clock
        world_time = self.app.world_clock.get_current_time().get_fulltime()
        tk.Label(
            header_frame,
            text=f"World Clock: {world_time}",
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Courier', 10)
        ).pack(side='right', padx=5, pady=15)
        
        # Main content area
        content_frame = tk.Frame(self, bg='#2b2b2b')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top section: Title and Create button
        top_section = tk.Frame(content_frame, bg='#2b2b2b')
        top_section.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            top_section,
            text=f"{self.app.current_user.username}'s Characters",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 20, 'bold')
        ).pack(side='left', padx=20)
        
        tk.Button(
            top_section,
            text="+ Create New Character",
            command=self.show_create_character_dialog,
            bg='#4a8a4a',
            font=('Courier', 12, 'bold'),
            width=20,
            height=2,
            relief='flat',
            highlightthickness=0
        ).pack(side='right')
        
        # Characters list section
        self.characters_container = tk.Frame(content_frame, bg='#2b2b2b')
        self.characters_container.pack(fill='both', expand=True)
        
        # Display characters
        self.refresh_characters_list()
    
    def refresh_characters_list(self):
        """
        Refresh the list of characters
        """
        
        # Clear existing widgets
        for widget in self.characters_container.winfo_children():
            widget.destroy()
        
        characters = self.app.current_user.characters
        
        if not characters:
            # No characters message
            tk.Label(
                self.characters_container,
                text="No characters yet! Create your first character to get started.",
                bg='#2b2b2b',
                fg='#888888',
                font=('Courier', 14)
            ).pack(pady=50)
        else:
            # Create scrollable frame for characters
            canvas = tk.Canvas(self.characters_container, bg='#2b2b2b', highlightthickness=0)
            scrollbar = tk.Scrollbar(self.characters_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind canvas width to scrollable_frame width
            def configure_scroll_region(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", configure_scroll_region)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Display each character
            for idx, character in enumerate(characters):
                self.create_character_card(scrollable_frame, character, idx)
    
    def create_character_card(self, parent, character, idx):
        """
        Create a card widget for a character
        """
        
        # Card frame
        card = tk.Frame(parent, bg='#3a3a3a', relief='raised', bd=2)
        card.pack(fill='x', pady=10, padx=5)
        
        # Main content frame
        content = tk.Frame(card, bg='#3a3a3a')
        content.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Top row: Name and Level
        top_row = tk.Frame(content, bg='#3a3a3a')
        top_row.pack(fill='x', pady=(0, 5))
        
        # Character name
        tk.Label(
            top_row,
            text=character.name,
            bg='#3a3a3a',
            fg='white',
            font=('Courier', 16, 'bold'),
            wraplength=500,
            justify='left',
            anchor='w'
        ).pack(side='left', fill='x', expand=True)
        
        # Level badge
        tk.Label(
            top_row,
            text=f"Level {character.level}",
            bg='#4a6a8a',
            fg='white',
            font=('Courier', 12, 'bold'),
            padx=15,
            pady=5
        ).pack(side='left', padx=10)
        
        # Class row
        tk.Label(
            content,
            text=f"⚔️ {character.character_class}",
            bg='#3a3a3a',
            fg='#cccccc',
            font=('Courier', 12)
        ).pack(anchor='w', pady=5)
        
        # Inventory info
        inventory_count = len(character.curr_inventory.items)
        tk.Label(
            content,
            text=f"🎒 Inventory: {inventory_count} item(s)",
            bg='#3a3a3a',
            fg='#888888',
            font=('Courier', 10)
        ).pack(anchor='w', pady=5)
        
        # Buttons row
        button_row = tk.Frame(content, bg='#3a3a3a')
        button_row.pack(fill='x', pady=(10, 0))
        
        button_config = {
            'font': ('Courier', 10),
            'width': 12,
            'height': 1,
            'relief': 'flat',
            'bd': 0,
            'highlightthickness': 0
        }
        
        # Manage Inventory button
        tk.Button(
            button_row,
            text="Manage Inventory",
            command=lambda c=character, i=idx: self.show_inventory_management(c, i),
            bg='#4a7a8a',
            **button_config
        ).pack(side='left', padx=5)
        
        # Edit button
        tk.Button(
            button_row,
            text="Edit",
            command=lambda c=character, i=idx: self.show_edit_character_dialog(c, i),
            bg='#4a4a4a',
            **button_config
        ).pack(side='left', padx=5)
        
        # Delete button
        tk.Button(
            button_row,
            text="Delete",
            command=lambda i=idx: self.delete_character(i),
            bg='#8a4a4a',
            **button_config
        ).pack(side='left', padx=5)
    
    def show_create_character_dialog(self):
        """
        Show dialog to create a new character
        """
        
        dialog = tk.Toplevel(self.app)
        dialog.title("Create New Character")
        dialog.geometry("500x450")
        dialog.configure(bg='#2b2b2b')
        dialog.grab_set()
        
        # Title
        tk.Label(
            dialog,
            text="Create New Character",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 18, 'bold')
        ).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='#2b2b2b')
        form_frame.pack(pady=10, padx=40, fill='both', expand=True)
        
        # Character name
        tk.Label(
            form_frame,
            text="Character Name:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        name_entry = tk.Entry(form_frame, width=30, font=('Arial', 12))
        name_entry.grid(row=0, column=1, sticky='ew', pady=10, padx=(10, 0))
        name_entry.focus()
        
        # Character class
        tk.Label(
            form_frame,
            text="Class:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        class_var = tk.StringVar(dialog)
        class_options = ["Warrior", "Mage", "Rogue", "Cleric", "Ranger", "Paladin", "Bard", "Druid"]
        class_var.set(class_options[0])
        
        class_dropdown = tk.OptionMenu(form_frame, class_var, *class_options)
        class_dropdown.config(bg='#4a4a4a', fg='white', font=('Courier', 11), width=25)
        class_dropdown.grid(row=1, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        # Level
        tk.Label(
            form_frame,
            text="Starting Level:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        level_entry = tk.Entry(form_frame, width=30, font=('Arial', 12))
        level_entry.insert(0, "1")
        level_entry.grid(row=2, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        def do_create():
            name = name_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Character name cannot be empty!")
                return
            
            try:
                level = int(level_entry.get())
                if level < 1:
                    messagebox.showerror("Error", "Level must be at least 1!")
                    return
                if level > 100:
                    messagebox.showerror("Error", "Level cannot exceed 100!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid level number!")
                return
            
            # Create character (curr_inventory auto-created by default_factory)
            character = Character(
                name=name,
                character_class=class_var.get(),
                level=level
            )
            
            self.app.current_user.characters.append(character)
            
            messagebox.showinfo("Success", f"Character '{name}' created!")
            dialog.destroy()
            
            # Refresh the characters list
            self.refresh_characters_list()
            
            # Refresh main menu to update character count
            if "main_menu" in self.app.screens:
                self.app.screens["main_menu"].destroy()
                del self.app.screens["main_menu"]
        
        name_entry.bind('<Return>', lambda e: do_create())
        
        tk.Button(
            button_frame,
            text="Create Character",
            command=do_create,
            bg='#4a8a4a',
            font=('Courier', 12),
            width=15,
            relief='flat',
            highlightthickness=0
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg='#4a4a4a',
            font=('Courier', 12),
            width=15,
            relief='flat',
            highlightthickness=0
        ).pack(side='left', padx=5)
    
    def show_edit_character_dialog(self, character, char_idx):
        """
        Show dialog to edit a character
        """
        
        dialog = tk.Toplevel(self.app)
        dialog.title("Edit Character")
        dialog.geometry("500x450")
        dialog.configure(bg='#2b2b2b')
        dialog.grab_set()
        
        # Title
        tk.Label(
            dialog,
            text="Edit Character",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 18, 'bold')
        ).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='#2b2b2b')
        form_frame.pack(pady=10, padx=40, fill='both', expand=True)
        
        # Character name
        tk.Label(
            form_frame,
            text="Character Name:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        name_entry = tk.Entry(form_frame, width=30, font=('Arial', 12))
        name_entry.insert(0, character.name)
        name_entry.grid(row=0, column=1, sticky='ew', pady=10, padx=(10, 0))
        name_entry.focus()
        name_entry.select_range(0, tk.END)
        
        # Character class
        tk.Label(
            form_frame,
            text="Class:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        class_var = tk.StringVar(dialog)
        class_options = ["Warrior", "Mage", "Rogue", "Cleric", "Ranger", "Paladin", "Bard", "Druid"]
        class_var.set(character.character_class)
        
        class_dropdown = tk.OptionMenu(form_frame, class_var, *class_options)
        class_dropdown.config(bg='#4a4a4a', fg='white', font=('Arial', 11), width=25)
        class_dropdown.grid(row=1, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        # Level
        tk.Label(
            form_frame,
            text="Level:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        level_entry = tk.Entry(form_frame, width=30, font=('Arial', 12))
        level_entry.insert(0, str(character.level))
        level_entry.grid(row=2, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        def do_save():
            name = name_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Character name cannot be empty!")
                return
            
            try:
                level = int(level_entry.get())
                if level < 1:
                    messagebox.showerror("Error", "Level must be at least 1!")
                    return
                if level > 100:
                    messagebox.showerror("Error", "Level cannot exceed 100!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid level number!")
                return
            
            # Update character
            character.name = name
            character.level = level
            character.character_class = class_var.get()
            
            messagebox.showinfo("Success", "Character updated!")
            dialog.destroy()
            
            # Refresh the characters list
            self.refresh_characters_list()
        
        name_entry.bind('<Return>', lambda e: do_save())
        
        tk.Button(
            button_frame,
            text="Save Changes",
            command=do_save,
            bg='#4a8a4a',
            font=('Courier', 12),
            width=15,
            relief='flat',
            highlightthickness=0
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg='#4a4a4a',
            fg='white',
            font=('Courier', 12),
            width=15,
            relief='flat',
            highlightthickness=0
        ).pack(side='left', padx=5)
    
    def delete_character(self, char_idx):
        """
        Delete a character
        """
        
        character = self.app.current_user.characters[char_idx]
        
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{character.name}'?\n\n"
            f"This will also delete {len(character.curr_inventory.items)} item(s) in their inventory.\n\n"
            "This action cannot be undone!"
        ):
            self.app.current_user.characters.pop(char_idx)
            messagebox.showinfo("Success", "Character deleted!")
            
            # Refresh the characters list
            self.refresh_characters_list()
            
            # Refresh main menu to update character count
            if "main_menu" in self.app.screens:
                self.app.screens["main_menu"].destroy()
                del self.app.screens["main_menu"]
    
    def show_inventory_management(self, character, char_idx):
        """
        Show inventory management dialog
        """
        
        dialog = tk.Toplevel(self.app)
        dialog.title(f"Inventory: {character.name}")
        dialog.geometry("600x500")
        dialog.configure(bg='#2b2b2b')
        dialog.grab_set()
        
        # Title
        title_frame = tk.Frame(dialog, bg='#2b2b2b')
        title_frame.pack(fill='x', pady=20, padx=20)
        
        tk.Label(
            title_frame,
            text=f"🎒 {character.name}'s Inventory",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 16, 'bold')
        ).pack(side='left')
        
        tk.Button(
            title_frame,
            text="+ Add Item",
            command=lambda: self.show_add_item_dialog(character, dialog),
            bg='#4a8a4a',
            font=('Courier', 10, 'bold'),
            relief='flat',
            highlightthickness=0,
            padx=15,
            pady=5
        ).pack(side='right')
        
        # Inventory list container
        inventory_container = tk.Frame(dialog, bg='#2b2b2b')
        inventory_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        def refresh_inventory():
            # Clear existing widgets
            for widget in inventory_container.winfo_children():
                widget.destroy()
            
            if not character.curr_inventory.items:
                tk.Label(
                    inventory_container,
                    text="No items in inventory",
                    bg='#2b2b2b',
                    fg='#888888',
                    font=('Courier', 12)
                ).pack(pady=50)
            else:
                # Create scrollable frame
                canvas = tk.Canvas(inventory_container, bg='#2b2b2b', highlightthickness=0)
                scrollbar = tk.Scrollbar(inventory_container, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg='#2b2b2b')
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                def configure_scroll_region(event):
                    canvas.configure(scrollregion=canvas.bbox("all"))
                    canvas.itemconfig(canvas_window, width=event.width)
                
                canvas.bind("<Configure>", configure_scroll_region)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
                # Display each item
                for idx, item in enumerate(character.curr_inventory.items):
                    item_frame = tk.Frame(scrollable_frame, bg='#3a3a3a', relief='raised', bd=1)
                    item_frame.pack(fill='x', pady=5)
                    
                    content = tk.Frame(item_frame, bg='#3a3a3a')
                    content.pack(fill='x', padx=10, pady=8)
                    
                    # Item name and rarity
                    info_frame = tk.Frame(content, bg='#3a3a3a')
                    info_frame.pack(fill='x')
                    
                    tk.Label(
                        info_frame,
                        text=item.name,
                        bg='#3a3a3a',
                        fg='white',
                        font=('Courier', 12, 'bold')
                    ).pack(side='left')
                    
                    tk.Label(
                        info_frame,
                        text=f"  •  {item.rarity}",
                        bg='#3a3a3a',
                        fg='#888888',
                        font=('Courier', 10)
                    ).pack(side='left')
                    
                    # Damage
                    tk.Label(
                        info_frame,
                        text=f"  •  Damage: {item.damage}",
                        bg='#3a3a3a',
                        fg='#ffaa00',
                        font=('Courier', 10)
                    ).pack(side='left')
                    
                    # Description
                    if item.description:
                        tk.Label(
                            content,
                            text=item.description,
                            bg='#3a3a3a',
                            fg='#cccccc',
                            font=('Courier', 9),
                            wraplength=500,
                            justify='left'
                        ).pack(anchor='w', pady=(5, 0))
                    
                    # Delete button
                    tk.Button(
                        content,
                        text="Remove",
                        command=lambda i=item: remove_item(i),
                        bg='#8a4a4a',
                        font=('Courier', 9),
                        relief='flat',
                        highlightthickness=0,
                        padx=10,
                        pady=2
                    ).pack(anchor='w', pady=(5, 0))
        
        def remove_item(item):
            if messagebox.askyesno("Confirm", f"Remove '{item.name}' from inventory?"):
                character.curr_inventory.remove_inventory(item)
                refresh_inventory()
                # Refresh main character list
                self.refresh_characters_list()
        
        refresh_inventory()
        
        # Store refresh function so add item dialog can use it
        dialog.refresh_inventory = refresh_inventory
        
        # Close button
        tk.Button(
            dialog,
            text="Close",
            command=dialog.destroy,
            bg='#4a4a4a',
            font=('Courier', 12),
            width=15,
            relief='flat',
            highlightthickness=0
        ).pack(pady=(0, 20))
    
    def show_add_item_dialog(self, character, parent_dialog):
        """
        Show dialog to add an item to character inventory
        """
        
        dialog = tk.Toplevel(self.app)
        dialog.title("Add Item")
        dialog.geometry("500x500")
        dialog.configure(bg='#2b2b2b')
        dialog.grab_set()
        
        # Title
        tk.Label(
            dialog,
            text="Add Item to Inventory",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 16, 'bold')
        ).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='#2b2b2b')
        form_frame.pack(pady=10, padx=40, fill='both', expand=True)
        
        # Item name
        tk.Label(
            form_frame,
            text="Item Name:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        name_entry = tk.Entry(form_frame, width=30, font=('Arial', 12))
        name_entry.grid(row=0, column=1, sticky='ew', pady=10, padx=(10, 0))
        name_entry.focus()
        
        # Rarity
        tk.Label(
            form_frame,
            text="Rarity:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        rarity_var = tk.StringVar(dialog)
        rarity_options = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic"]
        rarity_var.set(rarity_options[0])
        
        rarity_dropdown = tk.OptionMenu(form_frame, rarity_var, *rarity_options)
        rarity_dropdown.config(bg='#4a4a4a', fg='white', font=('Arial', 11), width=25)
        rarity_dropdown.grid(row=1, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        # Damage
        tk.Label(
            form_frame,
            text="Damage:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=2, column=0, sticky='w', pady=10)
        
        damage_entry = tk.Entry(form_frame, width=30, font=('Arial', 12))
        damage_entry.insert(0, "0")
        damage_entry.grid(row=2, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        # Description
        tk.Label(
            form_frame,
            text="Description:",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 12)
        ).grid(row=3, column=0, sticky='nw', pady=10)
        
        desc_text = tk.Text(form_frame, width=30, height=5, font=('Arial', 11))
        desc_text.grid(row=3, column=1, sticky='ew', pady=10, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        def do_add():
            name = name_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            
            if not name:
                messagebox.showerror("Error", "Item name cannot be empty!")
                return
            
            try:
                damage = int(damage_entry.get())
                if damage < 0:
                    messagebox.showerror("Error", "Damage cannot be negative!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid damage number!")
                return
            
            # Create item matching UML structure
            item = Item(
                name=name,
                rarity=rarity_var.get(),
                damage=damage,
                description=description
            )
            
            # Use proper method from Inventory class
            character.curr_inventory.add_inventory(item)
            
            messagebox.showinfo("Success", f"'{name}' added to inventory!")
            dialog.destroy()
            
            # Refresh parent inventory dialog
            if hasattr(parent_dialog, 'refresh_inventory'):
                parent_dialog.refresh_inventory()
            
            # Refresh main character list
            self.refresh_characters_list()
        
        name_entry.bind('<Return>', lambda e: do_add())
        
        tk.Button(
            button_frame,
            text="Add Item",
            command=do_add,
            bg='#4a8a4a',
            font=('Courier', 12),
            width=12,
            relief='flat',
            highlightthickness=0
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg='#4a4a4a',
            font=('Courier', 12),
            width=12,
            relief='flat',
            highlightthickness=0
        ).pack(side='left', padx=5)