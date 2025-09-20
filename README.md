<h1 align="center">video-downloader</h1>

A CLI tool to download video and audio from various web sources, built with Python and yt-dlp.

## Description

This command-line application allows you to download video and audio from a given URL. You can choose the format (MP4 for video, MP3 for audio), specify a destination folder, and use a browser cookies file for websites that require a login.

The tool is powered by `yt-dlp` and features a real-time progress bar.

## Features

-   **Simple CLI:** A clean and straightforward command-line interface.
-   **Video and Audio Formats:** Download as MP4 video or MP3 audio.
-   **Real-Time Progress:** A progress bar provides feedback on the download status.
-   **Custom Download Location:** Specify a directory for your downloads.
-   **Cookie Support:** Use a cookies file for authenticated downloads.

## Prerequisites

-   Python 3.8+
-   `pipx` (recommended for installation)
-   `ffmpeg` (required by `yt-dlp` for processing video and audio)

## Installation

It is recommended to install the tool using `pipx` to avoid dependency conflicts:

```bash
pipx install git+https://github.com/vonkoTH/video-downloader.git
```

## Usage

```bash
video-download [OPTIONS] URL
```

### Arguments

-   `URL`: The URL of the video to download.

### Options

-   `-f`, `--format [video|audio]`: The download format (default: `video`).
-   `-o`, `--output DIRECTORY`: The output directory (default: `~/Downloads`).
-   `-c`, `--cookies FILE`: Path to a browser cookies file.
-   `--help`: Show the help message and exit.

### Examples

1.  **Download a video to your Downloads folder:**

    ```bash
    video-download "https://www.youtube.com/watch?v=DuDX6wNfjqc&list=RDDuDX6wNfjqc"
    ```

2.  **Download audio only to a specific folder:**

    ```bash
    video-download --format audio --output /path/to/your/music "https://www.youtube.com/watch?v=DuDX6wNfjqc&list=RDDuDX6wNfjqc"
    ```

3.  **Download a video using a cookies file:**

-   **Tiktok:** usually has a login system; use cookies to bypass it. I recommend the [Get cookies.txt](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) LOCALLY extension, which can export the cookies from just one site instead of the entire browser.
    ```bash
    video-download --cookies /path/to/your/cookies.txt "https://www.some-website.com/video"
    ```
