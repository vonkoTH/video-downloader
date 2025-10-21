"""
CLI interface for video-downloader.

Provides command-line interface for downloading videos and audio
with multiple authentication methods and configuration options.
"""

import os
import sys
import logging
from typing import Optional
from urllib.parse import urlparse

import click
from rich.progress import Progress
from rich.console import Console
from rich.logging import RichHandler

from .downloader import Downloader
from .exceptions import (
    DownloadError,
    NetworkError,
    FormatError,
    DependencyError,
    ValidationError,
)

# Setup logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)
logger = logging.getLogger(__name__)
console = Console()


def validate_url(ctx, param, value: str) -> str:
    """
    Validate URL format.

    Args:
        ctx: Click context
        param: Click parameter
        value: URL string to validate

    Returns:
        Validated URL

    Raises:
        click.BadParameter: If URL is invalid
    """
    try:
        result = urlparse(value)
        if not all([result.scheme, result.netloc]):
            raise click.BadParameter(
                "Invalid URL. Must include scheme (http/https) and domain."
            )
        if result.scheme not in ["http", "https"]:
            raise click.BadParameter("URL must use http or https protocol.")
        return value
    except Exception as e:
        raise click.BadParameter(f"Invalid URL: {e}") from e


@click.command()
@click.argument("url", callback=validate_url)
@click.option(
    "-f",
    "--format",
    "download_format",
    type=click.Choice(["video", "audio"], case_sensitive=False),
    default="video",
    help="Download format (video or audio).",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    default=os.path.expanduser("~/Downloads"),
    help="Output directory.",
)
@click.option(
    "-c",
    "--cookies",
    "cookies_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Path to a browser cookies file (fallback method).",
)
@click.option(
    "-u",
    "--username",
    help="Username for authentication (preferred over cookies).",
)
@click.option(
    "-p",
    "--password",
    help="Password for authentication (use with --username).",
)
@click.option(
    "-s",
    "--site",
    help="Site identifier for stored credentials (e.g., 'youtube', 'tiktok').",
)
@click.option(
    "--no-cookies",
    is_flag=True,
    help="Disable cookie-based authentication entirely.",
)
@click.option(
    "--no-check-certificate",
    is_flag=True,
    help="Disable SSL certificate verification (insecure, not recommended).",
)
@click.option(
    "--audio-quality",
    default="192",
    help="Audio bitrate in kbps (default: 192).",
)
@click.option(
    "--retries",
    default=3,
    type=int,
    help="Maximum number of retry attempts (default: 3).",
)
@click.option(
    "--timeout",
    default=30,
    type=int,
    help="Socket timeout in seconds (default: 30).",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose logging.",
)
def main(
    url: str,
    download_format: str,
    output_path: str,
    cookies_path: Optional[str],
    username: Optional[str],
    password: Optional[str],
    site: Optional[str],
    no_cookies: bool,
    no_check_certificate: bool,
    audio_quality: str,
    retries: int,
    timeout: int,
    verbose: bool,
) -> None:
    """
    A CLI tool to download video and audio from various web sources.

    Supports multiple authentication methods (in priority order):
    1. Username/password (--username and --password)
    2. Stored credentials (--site)
    3. Browser cookies (--cookies)
    4. No authentication (--no-cookies)

    Examples:

        # Download video to Downloads folder
        video-download "https://www.youtube.com/watch?v=example"

        # Download audio with username/password
        video-download -f audio -u myuser -p mypass "https://example.com/video"

        # Download using stored credentials
        video-download --site youtube "https://www.youtube.com/watch?v=example"

        # Download without any authentication
        video-download --no-cookies "https://www.youtube.com/watch?v=example"
    """
    # Set logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    # Validate authentication options
    if username and not password:
        console.print("[red]Error: --password is required when using --username[/red]")
        sys.exit(1)

    if password and not username:
        console.print("[red]Error: --username is required when using --password[/red]")
        sys.exit(1)

    # Warn about insecure options
    if no_check_certificate:
        console.print(
            "[yellow]Warning: SSL certificate verification is disabled. "
            "This is insecure and not recommended.[/yellow]"
        )

    # Convert format to boolean
    is_audio = download_format.lower() == "audio"

    # Display configuration
    logger.info(f"Download format: {download_format}")
    logger.info(f"Output directory: {output_path}")

    if username:
        logger.info("Authentication: username/password")
    elif site:
        logger.info(f"Authentication: stored credentials for '{site}'")
    elif cookies_path:
        logger.info("Authentication: browser cookies")
    elif no_cookies:
        logger.info("Authentication: none (public content only)")

    # Execute download
    with Progress() as progress:
        try:
            downloader = Downloader(progress)
            downloader.download(
                url=url,
                download_path=output_path,
                is_audio=is_audio,
                cookies_path=cookies_path,
                username=username,
                password=password,
                site=site,
                audio_quality=audio_quality,
                verify_ssl=not no_check_certificate,
                max_retries=retries,
                timeout=timeout,
                use_cookies=not no_cookies,
            )
            console.print("[green]✓ Download completed successfully![/green]")

        except DependencyError as e:
            console.print(f"[red]Dependency Error:[/red] {e}")
            sys.exit(2)

        except ValidationError as e:
            console.print(f"[red]Validation Error:[/red] {e}")
            sys.exit(3)

        except NetworkError as e:
            console.print(
                f"[red]Network Error:[/red] {e}\n"
                f"[yellow]Tip: Check your internet connection and try again.[/yellow]"
            )
            sys.exit(4)

        except FormatError as e:
            console.print(
                f"[red]Format Error:[/red] {e}\n"
                f"[yellow]Tip: The requested format may not be available for this video.[/yellow]"
            )
            sys.exit(5)

        except DownloadError as e:
            console.print(f"[red]Download Error:[/red] {e}")
            sys.exit(6)

        except KeyboardInterrupt:
            console.print("\n[yellow]Download cancelled by user.[/yellow]")
            sys.exit(130)

        except Exception as e:
            console.print(f"[red]Unexpected Error:[/red] {e}")
            if verbose:
                console.print_exception()
            sys.exit(1)


if __name__ == "__main__":
    main()
