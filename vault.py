import os
import json
import customtkinter as ctk
from tkinter import messagebox
from utils import clear_view

from theme import get_theme_color, CLR_ACCENT


class Vault:

    def __init__(self, app):
        self.app = app

    # ===============================
    # LOAD VAULT
    # ===============================

    def load_vault(self):

        app = self.app

        if os.path.exists(self.app.vault_file):
            try:
                with open(self.app.vault_file, "r") as f:
                    return json.load(f)
            except:
                return []

        return []

    # ===============================
    # SAVE VAULT
    # ===============================

    def save_vault(self):

        app = self.app

        with open(self.app.vault_file, "w") as f:
            json.dump(self.app.history_data, f, indent=4)

    # ===============================
    # MANUAL SAVE
    # ===============================

    def manual_save(self):

        app = self.app

        if app.last_content:
            self.app.history_data.append(self.app.last_content)
            self.save_vault()

            messagebox.showinfo("Saved", "Archived to The Vault! ✨")

            self.app.save_vault_btn.pack_forget()
            self.app.last_content = None

        else:
            messagebox.showwarning("Empty", "No content to save.")

    # ===============================
    # TOGGLE FAVORITE
    # ===============================

    def toggle_fav(self, item):

        item['fav'] = not item.get('fav', False)

        self.save_vault()
        self.show_vault()

    # ===============================
    # DELETE ENTRY
    # ===============================

    def delete_entry(self, item):

        app = self.app

        if messagebox.askyesno("Confirm", "Delete this generation?"):

            self.app.history_data.remove(item)

            self.save_vault()

            self.show_vault()

    # ===============================
    # VAULT UI
    # ===============================

    def show_vault(self):
        clear_view(self.app)

        ctk.CTkLabel(
            self.app.view,
            text="🏛️ The Vault",
            font=("Segoe UI", 32, "bold"),
            text_color=get_theme_color("accent")
        ).pack(anchor="w", pady=10)

        scroll = ctk.CTkScrollableFrame(self.app.view, fg_color="transparent")
        scroll.pack(expand=True, fill="both")

        # Sort by Favorites first
        user_data = [
            i for i in self.app.history_data
            if i.get('user') == self.app.current_user
        ]

        user_data.sort(key=lambda x: x.get('fav', False), reverse=True)

        for item in user_data:

            f = ctk.CTkFrame(scroll, fg_color=get_theme_color("sidebar"))
            f.pack(fill="x", pady=5)

            fav_icon = "⭐" if item.get('fav') else "☆"

            ctk.CTkButton(
                f,
                text=fav_icon,
                width=30,
                fg_color="transparent",
                text_color=CLR_ACCENT,
                command=lambda i=item: self.toggle_fav(i)
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                f,
                text=f"{item['topic']} ({item.get('timestamp','')})",
                text_color=get_theme_color("txt")
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                f,
                text="Delete",
                fg_color="#EF4444",
                width=60,
                command=lambda i=item: self.delete_entry(i)
            ).pack(side="right", padx=10)

            ctk.CTkButton(
                f,
                text="View",
                width=60,
                command=lambda c=item['content']: self.app.view_entry(c)
            ).pack(side="right")