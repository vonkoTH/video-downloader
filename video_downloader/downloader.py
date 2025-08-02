import os
import yt_dlp
from rich.progress import Progress

class Downloader:
    def __init__(self, progress: Progress):
        self.progress = progress
        self.task_id = None

    def _hook(self, d):
        if d["status"] == "downloading":
            if self.task_id is None:
                self.task_id = self.progress.add_task(
                    "[cyan]Downloading...", total=d.get("total_bytes")
                )
            self.progress.update(
                self.task_id, completed=d["downloaded_bytes"], total=d.get("total_bytes")
            )
        elif d["status"] == "finished":
            if self.task_id is not None:
                self.progress.update(
                    self.task_id, completed=d.get("total_bytes"), description="[green]Download complete!"
                )

    def download(
        self,
        url: str,
        download_path: str,
        is_audio: bool,
        cookies_path: str | None = None,
    ):
        """Executes the download using yt-dlp."""
        ydl_opts = {
            "format": "bestaudio/best"
            if is_audio
            else "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            "progress_hooks": [self._hook],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
            if is_audio
            else [],
            "nocheckcertificate": True,
            "concurrent_fragments": 16,
        }

        if cookies_path:
            ydl_opts["cookiefile"] = cookies_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])