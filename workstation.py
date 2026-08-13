import time
import threading
import random
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image
import threading  # ADD THIS LINE


from theme import get_theme_color
from utils import clear_view
from utils import INTERESTING_FACTS  # or move the list to a separate constants file


class Workstation:
    def __init__(self, app):
        self.app = app
        self.first_load_done = False

    # ===============================
    # AI LOGIC / WORKSTATION UI
    # ===============================
    def show_workstation(self, default_type="Short Story"):
        app = self.app

        def build_ui():
            clear_view(app)


            app.workspace_frame = ctk.CTkFrame(app.view)
            app.workspace_frame.pack(expand=True, fill="both")

        # KEEP ALL YOUR EXISTING UI CODE BELOW THIS

        # Header
            header = ctk.CTkFrame(app.workspace_frame, height=80, corner_radius=20)
            header.pack(fill="x", pady=(0, 20))
            header.pack_propagate(False)

            # Left spacer
            left_space = ctk.CTkFrame(header, fg_color="transparent", width=60)
            left_space.pack(side="left")

            # Center title
            title_lbl = ctk.CTkLabel(
                header,
                text="🚀 Creative Workstation",
                font=("Segoe UI", 36, "bold"),
                text_color=get_theme_color("accent"),
            )
            title_lbl.pack(side="left", expand=True, padx=20)

            # Right logout button
            logout_btn = ctk.CTkButton(
                header,
                text="➜]",
                width=50,
                height=50,
                corner_radius=25,
                font=("Segoe UI", 22, "bold"),
                fg_color="transparent",
                hover_color="#DC2626",
                text_color="#EF4444",
                command=app.logout
            )
            logout_btn.pack(side="right", padx=20, pady=15)

            # Content Type
            type_frame = ctk.CTkFrame(app.workspace_frame, fg_color="transparent")
            type_frame.pack(fill="x", pady=10)
            ctk.CTkLabel(
                type_frame,
                text="Create:",
                font=("Segoe UI", 18, "bold"),
                text_color=get_theme_color("txt"),
            ).pack(anchor="w")

            app.asset_type = ctk.StringVar(value=default_type)
            types = [
                "Blog Post",
                "Poem",
                "Video Script",
                "Short Story",
                "Email",
                "Image Prompt",
                "AI Artwork Description",
                "Social Post",
            ]
            opt = ctk.CTkOptionMenu(
                type_frame,
                values=types,
                variable=app.asset_type,
                fg_color=get_theme_color("accent"),
                button_color=get_theme_color("accent_hover"),
                dropdown_fg_color=get_theme_color("sidebar"),
                width=300,
                height=50,
                font=("Segoe UI", 16),
            )
            opt.pack(pady=(5, 15))

            # Input
            app.topic_entry = ctk.CTkEntry(
                app.workspace_frame,
                placeholder_text="📝 Enter your creative vision or topic...",
                height=55,
                font=("Segoe UI", 16),
                corner_radius=15,
            )
            app.topic_entry.pack(fill="x", pady=(0, 20))

            # Controls Row 1: Fast Mode + IMAGE CHECKBOX + Max Tokens
            ctrl1 = ctk.CTkFrame(app.workspace_frame, fg_color="transparent")
            ctrl1.pack(fill="x", pady=5)

            app.fast_mode = ctk.BooleanVar()
            fast_cb = ctk.CTkCheckBox(
                ctrl1,
                text="⚡Fast Mode (Stream + Short)",
                variable=app.fast_mode,
                font=("Segoe UI", 14),
                checkbox_width=25,
                fg_color=get_theme_color("accent"),
            )
            fast_cb.pack(side="left")

            app.gen_image_cb = ctk.BooleanVar(value=False)
            image_cb = ctk.CTkCheckBox(
                ctrl1,
                text="🖼️Generate Image",
                variable=app.gen_image_cb,
                font=("Segoe UI", 14),
                checkbox_width=25,
                fg_color=get_theme_color("accent"),
            )
            image_cb.pack(side="left", padx=(10, 0))

            app.max_tokens = ctk.CTkSlider(
                ctrl1,
                from_=120,
                to=350,
                width=250,
                height=30,
                fg_color=get_theme_color("sidebar"),
                progress_color=get_theme_color("accent"),
            )
            app.max_tokens.set(500)
            app.max_tokens.pack(side="right")
            ctk.CTkLabel(
                ctrl1,
                text="Tokens:",
                font=("Segoe UI", 12),
            ).pack(side="right", padx=(0, 10))

            # Main Buttons Row
            row = ctk.CTkFrame(app.workspace_frame, fg_color="transparent", height=60)
            row.pack(fill="x", pady=10)
            row.pack_propagate(False)

            app.gen_btn = ctk.CTkButton(
                row,
                text="✨ GENERATE MAGIC",
                command=self.start_ai,
                fg_color=get_theme_color("accent"),
                hover_color=get_theme_color("accent_hover"),
                height=55,
                width=220,
                font=("Segoe UI", 18, "bold"),
                corner_radius=15,
            )
            app.gen_btn.pack(side="left", padx=10)

            app.stop_btn = ctk.CTkButton(
                row,
                text="⏹ STOP",
                command=self.stop_ai,
                fg_color="#F50909",
                hover_color="#DC2626",
                height=55,
                width=120,
                font=("Segoe UI", 16, "bold"),
            )
            app.stop_btn.pack(side="left", padx=10)

            app.spinner_frame = ctk.CTkFrame(row, width=110, height=55, fg_color="transparent")
            app.save_vault_btn = ctk.CTkButton(
                row,
                text="💾 SAVE",
                command=app.vault.manual_save,
                fg_color="#10B981",
                hover_color="#059669",
                height=55,
                width=140,
                font=("Segoe UI", 16, "bold"),
            )

            app.timer_lbl = ctk.CTkLabel(row, text="⏱️ 0.0s", font=("Segoe UI", 14, "bold"))
            app.timer_lbl.pack(side="right", padx=20)

            # FULL HEIGHT TEXT AREA
            text_frame = ctk.CTkFrame(app.workspace_frame)
            text_frame.pack(expand=True, fill="both", pady=(20, 10))

            # Top bar inside text area
            # Textbox
        

            # Overlay maximize button
            # Textbox
            app.output = ctk.CTkTextbox(
                text_frame,
                font=("Segoe UI", 14),
                fg_color=get_theme_color("bg"),
                text_color=get_theme_color("txt"),
                corner_radius=15,
                border_width=2,
                border_color=get_theme_color("border"),
            )
            app.output.pack(expand=True, fill="both", padx=5, pady=5)

            # Overlay maximize button
            maximize_btn = ctk.CTkButton(
                text_frame,
                text="⛶",
                width=36,
                height=36,
                corner_radius=18,
                command=self.open_result_window,
                font=("grunger", 14, "bold"),
                fg_color=get_theme_color("accent"),
                hover_color=get_theme_color("accent_hover")
            )

            maximize_btn.place(relx=0.975, rely=0.03, anchor="ne")
            maximize_btn.lift()

            # NEW FOOTER
            app.footer = ctk.CTkFrame(app.workspace_frame, height=60, corner_radius=15)
            app.footer.pack(side="bottom", fill="x")
            app.footer.pack_propagate(False)

            status_frame = ctk.CTkFrame(app.footer, fg_color="transparent")
            status_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)

            app.sd_status = ctk.CTkLabel(
                status_frame,
                text="🖼️SD Turbo: Loading...",
                font=("Segoe UI", 15),
            )
            app.sd_status.pack(side="left")

            app.fact_lbl = ctk.CTkLabel(
                status_frame,
                text="💡 Loading inspiration...",
                font=("Segoe UI", 16),
                text_color=get_theme_color("accent"),
            )
            app.fact_lbl.pack(side="right", padx=20)
                    # show loading overlay only first time
            
        if not self.first_load_done:
            overlay, loading_lbl = self.show_loading_overlay()

            def load_once():
                build_ui()
                overlay.destroy()
                self.first_load_done = True

            app.after(800, load_once)
        else:
            build_ui()

    

    # ===============================
    # GENERATION CONTROL
    # ===============================
    def finish_generation(self, text):
        app = self.app

        def _typewriter():
            app.output.delete("1.0", "end")
            i = 0

            def type_char():
                nonlocal i
                if i < len(text) and not app.stop_requested:
                    app.output.insert("end", text[i])
                    app.output.see("end")
                    i += 1
                    app.after(5, type_char)
                else:
                    app.is_generating = False
                    app.gen_btn.configure(state="normal", text="✨ GENERATE MAGIC")
                    app.stop_btn.configure(state="disabled")
                    app.save_vault_btn.pack(side="left", padx=10)
                    app.spinner_frame.pack_forget()

                    if app.gen_image_cb.get() and not hasattr(app, "_popup_shown"):
                        app.after(5000, app.ai.maybe_open_result_window)
                    else:
                        app.is_generating = False
                        app.gen_btn.configure(state="normal", text="✨ GENERATE MAGIC")
                        app.stop_btn.configure(state="disabled")
                        app.save_vault_btn.pack(side="left", padx=10)
                        app.spinner_frame.pack_forget()

                        self.open_result_window()

            type_char()

        app.after(0, _typewriter)

    def start_ai(self):
        app = self.app
        topic = app.topic_entry.get().strip()
        if not topic or not app.local_model:
            messagebox.showwarning("Input Required", "Please enter a topic!")
            return

        app._popup_shown = False
        app.spinner_frame.pack(side="left", padx=10)
        app.save_vault_btn.pack_forget()

        app.is_generating = True
        app.stop_requested = False
        app.gen_btn.configure(
            state="disabled",
            text="✨ GENERATING...",
            fg_color="#F59E0B",
        )

        app.output.delete("1.0", "end")
        app.output.insert("end", "🎭 Thinking creatively...\n\n")
        app.start_time = time.time()
        self.update_timer()

        threading.Thread(
            target=app.ai.run_full_generation,
            args=(topic,),
            daemon=True,
        ).start()

    def update_timer(self):
        app = self.app
        if not app.is_generating:
            return

        try:
            elapsed = time.time() - app.start_time
            if app.timer_lbl.winfo_exists():
                app.timer_lbl.configure(text=f"⏱️ {elapsed:.1f}s")

            if int(elapsed) % 5 == 0 and app.fact_lbl.winfo_exists():
                app.fact_lbl.configure(
                    text=f"💡 {random.choice(INTERESTING_FACTS)}"
                )
        except Exception:
            return

        app.after(100, self.update_timer)

    def stop_ai(self):
        app = self.app
        app.stop_requested = True
        app.is_generating = False
        app.gen_btn.configure(state="normal", text="✨ GENERATE MAGIC")

    # ===============================
    # IMAGE PREVIEW & POPUP
    # ===============================
    def show_image_preview(self, img):
        app = self.app
        # image_preview_label lives in old result_frame version; here you can create it if needed.
        if not hasattr(app, "image_preview_label"):
            return
        try:
            app.image_preview_label.configure(image=img, text="")
            app.image_preview_label.image = img
        except Exception:
            pass

    def open_result_window(self):
        app = self.app

        win = ctk.CTkToplevel(app)
        win.transient(app)
        win.lift()                 # bring above main window
        win.focus_force()          # force keyboard + window focus
        win.attributes("-topmost", True)   # keep on top temporarily
        win.after(300, lambda: win.attributes("-topmost", False))
        win.title("Generated Content - Image & Text")
        win.geometry("1200x720")

        # GRID STRUCTURE
        win.grid_columnconfigure(0, weight=2)  # image
        win.grid_columnconfigure(1, weight=3)  # text
        win.grid_rowconfigure(1, weight=1)

        # TITLE
        title = ctk.CTkLabel(
            win,
            text="✨ Generated Output",
            font=("Segoe UI", 24, "bold"),
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # ========================
        # LEFT SIDE → IMAGE
        # ========================
        img_frame = ctk.CTkFrame(win)
        img_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        if app.last_image:
            img_label = ctk.CTkLabel(img_frame, image=app.last_image, text="")
            img_label.image = app.last_image
            img_label.pack(expand=True, pady=10)
        else:
            ctk.CTkLabel(
                img_frame,
                text="No image generated",
                font=("Segoe UI", 16)
            ).pack(expand=True)

        # DOWNLOAD IMAGE
        def download_image():
            from tkinter import filedialog
            path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png")]
            )
            if path:
                Image.open("generated.png").save(path)

        download_btn = ctk.CTkButton(
            img_frame,
            text="⬇ Download Image",
            width=180,
            command=download_image
        )
        download_btn.pack(pady=10)

        # ========================
        # RIGHT SIDE → TEXT
        # ========================
        text_frame = ctk.CTkFrame(win)
        text_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

        # TOOLBAR
        toolbar = ctk.CTkFrame(text_frame, fg_color="transparent")
        toolbar.pack(fill="x")

        # COPY
        def copy_text():
            app.clipboard_clear()
            app.clipboard_append(text_box.get("1.0", "end"))

        # EXPORT
        def export_text():
            from tkinter import filedialog
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text File", "*.txt")]
            )
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text_box.get("1.0", "end"))

        copy_btn = ctk.CTkButton(toolbar, text="📋 Copy", width=90, command=copy_text)
        copy_btn.pack(side="left", padx=5, pady=5)

        export_btn = ctk.CTkButton(toolbar, text="📤 Export", width=90, command=export_text)
        export_btn.pack(side="left", padx=5)

        save_btn = ctk.CTkButton(toolbar, text="💾 Save", width=90, command=app.vault.manual_save)
        save_btn.pack(side="left", padx=5)

        # TEXT AREA
        text_box = ctk.CTkTextbox(text_frame, font=("Segoe UI", 14))
        text_box.pack(expand=True, fill="both", padx=5, pady=5)

        if app.last_content:
            text_box.insert("1.0", app.last_content["content"])

        # ========================
        # FLOATING REGENERATE BAR
        # ========================
        regen_bar = ctk.CTkFrame(win, height=70)
        regen_bar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(5,15))

        regen_bar.grid_columnconfigure(0, weight=1)

        edit_entry = ctk.CTkEntry(
            regen_bar,
            placeholder_text="✏ Edit topic and regenerate..."
        )
        edit_entry.grid(row=0, column=0, padx=15, pady=15, sticky="ew")

        def regenerate():
            topic = edit_entry.get().strip()
            if not topic:
                return
            app.topic_entry.delete(0, "end")
            app.topic_entry.insert(0, topic)
            self.start_ai()

        regen_btn = ctk.CTkButton(
            regen_bar,
            text="🔄 Regenerate",
            width=160,
            command=regenerate
        )
        regen_btn.grid(row=0, column=1, padx=15)


    def show_loading_overlay(self):
        app = self.app

        overlay = ctk.CTkFrame(app, fg_color="#0B1120")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        loading_lbl = ctk.CTkLabel(
            overlay,
            text="⚡ Loading workspace",
            font=("Segoe UI", 26, "bold"),
            text_color="white"
        )
        loading_lbl.place(relx=0.5, rely=0.48, anchor="center")

        subtitle = ctk.CTkLabel(
            overlay,
            text="Preparing your creative tools...",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        )
        subtitle.place(relx=0.5, rely=0.54, anchor="center")

        return overlay, loading_lbl
    
    def add_profile_section(self, parent):
        app = self.app

        # get current logged in username
        username = app.current_user if app.current_user else "Guest"
        initial = username[0].upper()

        profile = ctk.CTkFrame(
            parent,
            height=70,
            corner_radius=40,
            fg_color="#111827"
        )
        profile.pack(fill="x", padx=12, pady=(10, 20))
        profile.pack_propagate(False)

        avatar = ctk.CTkLabel(
            profile,
            text=initial,
            width=45,
            height=45,
            corner_radius=22,
            fg_color="#8B5CF6",
            text_color="white",
            font=("Segoe UI", 18, "bold")
        )
        avatar.pack(side="left", padx=10)

        info = ctk.CTkFrame(profile, fg_color="transparent")
        info.pack(side="left", padx=5)

        name_lbl = ctk.CTkLabel(
            info,
            text=username,
            font=("Segoe UI", 14, "bold")
        )
        name_lbl.pack(anchor="w")

        pro_lbl = ctk.CTkLabel(
            info,
            text="● STUDIO PRO",
            text_color="#10B981",
            font=("Segoe UI", 11, "bold")
        )
        pro_lbl.pack(anchor="w")

        profile.bind("<Enter>", lambda e: profile.configure(fg_color="#1E293B"))
        profile.bind("<Leave>", lambda e: profile.configure(fg_color="#111827"))
        profile.bind("<Button-1>", lambda e: self.show_profile_menu(profile))
    
    def show_profile_menu(self, widget):
        menu = ctk.CTkToplevel(self.app)
        menu.geometry("180x140")
        menu.overrideredirect(True)

        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + 75

        menu.geometry(f"+{x}+{y}")

        frame = ctk.CTkFrame(menu, corner_radius=15)
        frame.pack(expand=True, fill="both")

        ctk.CTkButton(
            frame,
            text="👤 Profile",
            command=lambda: [menu.destroy(), self.app.show_profile()]
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame,
            text="⚙ Settings",
            command=lambda: [menu.destroy(), self.app.show_settings()]
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame,
            text="🚪 Logout",
            command=lambda: [menu.destroy(), self.app.logout()]
        ).pack(fill="x", padx=10, pady=5)