"""
Authentication module for video-downloader.

Provides cookie-free authentication methods:
- Username/password authentication
- Secure credential storage
- Environment variable support
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict
from base64 import b64encode, b64decode

logger = logging.getLogger(__name__)


class CredentialManager:
    """Manages authentication credentials without relying on browser cookies."""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize credential manager.

        Args:
            config_dir: Custom config directory. Defaults to ~/.config/video-downloader
        """
        if config_dir is None:
            config_dir = Path.home() / ".config" / "video-downloader"

        self.config_dir = config_dir
        self.credentials_file = config_dir / "credentials.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Create config directory if it doesn't exist with secure permissions."""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, mode=0o700)
            logger.info(f"Created config directory: {self.config_dir}")

    def save_credentials(self, site: str, username: str, password: str) -> None:
        """
        Save credentials for a specific site.

        Args:
            site: Site identifier (e.g., 'youtube', 'tiktok')
            username: Username for authentication
            password: Password for authentication

        Note:
            Credentials are base64 encoded (not encryption, just obfuscation).
            For production, consider using keyring library for OS-level encryption.
        """
        credentials = self._load_credentials_file()

        # Simple obfuscation (NOT encryption - use keyring for production)
        credentials[site] = {
            "username": b64encode(username.encode()).decode(),
            "password": b64encode(password.encode()).decode(),
        }

        # Write with secure permissions
        self.credentials_file.write_text(json.dumps(credentials, indent=2))
        self.credentials_file.chmod(0o600)
        logger.info(f"Saved credentials for site: {site}")

    def get_credentials(self, site: str) -> Optional[Dict[str, str]]:
        """
        Retrieve credentials for a specific site.

        Args:
            site: Site identifier

        Returns:
            Dictionary with 'username' and 'password' keys, or None if not found
        """
        # First check environment variables
        env_username = os.getenv(f"VIDEO_DOWNLOADER_{site.upper()}_USERNAME")
        env_password = os.getenv(f"VIDEO_DOWNLOADER_{site.upper()}_PASSWORD")

        if env_username and env_password:
            logger.info(f"Using credentials from environment for: {site}")
            return {"username": env_username, "password": env_password}

        # Fall back to stored credentials
        credentials = self._load_credentials_file()

        if site not in credentials:
            logger.debug(f"No credentials found for site: {site}")
            return None

        # Decode obfuscated credentials
        stored = credentials[site]
        return {
            "username": b64decode(stored["username"]).decode(),
            "password": b64decode(stored["password"]).decode(),
        }

    def remove_credentials(self, site: str) -> bool:
        """
        Remove credentials for a specific site.

        Args:
            site: Site identifier

        Returns:
            True if credentials were removed, False if they didn't exist
        """
        credentials = self._load_credentials_file()

        if site in credentials:
            del credentials[site]
            self.credentials_file.write_text(json.dumps(credentials, indent=2))
            logger.info(f"Removed credentials for site: {site}")
            return True

        return False

    def list_sites(self) -> list:
        """
        List all sites with stored credentials.

        Returns:
            List of site identifiers
        """
        credentials = self._load_credentials_file()
        return list(credentials.keys())

    def _load_credentials_file(self) -> Dict:
        """Load credentials from file or return empty dict."""
        if not self.credentials_file.exists():
            return {}

        try:
            return json.loads(self.credentials_file.read_text())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse credentials file: {e}")
            return {}


def get_auth_options(
    site: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    use_credentials: bool = True,
) -> Dict:
    """
    Get authentication options for yt-dlp without using cookies.

    Args:
        site: Site identifier for stored credentials
        username: Direct username (overrides stored)
        password: Direct password (overrides stored)
        use_credentials: Whether to use stored credentials

    Returns:
        Dictionary with yt-dlp authentication options
    """
    auth_opts = {}

    # Direct username/password takes precedence
    if username and password:
        auth_opts["username"] = username
        auth_opts["password"] = password
        logger.info("Using provided username/password for authentication")
        return auth_opts

    # Try to load stored credentials
    if use_credentials and site:
        manager = CredentialManager()
        creds = manager.get_credentials(site)
        if creds:
            auth_opts["username"] = creds["username"]
            auth_opts["password"] = creds["password"]
            logger.info(f"Using stored credentials for site: {site}")

    return auth_opts
