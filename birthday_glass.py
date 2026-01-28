import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont
import math
import random

class GlassBirthdayCard:
    def __init__(self, root):
        self.root = root
        self.root.title("Happy Birthday!")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # 1. Configuration
        self.bg_color_1 = (255, 107, 107)  # Coral
        self.bg_color_2 = (78, 205, 196)   # Teal
        self.glass_color = (255, 255, 255, 100) # White with transparency
        self.text_color = (255, 255, 255)
        
        # 2. Canvas Setup
        self.canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # 3. Generate Assets
        self.create_dynamic_background()
        self.create_glass_panel()
        
        # 4. Render
        self.render_frame()
        
        # 5. Add Text (GUI Overlay)
        self.add_text()
        
        # 6. Start Particle Animation
        self.particles = []
        self.animate()

    def create_dynamic_background(self):
        """Creates a gradient background with floating orbs."""
        # Create base image
        self.base_image = Image.new("RGB", (800, 600), self.bg_color_1)
        draw = ImageDraw.Draw(self.base_image)
        
        # Draw gradient orbs
        for _ in range(10):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            r = random.randint(100, 300)
            draw.ellipse((x-r, y-r, x+r, y+r), fill=self.bg_color_2, outline=None)
            
        # Blur the background to make it dreamy
        self.base_image = self.base_image.filter(ImageFilter.GaussianBlur(radius=50))

    def create_glass_panel(self):
        """Creates the frosted glass effect."""
        # 1. Crop the area where the glass will be (Center)
        glass_w, glass_h = 500, 300
        x1 = (800 - glass_w) // 2
        y1 = (600 - glass_h) // 2
        
        # 2. Crop and Blur heavily
        glass_region = self.base_image.crop((x1, y1, x1+glass_w, y1+glass_h))
        glass_region = glass_region.filter(ImageFilter.GaussianBlur(radius=20))
        
        # 3. Add White Tint (The "Glass" surface)
        overlay = Image.new("RGBA", glass_region.size, self.glass_color)
        glass_region = glass_region.convert("RGBA")
        glass_region = Image.alpha_composite(glass_region, overlay)
        
        # 4. Add Border (Shine)
        draw = ImageDraw.Draw(glass_region)
        draw.rectangle((0, 0, glass_w-1, glass_h-1), outline=(255, 255, 255, 150), width=2)
        
        # 5. Paste glass back onto base image
        self.final_image = self.base_image.convert("RGBA")
        self.final_image.paste(glass_region, (x1, y1))

    def render_frame(self):
        """Converts PIL image to Tkinter image."""
        self.tk_image = ImageTk.PhotoImage(self.final_image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

    def add_text(self):
        """Adds text on top of the glass panel."""
        custom_font = font.Font(family="Helvetica", size=30, weight="bold")
        sub_font = font.Font(family="Helvetica", size=14)
        
        # Main Wish
        self.canvas.create_text(400, 280, text="Happy Birthday!", 
                                font=custom_font, fill="white", tags="text")
        # Subtext
        self.canvas.create_text(400, 330, text="Wishing you a year of clear vision\nand zero merge conflicts.", 
                                font=sub_font, fill="#f0f0f0", justify="center", tags="text")

    def animate(self):
        """Simple particle animation loop."""
        if len(self.particles) < 30:
            x = random.randint(0, 800)
            y = 600
            speed = random.uniform(2, 5)
            self.particles.append([x, y, speed])

        for p in self.particles:
            p[1] -= p[2] # Move up
            # Draw particle
            self.canvas.create_oval(p[0], p[1], p[0]+3, p[1]+3, fill="white", outline="")
            
            if p[1] < 0:
                self.particles.remove(p)

        self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = GlassBirthdayCard(root)
    root.mainloop()
      
