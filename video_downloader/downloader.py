"""
Download module for video-downloader.

Handles video/audio downloads using yt-dlp with progress tracking,
error handling, and configurable options.
"""

import os
import logging
import shutil
from typing import Optional, Dict, Any
from pathlib import Path

import yt_dlp
from rich.progress import Progress

from .auth import get_auth_options
from .exceptions import (
    DownloadError,
    NetworkError,
    FormatError,
    DependencyError,
)

logger = logging.getLogger(__name__)


class Downloader:
    """Handles video and audio downloads with progress tracking."""

    def __init__(self, progress: Progress):
        """
        Initialize downloader.

        Args:
            progress: Rich Progress instance for UI feedback
        """
        self.progress = progress
        self.task_id = None
        self._verify_dependencies()

    def _verify_dependencies(self) -> None:
        """
        Verify that required external dependencies are installed.

        Raises:
            DependencyError: If required dependencies are missing
        """
        # Check for ffmpeg (required for audio conversion and video merging)
        if not shutil.which("ffmpeg"):
            raise DependencyError(
                "ffmpeg is not installed. Please install it:\n"
                "  Arch Linux: sudo pacman -S ffmpeg\n"
                "  Gentoo: sudo emerge media-video/ffmpeg"
            )

    def _hook(self, d: Dict[str, Any]) -> None:
        """
        Progress hook for yt-dlp downloads.

        Args:
            d: Download status dictionary from yt-dlp
        """
        status = d.get("status")

        if status == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate")

            if self.task_id is None:
                # Create progress task with total size (if available)
                self.task_id = self.progress.add_task(
                    "[cyan]Downloading...",
                    total=total_bytes if total_bytes else 100,
                )

            downloaded = d.get("downloaded_bytes", 0)

            # Handle streams without known size
            if total_bytes:
                self.progress.update(self.task_id, completed=downloaded, total=total_bytes)
            else:
                # Show indeterminate progress
                percentage = min(downloaded / 1_000_000, 100)  # Rough estimate
                self.progress.update(self.task_id, completed=percentage, total=100)

        elif status == "finished":
            if self.task_id is not None:
                total = self.progress.tasks[self.task_id].total or 100
                self.progress.update(
                    self.task_id,
                    completed=total,
                    description="[green]Download complete!",
                )

        elif status == "error":
            if self.task_id is not None:
                self.progress.update(
                    self.task_id,
                    description="[red]Download failed!",
                )

    def download(
        self,
        url: str,
        download_path: str,
        is_audio: bool = False,
        cookies_path: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        site: Optional[str] = None,
        audio_quality: str = "192",
        verify_ssl: bool = True,
        max_retries: int = 3,
        timeout: int = 30,
        use_cookies: bool = True,
    ) -> None:
        """
        Execute download using yt-dlp.

        Args:
            url: Video/audio URL to download
            download_path: Destination directory
            is_audio: Whether to extract audio only
            cookies_path: Path to browser cookies file (optional)
            username: Direct username for authentication (overrides stored)
            password: Direct password for authentication (overrides stored)
            site: Site identifier for stored credentials
            audio_quality: Audio bitrate in kbps (default: 192)
            verify_ssl: Whether to verify SSL certificates (default: True)
            max_retries: Maximum number of retry attempts (default: 3)
            timeout: Socket timeout in seconds (default: 30)
            use_cookies: Whether to use cookies at all (default: True)

        Raises:
            DownloadError: If download fails
            NetworkError: If network-related error occurs
            FormatError: If requested format is not available
        """
        # Ensure download path exists
        Path(download_path).mkdir(parents=True, exist_ok=True)

        # Build yt-dlp options
        ydl_opts = {
            "format": self._get_format_string(is_audio),
            "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            "progress_hooks": [self._hook],
            "retries": max_retries,
            "socket_timeout": timeout,
            "nocheckcertificate": not verify_ssl,  # Only disable if explicitly requested
            "concurrent_fragment_downloads": 16,
            "quiet": True,
            "no_warnings": False,
        }

        # Add audio post-processing if needed
        if is_audio:
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": str(audio_quality),
                }
            ]

        # Authentication: prioritize non-cookie methods
        if username and password:
            # Direct credentials (highest priority)
            ydl_opts["username"] = username
            ydl_opts["password"] = password
            logger.info("Using provided username/password")
        elif site:
            # Stored credentials (second priority)
            auth_opts = get_auth_options(site=site, use_credentials=True)
            ydl_opts.update(auth_opts)
        elif cookies_path and use_cookies:
            # Cookies as fallback (lowest priority)
            ydl_opts["cookiefile"] = cookies_path
            logger.info("Using cookies file for authentication")
        elif not use_cookies:
            logger.info("Running without authentication (no-cookie mode)")

        # Execute download
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Starting download from: {url}")
                ydl.download([url])
                logger.info("Download completed successfully")

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            logger.error(f"Download failed: {error_msg}")

            # Categorize errors for better user feedback
            if "network" in error_msg.lower() or "connection" in error_msg.lower():
                raise NetworkError(f"Network error: {error_msg}") from e
            elif "format" in error_msg.lower() or "video" in error_msg.lower():
                raise FormatError(f"Format error: {error_msg}") from e
            else:
                raise DownloadError(f"Download failed: {error_msg}") from e

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise DownloadError(f"Unexpected error: {e}") from e

    @staticmethod
    def _get_format_string(is_audio: bool) -> str:
        """
        Get format string for yt-dlp based on download type.

        Args:
            is_audio: Whether downloading audio only

        Returns:
            yt-dlp format string
        """
        if is_audio:
            return "bestaudio/best"
        else:
            # Prefer MP4 container with best quality
            return "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
