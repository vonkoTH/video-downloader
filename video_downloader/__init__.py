"""
video-downloader: A CLI tool to download video and audio from various web sources.

This package provides a command-line interface for downloading videos and audio
from various web sources using yt-dlp, with support for multiple authentication
methods and progress tracking.
"""

from .downloader import Downloader
from .auth import CredentialManager, get_auth_options
from .exceptions import (
    VideoDownloaderError,
    DownloadError,
    NetworkError,
    FormatError,
    DependencyError,
    AuthenticationError,
    ValidationError,
)

__version__ = "2.0.0"
__all__ = [
    "Downloader",
    "CredentialManager",
    "get_auth_options",
    "VideoDownloaderError",
    "DownloadError",
    "NetworkError",
    "FormatError",
    "DependencyError",
    "AuthenticationError",
    "ValidationError",
]
