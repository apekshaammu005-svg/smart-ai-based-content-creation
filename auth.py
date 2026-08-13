import json
import os
import re
from tkinter import messagebox
import customtkinter as ctk
import random
from utils import clear_screen
from theme import CLR_ACCENT, CLR_ACCENT_HOVER, CLR_BORDER
from PIL import Image
from PIL import ImageEnhance

# ===============================
# PASSWORD STRENGTH CHECKER
# ===============================
def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# ===============================
# AUTHENTICATION UI
# ===============================
def show_onboarding(self, mode="login"):
    clear_screen(self)

    self.geometry("1400x900")
    self.configure(fg_color="#0B1020")

    # MAIN WRAPPER
    wrapper = ctk.CTkFrame(self, fg_color="#0B1020")
    wrapper.pack(fill="both", expand=True)

    # LEFT PANEL WITH IMAGE
    left = ctk.CTkFrame(wrapper, width=1020, fg_color="#111827")
    left.pack(side="left", fill="both", expand=True)

    # Background image
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir, "assets", "login_bg.png")

    bg_img = Image.open(img_path)
    enhancer = ImageEnhance.Brightness(bg_img)
    bg_img = enhancer.enhance(0.55)

    bg_ctk = ctk.CTkImage(
        light_image=bg_img,
        dark_image=bg_img,
        size=(1100, 980)
    )

    bg_label = ctk.CTkLabel(left, image=bg_ctk, text="")
    bg_label.place(relwidth=1, relheight=1)

    chip_frame = ctk.CTkFrame(left, fg_color="transparent")
    chip_frame.place(x=20, y=755)

    modules = ["✨ Content Gen", "🖼 Image Lab", "🎤 Voice TTS", "📈 Trend Explore", "🎬 Vlog Tools"]

    for module in modules:
        chip = ctk.CTkButton(
            chip_frame,
            text=module,
            width=88,
            height=28,
            corner_radius=14,
            fg_color="transparent",
            text_color="white",
            font=("poppins", 12)
        )
        chip.pack(side="left", padx=6)

        

   

    # RIGHT LOGIN PANEL
    


    # ---------------- LOGIN CARD ----------------
    # RIGHT LOGIN PANEL
    right = ctk.CTkFrame(wrapper, width=380, fg_color="#0F172A")
    right.pack(side="right", fill="y")

    card = ctk.CTkFrame(
        right,
        width=360,
        height=560,
        corner_radius=25,
        fg_color="#0D1328",
        border_width=1,
        border_color="#2E3A59"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        card,
        text="CREATIX",
        font=("Grunger", 32, "bold"),
        text_color="#A78BFA"
    ).pack(pady=(35, 10))

    title = "Welcome Back 👋" if mode == "login" else "Create Account ✨"

    ctk.CTkLabel(
        card,
        text=title,
        font=("Poppins", 22, "bold")
    ).pack()

    # USERNAME
    self.u_in = ctk.CTkEntry(
        card,
        placeholder_text="Username",
        width=300,
        height=50,
        corner_radius=15
    )
    self.u_in.pack(pady=15)

    # PASSWORD
    self.p_in = ctk.CTkEntry(
        card,
        placeholder_text="Password",
        show="*",
        width=300,
        height=50,
        corner_radius=15
    )
    self.p_in.pack(pady=10)

    # PASSWORD STRENGTH LABEL
    self.pass_hint = ctk.CTkLabel(
        card,
        text="",
        font=("Poppins", 12),
        text_color="#f59e0b"
    )
    self.pass_hint.pack()

    # CONFIRM PASSWORD FOR SIGNUP
    self.p_confirm = None
    self.match_hint = None

    if mode == "signup":
        self.p_confirm = ctk.CTkEntry(
            card,
            placeholder_text="Confirm Password",
            show="*",
            width=300,
            height=50,
            corner_radius=15
        )
        self.p_confirm.pack(pady=10)

        self.match_hint = ctk.CTkLabel(
            card,
            text="",
            font=("Poppins", 12)
        )
        self.match_hint.pack()

    # BUTTON
    btn_text = "SIGN IN →" if mode == "login" else "SIGN UP →"
    btn_cmd = lambda: auth_action_login(self) if mode == "login" else auth_action_signup(self)

    ctk.CTkButton(
        card,
        text=btn_text,
        width=300,
        height=50,
        corner_radius=15,
        fg_color="#8B5CF6",
        hover_color="#7C3AED",
        command=btn_cmd
    ).pack(pady=20)

    # TOGGLE
    toggle_text = "New? Create Account" if mode == "login" else "Back to Login"

    ctk.CTkButton(
        card,
        text=toggle_text,
        fg_color="transparent",
        text_color="#A78BFA",
        hover_color="#1F2937",
        command=lambda: show_onboarding(self, "signup" if mode == "login" else "login")
    ).pack()

    # PASSWORD CHECK FUNCTIONS
    def check_password(event=None):
        p = self.p_in.get()
        missing = []

        if len(p) < 8:
            missing.append("8+ chars")
        if not re.search(r"[A-Z]", p):
            missing.append("1 uppercase")
        if not re.search(r"[a-z]", p):
            missing.append("1 lowercase")
        if not re.search(r"\d", p):
            missing.append("1 number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", p):
            missing.append("1 special")

        if missing:
            self.pass_hint.configure(
                text="Missing: " + ", ".join(missing),
                text_color="#f59e0b"
            )
        else:
            self.pass_hint.configure(
                text="✓ Strong password",
                text_color="#10b981"
            )

    def check_match(event=None):
        if self.p_confirm and self.match_hint:
            if self.p_confirm.get() == self.p_in.get():
                self.match_hint.configure(
                    text="✓ Passwords match",
                    text_color="#10b981"
                )
            else:
                self.match_hint.configure(
                    text="✗ Passwords do not match",
                    text_color="#ef4444"
                )

    self.p_in.bind("<KeyRelease>", check_password)

    if self.p_confirm:
        self.p_confirm.bind("<KeyRelease>", check_match)
        self.p_in.bind("<KeyRelease>", check_match)
   
# ===============================
# ACTIONS
# ===============================
def auth_action_login(self):
    u = self.u_in.get().strip()
    p = self.p_in.get()
    
    if not u or not p:
        messagebox.showerror("Error", "Username and password required")
        return
        
    try:
        with open(self.users_file, "r") as f:
            users = json.load(f)
        if u in users and users[u] == p:
            self.current_user = u
            self.setup_main_ui()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    except FileNotFoundError:
        messagebox.showerror("Error", "User database not found")

def auth_action_signup(self):
    u = self.u_in.get().strip()
    p = self.p_in.get()
    
    if not u or not p:
        messagebox.showerror("Error", "Username and password required")
        return
    
    if not is_strong_password(p):
        messagebox.showerror(
            "Weak Password",
            "Password must contain:\n"
            "• Minimum 8 characters\n"
            "• One uppercase letter\n"
            "• One lowercase letter\n"
            "• One number\n"
            "• One special character"
        )
        return
    
    try:
        with open(self.users_file, "r") as f:
            users = json.load(f)
        if u in users:
            messagebox.showerror("Error", "Username already exists")
            return
        
        users[u] = p
        with open(self.users_file, "w") as f:
            json.dump(users, f)
        messagebox.showinfo("Success", "Account Created Successfully")
        show_onboarding(self, "login")
    except FileNotFoundError:
        messagebox.showerror("Error", "Cannot access user database")

def forgot_password(self):
    messagebox.showinfo(
        "Password Recovery",
        "Password recovery is not implemented yet.\nPlease contact the administrator."
    )
