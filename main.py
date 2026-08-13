import os
import json
import threading
from tkinter import messagebox
import customtkinter as ctk
from utils import clear_screen
from theme import get_theme_color
import threading  # ADD THIS LINE
from image_generator import ImageGenerator

# modules
import auth
import vault
import theme
import utils
from ai_models import AIModels
from workstation import Workstation
from vault import Vault

class ContentIQ_Pro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CreatiX | Modern Pro Edition")
        self.geometry("1400x900")

        ctk.set_appearance_mode("Dark")

        # =============================== 
        # INTERNAL STATE (same as original)
        # ===============================

        self.model_name = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
        self.users_file = "secure_registry.json"
        self.vault_file = "content_vault.json"

        self.current_user = None
        self.is_generating = False
        self.stop_requested = False
        self.trend_typing_job = None
        self.trend_generation_id = 0
        self.tts_engine = None
        self.is_speaking = False

        self.local_model = None
        self.last_content = None
        self.last_image = None
        self.configure(fg_color=get_theme_color("bg"))

        self.content_cache = {}

        # =============================== 
        # MODULE INSTANCES
        # ===============================
        self.image_gen=ImageGenerator(self)
        self.ai = AIModels(self, self.model_name)
        self.vault = Vault(self)
        self.workstation = Workstation(self)
        


        threading.Thread(
            target=self.image_gen.load_model,
            daemon=True
        ).start()

        #to save generated content
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.image_dir = os.path.join(self.base_dir, "data", "images")
        self.content_dir = os.path.join(self.base_dir, "data", "content")

        # create folders if not exist
        os.makedirs(self.image_dir, exist_ok=True)
        os.makedirs(self.content_dir, exist_ok=True)
        #end of content cache

        # =============================== 
        # INITIAL FILES
        # ===============================

        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({"admin": "1234"}, f)

        self.history_data = self.vault.load_vault()

        # =============================== 
        # LOAD AI ENGINES
        # ===============================

        threading.Thread(target=self.ai.preload_engine, daemon=True).start()
    

        # =============================== 
        # START APP
        # ===============================

        auth.show_onboarding(self)

    #theme
    def safe_after(self, delay, func):
        if self.winfo_exists():
            try:
                self.after(delay, func)
            except Exception:
                pass

    #end of theme

    # SIDEBAR
    def setup_main_ui(self):

        clear_screen(self)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
       
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color=get_theme_color("sidebar"))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(30,10))

        ctk.CTkLabel(
            header_frame,
            text="CreatiX",
            font=("Grunger", 28, "bold"),
            text_color=get_theme_color("accent")
        ).pack()
        self.workstation.add_profile_section(self.sidebar)

        # helper functions
        def section(title):
            ctk.CTkLabel(
                self.sidebar,
                text=title,
                font=("Poppins", 12, "bold"),
                text_color="#7c8db5"
            ).pack(anchor="w", padx=20, pady=(12,4))

        def nav_button(text, command):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=38,
                fg_color="transparent",
                text_color=get_theme_color("txt"),
                hover_color=get_theme_color("accent_hover"),
                anchor="w",
                font=("Segoe UI", 15, "bold"),
                corner_radius=10
            )
            btn.pack(fill="x", padx=15, pady=4)

        # AI CREATION
        section("AI CREATION")
        nav_button("✨ Content Creator", self.workstation.show_workstation)
        nav_button("🎬 Script Writer", self.show_script_writer)
        nav_button("📱 Social Post Generator", self.show_social_generator)

        # MEDIA
        section("MEDIA")
        nav_button("🖼 Image Lab", self.show_image_lab)

        # VOICE
        section("VOICE")
        nav_button("🎤 Voice Lab", self.show_voice_lab)
        nav_button("🔥 Trend Explorer", self.show_trend_analysis)

        # STORAGE
        section("STORAGE")
        nav_button("🏛️ The Vault", self.vault.show_vault)

        # ACCOUNT
        nav_button("🚪 Logout", self.logout)

    

        # MAIN VIEW
        self.view = ctk.CTkFrame(self, fg_color=get_theme_color("bg"))
        self.view.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        self.workstation.show_workstation()

    #===================end of sidebar====================

    #safe
    
    #end of safe

    
    def logout(self):
        import auth
        self.current_user = None
        auth.show_onboarding(self)

    def show_script_writer(self):

        utils.clear_view(self)

        ctk.CTkLabel(
            self.view,
            text="🎬 Script Writer",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=20)

        topic = ctk.CTkEntry(
            self.view,
            placeholder_text="Enter video topic...",
            width=500,
            height=50
        )
        topic.pack(pady=10)

        def generate_script():
            t = topic.get().strip()
            if not t:
                return

            self.workstation.show_workstation()

            def continue_generate():
                self.asset_type.set("Video Script")
                self.topic_entry.delete(0, "end")
                self.topic_entry.insert(0, t)
                self.workstation.start_ai()

            self.after(900, continue_generate)

        ctk.CTkButton(
            self.view,
            text="Generate Script",
            height=45,
            command=generate_script
        ).pack(pady=20) 


        


    def show_profile(self):
        utils.clear_view(self)

        ctk.CTkLabel(
            self.view,
            text="👤 Profile",
            font=("Segoe UI", 32, "bold")
        ).pack(pady=30)

        ctk.CTkLabel(
            self.view,
            text=f"Logged in as: {self.current_user}",
            font=("Segoe UI", 18)
        ).pack()

    #social post generator
    def show_social_generator(self):

        utils.clear_view(self)

        ctk.CTkLabel(
            self.view,
            text="📱 Social Post Generator",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=20)

        topic = ctk.CTkEntry(
            self.view,
            placeholder_text="Enter topic...",
            width=500,
            height=50
        )
        topic.pack(pady=10)

        def generate_post():
            t = topic.get().strip()
            if not t:
                return

            self.workstation.show_workstation()

            def continue_generate():
                self.asset_type.set("Social Post")
                self.topic_entry.delete(0, "end")
                self.topic_entry.insert(0, t)
                self.workstation.start_ai()

            self.after(900, continue_generate)

        ctk.CTkButton(
            self.view,
            text="Generate Post",
            height=45,
            command=generate_post
        ).pack(pady=20)
    #end of social post generator
    #show image lab
    def show_image_lab(self):

        utils.clear_view(self)

        ctk.CTkLabel(
            self.view,
            text="🖼 SD-Turbo Image Lab",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=20)

        prompt_entry = ctk.CTkEntry(
            self.view,
            placeholder_text="Describe the image you want...",
            width=500,
            height=50
        )
        prompt_entry.pack(pady=10)

        # generate button
        generate_btn = ctk.CTkButton(
            self.view,
            text="Generate Image",
            height=45
        )
        generate_btn.pack(pady=10)

        # preview frame
        preview_frame = ctk.CTkFrame(self.view, width=420, height=420)
        preview_frame.pack(pady=20)

        preview_frame.pack_propagate(False)

        loading_lbl = ctk.CTkLabel(
            preview_frame,
            text="",
            font=("Segoe UI",18)
        )
        loading_lbl.pack(expand=True)

        img_label = ctk.CTkLabel(preview_frame, text="")
        img_label.pack()

        # download button
        download_btn = ctk.CTkButton(
            self.view,
            text="⬇ Download Image",
            state="disabled"
        )
        download_btn.pack(pady=10)

        def download_image():

            from tkinter import filedialog
            from PIL import Image

            path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image","*.png")]
            )

            if path:
                Image.open(self.last_image_path).save(path)

        download_btn.configure(command=download_image)

        def generate_img():

            prompt = prompt_entry.get().strip()
            if not prompt:
                return

            loading_lbl.configure(text="⏳ Generating image...")
            generate_btn.configure(state="disabled")

            def task():

                path = self.image_gen.generate(prompt)

                if not path:
                    self.after(0, lambda: loading_lbl.configure(text="❌ Generation failed"))
                    self.after(0, lambda: generate_btn.configure(state="normal"))
                    return

                from PIL import Image

                pil = Image.open(path).convert("RGB")

                img = ctk.CTkImage(
                    light_image=pil,
                    dark_image=pil,
                    size=(400,400)
                )

                # store image like workstation
                self.last_image = img

                def display():

                    try:
                        if not self.winfo_exists():
                            return

                        if loading_lbl.winfo_exists():
                            loading_lbl.configure(text="")

                        if img_label.winfo_exists():
                            img_label.configure(image=img)
                            img_label.image = img

                        if download_btn.winfo_exists():
                            download_btn.configure(state="normal")

                        if generate_btn.winfo_exists():
                            generate_btn.configure(state="normal")

                    except Exception as e:
                        print("UI update skipped:", e)

                self.safe_after(0, display)

            threading.Thread(target=task, daemon=True).start()

        generate_btn.configure(command=generate_img)
    #end of image lab

    def show_voice_lab(self):
        utils.clear_view(self)

        ctk.CTkLabel(
            self.view,
            text="🎤 Voice Lab",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=20)

        self.voice_log = ctk.CTkTextbox(
            self.view,
            font=("Segoe UI", 14),
            height=250,
            corner_radius=12,
            border_width=2,
            border_color=get_theme_color("border")
        )
        self.voice_log.pack(expand=False, fill="x", padx=20, pady=10)
        self.voice_log.insert("1.0", "Voice transcriptions and AI responses will appear here.\n")

        self.voice_entry = ctk.CTkEntry(
            self.view,
            placeholder_text="Type text or use microphone",
            width=700,
            height=45,
            font=("Segoe UI", 14),
            corner_radius=15
        )
        self.voice_entry.pack(pady=10)

        self.voice_status = ctk.CTkLabel(
            self.view,
            text="Ready",
            font=("Segoe UI", 14, "bold"),
            text_color=get_theme_color("accent")
        )
        self.voice_status.pack(pady=(0, 10))

        commands_frame = ctk.CTkFrame(self.view, fg_color="transparent")
        commands_frame.pack(pady=5)

        record_btn = ctk.CTkButton(
            commands_frame,
            text="🎙️ Record Voice",
            width=170,
            command=self.start_speech_to_text
        )
        record_btn.pack(side="left", padx=8)

        send_btn = ctk.CTkButton(
            commands_frame,
            text="📩 Send to AI",
            width=150,
            command=self.handle_voice_query
        )
        send_btn.pack(side="left", padx=8)

        play_btn = ctk.CTkButton(
            commands_frame,
            text="🔊 Play Response",
            width=160,
            command=self.play_last_voice_response
        )
        play_btn.pack(side="left", padx=8)

        self.voice_response_text = ""

        stop_btn = ctk.CTkButton(
            commands_frame,
            text="⏹ Stop Voice",
            width=160,
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.stop_voice
        )
        stop_btn.pack(side="left", padx=8)

    def start_speech_to_text(self):
        self.stop_voice()
        def _record():
            try:
                import speech_recognition as sr
            except Exception as e:
                self.voice_status.configure(text="Install speechrecognition + pyaudio", text_color="#F59E0B")
                return

            recognizer = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    self.voice_status.configure(text="Listening...", text_color="#22C55E")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio_data = recognizer.listen(source, timeout=8, phrase_time_limit=20)
                self.voice_status.configure(text="Recognizing...", text_color="#FBBF24")

                text = recognizer.recognize_google(audio_data)
                self.voice_entry.delete(0, "end")
                self.voice_entry.insert(0, text)
                self._append_voice_log(f"User: {text}\n")
                self.voice_status.configure(text="Transcription complete", text_color="#22C55E")
            except Exception as e:
                self.voice_status.configure(text=f"Voice capture failed: {e}", text_color="#F87171")

        threading.Thread(target=_record, daemon=True).start()

    def handle_voice_query(self):
        query = self.voice_entry.get().strip()
        if not query:
            messagebox.showwarning("Input required", "Please input text or record your voice first.")
            return

        self._append_voice_log(f"User: {query}\n")
        self.voice_status.configure(text="Sending to AI...", text_color="#60A5FA")

        def _generate():
            if not self.ai:
                self.voice_status.configure(text="AI model not loaded yet", text_color="#F87171")
                return

            ai_response = self.ai.generate_text_for_prompt(query)
            if not ai_response:
                ai_response = "No response from AI."

            self.voice_response_text = ai_response
            self._append_voice_log(f"AI: {ai_response}\n")
            self.voice_status.configure(text="AI response ready", text_color="#22C55E")
            self.play_text(ai_response)

        threading.Thread(target=_generate, daemon=True).start()

    def play_last_voice_response(self):
        if not self.voice_response_text:
            messagebox.showinfo("No response", "Generate AI text first.")
            return
        self.play_text(self.voice_response_text)

    def play_text(self, text):
        try:
            import pyttsx3
        except Exception:
            self.voice_status.configure(
                text="Install pyttsx3 for text-to-speech",
                text_color="#F87171"
            )
            return

        def _speak():
            try:
                self.is_speaking = True

                # fresh engine every time 
                engine = pyttsx3.init()
                self.tts_engine = engine

                engine.say(text)
                engine.runAndWait()

            except Exception as e:
                self.voice_status.configure(
                    text=f"TTS failed: {e}",
                    text_color="#F87171"
                )
            finally:
                self.is_speaking = False
                self.tts_engine = None

        threading.Thread(target=_speak, daemon=True).start()

    def stop_voice(self):
        try:
            if self.tts_engine:
                self.tts_engine.stop()
                self.tts_engine = None

            self.is_speaking = False

            if hasattr(self, "voice_status"):
                self.voice_status.configure(
                    text="Speech stopped",
                    text_color="#F59E0B"
                )

        except Exception as e:
            print("Stop voice error:", e)

    def _append_voice_log(self, msg):
        try:
            self.voice_log.insert("end", msg)
            self.voice_log.see("end")
        except Exception:
            pass

    def show_trend_analysis(self):
        utils.clear_view(self)

        ctk.CTkLabel(
            self.view,
            text="🔥 Trend Explorer",
            font=("Segoe UI", 30, "bold")
        ).pack(pady=20)

        trend_entry = ctk.CTkEntry(
            self.view,
            placeholder_text="Search trends like dresses, songs, reels...",
            width=600,
            height=50
        )
        trend_entry.pack(pady=10)

        result_box = ctk.CTkTextbox(self.view, font=("Segoe UI", 14))
        result_box.pack(fill="both", expand=True, padx=20, pady=20)

        def refresh_trends():
            self.trend_generation_id += 1

            if self.trend_typing_job:
                try:
                    self.after_cancel(self.trend_typing_job)
                except:
                    pass

            trend_entry.delete(0, "end")
            result_box.delete("1.0", "end")
            result_box.insert("1.0", "✨ Ready for new task...\n")

        def find_trends():
            topic = trend_entry.get().strip()
            if not topic:
                return

            current_id = self.trend_generation_id + 1
            self.trend_generation_id = current_id

            if self.trend_typing_job:
                try:
                    self.after_cancel(self.trend_typing_job)
                except:
                    pass

            result_box.delete("1.0", "end")
            result_box.insert("1.0", "⏳ Finding trends...\n")

            def task():
                prompt = f"Give current trending ideas, styles, songs, and popular content around {topic}"
                response = self.ai.generate_text_for_prompt(prompt)

                def type_live():
                    result_box.delete("1.0", "end")
                    i = 0

                    def type_char():
                        nonlocal i

                        # stop old task if new refresh/search happens
                        if current_id != self.trend_generation_id:
                            return

                        if i < len(response):
                            result_box.insert("end", response[i])
                            result_box.see("end")
                            i += 1
                            self.trend_typing_job = self.after(5, type_char)

                    type_char()

                self.after(0, type_live)

            threading.Thread(target=task, daemon=True).start()

        button_frame = ctk.CTkFrame(self.view, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="🔥 Find Trends",
            command=find_trends
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=refresh_trends
        ).pack(side="left", padx=10)

    
    #end of voice lab

    def show_settings(self):
        utils.clear_view(self)

        ctk.CTkLabel(
            self.view,
            text="⚙ Settings",
            font=("Segoe UI", 32, "bold")
        ).pack(pady=30)

        ctk.CTkButton(
            self.view,
            text="Toggle Theme",
            command=lambda: theme.toggle_theme(self)
        ).pack(pady=10)

    def view_entry(self, content):
        utils.clear_view(self)

        # Top bar
        top_bar = ctk.CTkFrame(self.view, fg_color="transparent")
        top_bar.pack(fill="x", pady=10)

        back_btn = ctk.CTkButton(
            top_bar,
            text="⬅ Back to Vault",
            command=self.vault.show_vault,
            width=160
        )
        back_btn.pack(side="left", padx=20)

        title = ctk.CTkLabel(
            top_bar,
            text="📜 Vault Entry",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(side="left", padx=20)

        # Text viewer
        text_box = ctk.CTkTextbox(
            self.view,
            font=("Segoe UI", 14)
        )
        text_box.pack(expand=True, fill="both", padx=30, pady=20)

        text_box.insert("1.0", content)


# =============================== 
# APP ENTRY
# ===============================

if __name__ == "__main__":
    app = ContentIQ_Pro()
    app.mainloop()
