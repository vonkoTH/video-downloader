import customtkinter as ctk
import threading
import yt_dlp
import os
from tkinter import filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Main Window Configuration ---
        self.title("Video and Audio Downloader")
        self.geometry("700x450")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # --- State Variables ---
        self.download_path = os.path.expanduser("~/Downloads")  # Default to user's Downloads folder
        self.cookies_path = None

        # --- UI Widgets ---
        self.create_widgets()

    def create_widgets(self):
        # --- Input Frame ---
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=15, padx=20, fill="x")

        url_label = ctk.CTkLabel(input_frame, text="Video URL:")
        url_label.pack(pady=5)

        self.url_entry = ctk.CTkEntry(input_frame, width=400, placeholder_text="Paste the video URL here")
        self.url_entry.pack(pady=5, padx=10, fill="x", expand=True)

        # --- Options Frame ---
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=10, padx=20, fill="x")

        # Format Selection
        format_label = ctk.CTkLabel(options_frame, text="Format:")
        format_label.pack(side="left", padx=(10, 5))
        self.format_combobox = ctk.CTkComboBox(options_frame, values=["Video (MP4)", "Audio (MP3)"])
        self.format_combobox.set("Video (MP4)")
        self.format_combobox.pack(side="left", padx=(0, 10))

        # Directory Selection Button
        self.select_dir_button = ctk.CTkButton(options_frame, text="Select Folder", command=self.select_directory)
        self.select_dir_button.pack(side="right", padx=10)

        # Cookies Selection Button
        self.select_cookies_button = ctk.CTkButton(options_frame, text="Select Cookies", command=self.select_cookies)
        self.select_cookies_button.pack(side="right", padx=10)

        # Label to display the download path
        self.path_label = ctk.CTkLabel(self, text=f"Saving to: {self.download_path}", wraplength=650)
        self.path_label.pack(pady=10, padx=20)

        # --- Download Button ---
        self.download_button = ctk.CTkButton(self, text="Download", command=self.start_download_thread, height=40)
        self.download_button.pack(pady=20, padx=20, fill="x")

        # --- Progress Frame ---
        progress_frame = ctk.CTkFrame(self)
        progress_frame.pack(pady=10, padx=20, fill="x")

        self.progress_label = ctk.CTkLabel(progress_frame, text="Progress: 0%")
        self.progress_label.pack(pady=(5, 0))
try.get()
        if not url:
            self.status_label.configure(text="Error: Please enter a valid URL.", text_color="orange")
            return

        self.set_ui_state("disabled")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Progress: 0%")
        self.status_label.configure(text="Initiating download...", text_color="white")

        download_thread = threading.Thread(target=self.download, args=(url,))
        download_thread.start()

    def download(self, url):
        """Executes the download using yt-dlp."""
        try:
            is_audio = self.format_combobox.get() == "Audio (MP3)"
            ydl_opts = {
                'format': 'bestaudio/best' if is_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.on_progress],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if is_audio else [],
                'nocheckcertificate': True,
            'concurrent_fragments': 4, # increasing this, you can boost the download speed without losing quality.
            }

            if self.cookies_path:
                ydl_opts['cookies'] = self.cookies_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except Exception as e:
            self.status_label.configure(text=f"Download Error: {str(e)}", text_color="red")
        finally:
            self.set_ui_state("normal")

    def on_progress(self, d):
        """Hook to update the progress bar."""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                percentage = d['downloaded_bytes'] / total_bytes
                self.progress_bar.set(percentage)
                self.progress_label.configure(text=f"Progress: {percentage:.0%}")
        elif d['status'] == 'finished':
            self.status_label.configure(text="Download completed successfully!", text_color="green")
            self.progress_bar.set(1)
            self.progress_label.configure(text="Progress: 100%")


    def set_ui_state(self, state):
        """Enables or disables the UI widgets."""
        self.download_button.configure(state=state)
        self.url_entry.configure(state=state)
        self.format_combobox.configure(state=state)
        self.select_dir_button.configure(state=state)
        self.select_cookies_button.configure(state=state)

if __name__ == "__main__":
    app = App()
    app.mainloop()
