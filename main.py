import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from moviepy.editor import VideoFileClip
from PIL import Image

class GifMaker:
    def __init__(self, root):
        self.root = root
        self.root.title('GIF Maker')

        self.video_button = tk.Button(root, text="Convert Video to GIF", command=self.video_to_gif)
        self.video_button.pack(pady=20)

        self.images_button = tk.Button(root, text="Combine Images to GIF", command=self.images_to_gif)
        self.images_button.pack(pady=20)

    def video_to_gif(self):
        video_path = filedialog.askopenfilename(title="Select video file", filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
        if not video_path:
            return
        start_time = simpledialog.askfloat("Input", "Enter start time (in seconds):")
        end_time = simpledialog.askfloat("Input", "Enter end time (in seconds):")
        loop_duration = simpledialog.askinteger("Input", "Enter loop duration (0 for infinite):")
        gif_path = filedialog.asksaveasfilename(title="Save gif as", defaultextension=".gif", filetypes=[("GIF Files", "*.gif")])
        
        if gif_path:
            clip = VideoFileClip(video_path).subclip(start_time, end_time)
            clip.write_gif(gif_path, fps=15, loop=loop_duration)
            messagebox.showinfo("Success", "GIF created successfully!")

    def images_to_gif(self):
        images_list = filedialog.askopenfilenames(title="Select images to combine", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not images_list or len(images_list) < 2 or len(images_list) > 10:
            messagebox.showerror("Error", "Please select at least 2 and at most 10 images.")
            return
        
        duration_per_frame = simpledialog.askinteger("Input", "Enter duration per frame in milliseconds (e.g., 500 for half a second):")
        loop_duration = simpledialog.askinteger("Input", "Enter loop duration (0 for infinite):")
        gif_path = filedialog.asksaveasfilename(title="Save gif as", defaultextension=".gif", filetypes=[("GIF Files", "*.gif")])
        
        if gif_path:
            # Open the first image and set the size based on its dimensions
            base_img = Image.open(images_list[0])
            img_width, img_height = base_img.size
            
            # Resize all images to match the first image's size
            imgs = [base_img] + [Image.open(img_path).resize((img_width, img_height)) for img_path in images_list[1:]]
            
            # Save them as GIF
            imgs[0].save(gif_path, append_images=imgs[1:], save_all=True, duration=duration_per_frame, loop=loop_duration)
            messagebox.showinfo("Success", "GIF created successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GifMaker(root)
    root.mainloop()
