# gui/screens/login_screen.py

import tkinter as tk
from tkinter import messagebox
from gui.screens.base_screen import BaseScreen
from models import User, User_Settings


class LoginScreen(BaseScreen):
    def create_widgets(self):
        """Create the login/register screen"""

        # Container for ASCII art (centered)
        art_frame = tk.Frame(self)
        art_frame.pack(pady=30)

        # Simpler ASCII Art that will display correctly
        art = r"""
   ______      _ __    __   ____                  __ 
  / ____/_  __(_) /___/ /  / __ \__  _____  _____/ /_
 / / __/ / / / / / __  /  / / / / / / / _ \/ ___/ __/
/ /_/ / /_/ / / / /_/ /  / /_/ / /_/ /  __(__  ) /_  
\____/\__,_/_/_/\__,_/   \___\_\__,_/\___/____/\__/
        """

        tk.Label(
            art_frame,
            text=art,
            fg='#00ff00',
            font=('Courier', 10),
            justify=tk.CENTER  # ← Changed to CENTER
        ).pack()

        # Title
        tk.Label(
            self,
            text="Welcome to GuildQuest",
            fg='white',
            font=('Courier', 20, 'bold')
        ).pack(pady=10)

        # Main container for form
        self.main_container = tk.Frame(self)
        self.main_container.pack(pady=30)

        # Show initial buttons
        self.show_initial_buttons()

    def show_initial_buttons(self):
        """Show initial Login/Register/Exit buttons"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        button_config = {
            'width': 20,
            'height': 2,
        }

        tk.Button(
            self.main_container,
            text="Login",
            command=self.show_login_form,
            font=('courier', 11),
            **button_config
        ).pack(pady=10)

        tk.Button(
            self.main_container,
            text="Register",
            command=self.show_register_form,
            font=('courier', 11),
            **button_config
        ).pack(pady=10)

        tk.Button(
            self.main_container,
            text="Exit",
            command=self.app.destroy,
            font=('courier', 11),
            **button_config
        ).pack(pady=10)

    def show_login_form(self):
        """Show login form"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Form frame
        form_frame = tk.Frame(self.main_container, bg='#2b2b2b')
        form_frame.pack(pady=20)

        # Title
        tk.Label(
            form_frame,
            text="Login",
            font=('Courier', 16, 'bold'),
            bg='#2b2b2b'
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Username label and entry
        tk.Label(
            form_frame,
            text="Username:",
            font=('Courier', 12),
            bg='#2b2b2b'
        ).grid(row=1, column=0, padx=10, pady=10, sticky='e')

        username_entry = tk.Entry(form_frame, width=25, font=('Courier', 12))
        username_entry.grid(row=1, column=1, padx=10, pady=10)
        username_entry.focus()

        # Button frame
        button_frame = tk.Frame(form_frame, bg='#2b2b2b')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        def do_login():
            username = username_entry.get().strip()

            if not username:
                messagebox.showerror("Error", "Please enter a username!")
                return

            if username in self.app.users:
                self.app.current_user = self.app.users[username]
                messagebox.showinfo("Success", f"Welcome back, {username}!")
                self.navigate_to("main_menu")
            else:
                messagebox.showerror("Error", "User not found!")

        username_entry.bind('<Return>', lambda e: do_login())

        tk.Button(
            button_frame,
            text="Login",
            command=do_login,
            width=15,
            font=('Courier', 12)
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="Back",
            command=self.show_initial_buttons,
            width=15,
            font=('Courier', 12)
        ).pack(side='left', padx=5)

    def show_register_form(self):
        """Show registration form"""
        # Clear container
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Form frame
        form_frame = tk.Frame(self.main_container, bg='#2b2b2b')
        form_frame.pack(pady=20)

        # Title
        tk.Label(
            form_frame,
            text="Register New User",
            bg='#2b2b2b',
            fg='white',
            font=('Courier', 16, 'bold')
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Username label and entry
        tk.Label(
            form_frame,
            text="Username:",
            bg='#2b2b2b',
            font=('Courier', 12)
        ).grid(row=1, column=0, padx=10, pady=10, sticky='e')

        username_entry = tk.Entry(form_frame, width=25, font=('Courier', 12))
        username_entry.grid(row=1, column=1, padx=10, pady=10)
        username_entry.focus()

        # Info label
        tk.Label(
            form_frame,
            text="(minimum 3 characters)",
            bg='#2b2b2b',
            fg='#888888',
            font=('Courier', 9)
        ).grid(row=2, column=1, sticky='w', padx=10)

        # Button frame
        button_frame = tk.Frame(form_frame, bg='#2b2b2b')
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        def do_register():
            username = username_entry.get().strip()

            if len(username) < 3:
                messagebox.showerror(
                    "Error", "Username must be at least 3 characters!")
                return

            if username in self.app.users:
                messagebox.showerror("Error", "Username already exists!")
                return

            # Create user
            settings = User_Settings(
                time_display='24hr',
                switch_time=False,
                current_realm=self.app.realms["Central"]
            )

            user = User(
                username=username,
                number_of_campaigns=0,
                user_settings=settings
            )

            self.app.users[username] = user
            self.app.current_user = user

            messagebox.showinfo("Success", f"User '{username}' created!")
            self.navigate_to("main_menu")

        username_entry.bind('<Return>', lambda e: do_register())

        tk.Button(
            button_frame,
            text="Register",
            command=do_register,
            width=15,
            bg='#4a4a4a',
            font=('Courier', 12)
        ).pack(side='left', padx=5)

        tk.Button(
            button_frame,
            text="Back",
            command=self.show_initial_buttons,
            width=15,
            bg='#4a4a4a',
            font=('Courier', 12)
        ).pack(side='left', padx=5)
