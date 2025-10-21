"""
Custom exceptions for video-downloader.

Provides specific exception types for better error handling and user feedback.
"""


class VideoDownloaderError(Exception):
    """Base exception for all video-downloader errors."""
    pass


class DownloadError(VideoDownloaderError):
    """Raised when a download fails for any reason."""
    pass


class NetworkError(DownloadError):
    """Raised when network-related errors occur (connection, timeout, etc.)."""
    pass


class FormatError(DownloadError):
    """Raised when requested format is not available or invalid."""
    pass


class DependencyError(VideoDownloaderError):
    """Raised when required external dependencies are missing."""
    pass


class AuthenticationError(VideoDownloaderError):
    """Raised when authentication fails."""
    pass


class ValidationError(VideoDownloaderError):
    """Raised when input validation fails."""
    pass
