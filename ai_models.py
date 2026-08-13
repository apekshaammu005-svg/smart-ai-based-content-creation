import os
import time
import torch
from diffusers import StableDiffusionPipeline
from gpt4all import GPT4All
from PIL import Image
import customtkinter as ctk
import threading 
from image_generator import ImageGenerator


class AIModels:
    def __init__(self, app, model_name):
        self.app = app
        self.model_name = model_name
        self.local_model = None
        self.sd_pipe = None
        self.image_gen = app.image_gen
        self.model_lock = threading.Lock()

    # ===============================
    # MODEL & UTILS (preload_engine, preload_sd)
    # ===============================
    def preload_engine(self):
        """Original preload_engine logic, but bound to app/local_model."""
        try:
            if GPT4All and os.path.exists(self.model_name):
                self.local_model = GPT4All(
                    self.model_name,
                    model_path=".",
                    device="cpu",
                )
                # expose to app so start_ai can check app.local_model
                self.app.local_model = self.local_model
                print("✅ Engine Loaded on CPU")
            else:
                print("❌ Model file not found or GPT4All not installed.")
        except Exception as e:
            print(f"❌ Load Error: {e}")

    def finish_live_ui(self):
        app = self.app

        app.is_generating = False
        app.gen_btn.configure(state="normal", text="✨ GENERATE MAGIC")
        app.stop_btn.configure(state="disabled")
        app.save_vault_btn.pack(side="left", padx=10)
        app.spinner_frame.pack_forget()
        if app.last_content:
            app.after(1000,app.workstation.open_result_window) 

    def preload_sd(self):                                                                   
        """Original preload_sd logic, but bound to app.sd_status."""
        try:
            print("Loading SD Turbo....")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float32  # Force float32 for CPU stability

            self.sd_pipe = StableDiffusionPipeline.from_pretrained(
                "stabilityai/sd-turbo",
                torch_dtype=dtype,
                safety_checker=None,
                requires_safety_checker=False,
            )
            self.sd_pipe = self.sd_pipe.to(device)

            if device == "cpu":
                self.sd_pipe.enable_model_cpu_offload()
                self.sd_pipe.enable_vae_slicing()

            self.sd_pipe.enable_attention_slicing()
            self.sd_pipe.vae.config.force_upcast = True

            print(f"✅ SD Turbo Loaded on {device}")
            self.app.after(
                0,
                lambda: self.app.sd_status.configure(
                    text=" ✅ SD Turbo Ready ✓"
                )
            )
        except Exception as e:
            print("❌ SD Load Error:", e)

    # ===============================
    # IMAGE GENERATION (generate_image, generate_image_bg)
    # ===============================
    def generate_image(self, prompt):
        try:
            return self.image_gen.generate(prompt)
        except Exception as e:
            print("Image generation error:", e)
            return None
        
    def generate_script(self):
        if hasattr(self, "topic_entry") and self.topic_entry.winfo_exists():
            self.topic_entry.delete(0, "end")
            self.topic_entry.insert(0, "Write a YouTube script about ")

    def generate_image_bg(self, topic):
        """Background image gen - doesn't block text (original logic)."""
        app = self.app
        try:
            path = self.generate_image(topic)
            if path:
                pil_img = Image.open(path).convert("RGB")
                img = ctk.CTkImage(
                    light_image=pil_img,
                    dark_image=pil_img,
                    size=(400, 400),
                )
                app.last_image = img
                # original: self.after(0, lambda: self.show_image_preview(img))
                app.after(0, lambda: app.workstation.show_image_preview(img))
                if hasattr(app, "sd_status"):
                    app.after(
                        0,
                        lambda: app.sd_status.configure(
                            text="🖼️ SD Turbo Ready ✓ | Image Generated ✓ "
                        )
                    )
        except Exception as e:
            print("Image BG error:", e)
            if hasattr(app, "sd_status"):
                app.sd_status.configure(text="🖼️ Image Error")

    # ===============================
    # TEXT GENERATION (generate_text_only x2, run_full_generation)
    # ===============================
    
   
        
    def generate_text_only_fast(self, topic):
        app = self.app

        prompt = (
            f"You are a professional AI content writer.\n\n"
            f"Write a high quality {app.asset_type.get()} about: {topic}\n\n"
            "Make the writing:\n"
            "- Clear\n"
            "- Engaging\n"
            "- Well structured\n"
            "- Professional\n"
        )

        generated_text = ""

        with self.model_lock:
            with self.local_model.chat_session():
                stream = self.local_model.generate(
                    prompt,
                    max_tokens=int(app.max_tokens.get()),
                    temp=0.7,
                    top_k=10,
                    top_p=0.9,
                    repeat_penalty=1.1,
                    streaming=True
                )

                for chunk in stream:
                    if app.stop_requested:
                        break

                    chunk = str(chunk)
                    generated_text += chunk

                    app.after(
                        0,
                        lambda text_chunk=chunk: (
                            app.output.insert("end", text_chunk),
                            app.output.see("end")
                        )
                    )

        app.last_content = {
            "topic": topic,
            "content": generated_text,
            "fav": False,
            "user": app.current_user,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        app.after(0, self.finish_live_ui)
    #end

    def generate_text_only(self, topic):
        """
        Second version at bottom of original file (same logic, different prompt string).
        """
        app = self.app
        prompt = f"""
You are a professional AI content writer.

Write a high quality {app.asset_type.get()} about: {topic}

Make the writing:
- Clear
- Engaging
- Well structured
- Professional
"""
        with self.model_lock:
            res = self.local_model.generate(
                prompt,
                max_tokens=700,
                temp=0.7,
                top_k=40,
                top_p=0.9,
    )

        generated_text = res.strip()
        app.last_content = {
            "topic": topic,
            "content": generated_text,
            "fav": False,
            "user": app.current_user,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        app.after(0, lambda: app.workstation.finish_generation(generated_text))

    def run_full_generation(self, topic):
        """
        Original run_full_generation moved here.
        Called from Workstation.start_ai via app.ai.run_full_generation(topic)
        OR you can still keep a wrapper in ContentIQ_Pro that calls this.
        """
        app = self.app
        try:
            # TEXT ALWAYS (fast)
            text_thread = threading.Thread(
                target=self.generate_text_only_fast,
                args=(topic,),
                daemon=True,
            )
            text_thread.start()

            # OPTIONAL IMAGE (parallel, slow)
            if app.gen_image_cb.get():
                app.after(
                    0,
                    lambda: app.output.insert(
                        "end",
                        "🖼️ Image generating in background...\n",
                    ),
                )
                image_thread = threading.Thread(
                    target=self.generate_image_bg,
                    args=(topic,),
                    daemon=True,
                )
                image_thread.start()
            

        except Exception as e:
            print("Generation error:", e)

    def generate_text_for_prompt(self, prompt, max_tokens=450):
        """General-purpose text response for Voice Lab or chat modes."""
        if not self.local_model:
            return None

        try:
            with self.model_lock:
                if hasattr(self.local_model, "chat_session"):
                    with self.local_model.chat_session():
                        res = self.local_model.generate(
                            prompt,
                            max_tokens=max_tokens,
                            temp=0.7,
                            top_k=40,
                            top_p=0.9,
                        )
                else:
                    res = self.local_model.generate(
                        prompt,
                        max_tokens=max_tokens,
                        temp=0.7,
                        top_k=40,
                        top_p=0.9,
                    )

            return str(res).strip()
        except Exception as e:
            print("Voice prompt generation error:", e)
            return None

    def analyze_trends(self, vault_data):
        """Analyze vault for content trends using LLM."""
        if not self.local_model:
            return "AI model not loaded."

        if not vault_data:
            return "No saved content for analysis."

        recent_topics = [item.get('topic', 'N/A') for item in vault_data[-10:]]
        summary = ', '.join(recent_topics)

        prompt = f"""You are a trend analyst. Analyze these user's recent content topics: {summary}

Generate insights:
1. Dominant themes
2. Emerging patterns
3. 3 trending content ideas
4. Keyword suggestions

Concise bullet points."""

        try:
            with self.model_lock:
                res = self.local_model.generate(
                    prompt,
                    max_tokens=500,
                    temp=0.6,
                    top_p=0.9
                )
            return str(res).strip()
        except Exception as e:
            print(f"Trend analysis error: {e}")
            return "Analysis unavailable."

