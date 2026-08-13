import time
import torch
from diffusers import StableDiffusionPipeline
import os


class ImageGenerator:

    def __init__(self,app):
        self.app = app
        self.pipe = None

    def load_model(self):

        print("Loading SD Turbo...")

        device = "cuda" if torch.cuda.is_available() else "cpu"

        # FORCE float32 as you requested
        dtype = torch.float32

        self.pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/sd-turbo",
            torch_dtype=dtype,
            safety_checker=None,
            requires_safety_checker=False,
        ).to(device)

        # Stabilizers (important)
        self.pipe.enable_attention_slicing()

        if device == "cpu":
            self.pipe.enable_model_cpu_offload()
            self.pipe.enable_vae_slicing()

        # Fix black images
        self.pipe.vae.config.force_upcast = True

        print(f"SD Turbo loaded on {device}")

    def generate(self, prompt):

        if self.pipe is None:
            print("Model not loaded. Loading now...")
            self.load_model()

        device = "cuda" if torch.cuda.is_available() else "cpu"

        generator = torch.Generator(device=device).manual_seed(int(time.time()))

        image = self.pipe(
            prompt=prompt,
            height=256,
            width=256,
            num_inference_steps=2,
            guidance_scale=0,
            generator=generator,
        ).images[0]

        image = image.convert("RGB")

        filename = f"img_{int(time.time())}.png"
        path = os.path.join(self.app.image_dir, filename)

        image.save(path)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return path
    
    
   