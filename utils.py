import os
import json
from tkinter import messagebox
import customtkinter as ctk


# ===============================
# VAULT (FAVORITE & DELETE)
# ===============================

INTERESTING_FACTS = [
    "Honey never spoils.",
    "Octopuses have three hearts.",
    "A day on Venus is longer than a year on Venus.",
    "Sharks existed before trees.",
    "Ants take 8-minute rests twice a day."
]

def show_vault(self):
    self.clear_view()
    ctk.CTkLabel(
        self.view,
        text="🏛️ The Vault",
        font=("Segoe UI", 32, "bold"),
        text_color=get_theme_color("accent")
    ).pack(anchor="w", pady=10)

    scroll = ctk.CTkScrollableFrame(self.view, fg_color="transparent")
    scroll.pack(expand=True, fill="both")

    # Sort by Favorites first, then timestamp
    user_data = [i for i in self.history_data if i.get('user') == self.current_user]
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
            command=lambda c=item['content']: self.view_entry(c)
        ).pack(side="right")


def toggle_fav(self, item):
    item['fav'] = not item.get('fav', False)
    self.save_vault()
    self.show_vault()


def delete_entry(self, item):
    if messagebox.askyesno("Confirm", "Delete this generation?"):
        self.history_data.remove(item)
        self.save_vault()
        self.show_vault()


def view_entry(self, content):
    self.show_workstation()
    self.output.insert("1.0", content)


# ===============================
# STORAGE
# ===============================

def load_vault(self):
    if os.path.exists(self.vault_file):
        try:
            with open(self.vault_file, "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_vault(self):
    with open(self.vault_file, "w") as f:
        json.dump(self.history_data, f, indent=4)


def manual_save(self):
    if self.last_content:
        self.history_data.append(self.last_content)
        self.save_vault()
        messagebox.showinfo("Saved", "Archived to The Vault! ✨")
        self.save_vault_btn.pack_forget()
        self.last_content = None
    else:
        messagebox.showwarning("Empty", "No content to save.")

def clear_screen(app):
    for w in app.winfo_children():
        w.destroy()


def clear_view(app):
    for w in app.view.winfo_children():
        w.destroy()