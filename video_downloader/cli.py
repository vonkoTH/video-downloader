import click
import os
from rich.progress import Progress
from .downloader import Downloader

@click.command()
@click.argument("url")
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
    help="Path to a browser cookies file.",
)
def main(url: str, download_format: str, output_path: str, cookies_path: str | None):
    """A CLI tool to download video and audio from various web sources."""
    is_audio = download_format.lower() == "audio"

    with Progress() as progress:
        downloader = Downloader(progress)
        try:
            downloader.download(
                url=url,
                download_path=output_path,
                is_audio=is_audio,
                cookies_path=cookies_path,
            )
        except Exception as e:
            progress.console.print(f"[red]Error: {e}")

if __name__ == "__main__":
    main()
