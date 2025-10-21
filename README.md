<h1 align="center">video-downloader</h1>

A secure, feature-rich CLI tool to download video and audio from various web sources, built with Python and yt-dlp.

## Description

This command-line application allows you to download video and audio from a given URL with multiple authentication methods, robust error handling, and enhanced security. Choose between MP4 video or MP3 audio formats, specify output quality, and authenticate using username/password, stored credentials, or cookies.

The tool is powered by `yt-dlp` and features real-time progress tracking, comprehensive logging, and automatic dependency verification.

## Features

### Core Functionality
-   **Simple CLI:** Clean and intuitive command-line interface with helpful error messages
-   **Multiple Formats:** Download as MP4 video or MP3 audio with configurable quality
-   **Real-Time Progress:** Rich progress bars with accurate download tracking
-   **Custom Download Location:** Specify any directory for your downloads
-   **Automatic Dependency Check:** Verifies ffmpeg installation before download

### Authentication & Security
-   **🆕 Cookie-Free Authentication:** Username/password support without browser cookies
-   **🆕 Credential Storage:** Securely store site credentials in `~/.config/video-downloader/`
-   **🆕 Environment Variables:** Support for `VIDEO_DOWNLOADER_<SITE>_USERNAME/PASSWORD`
-   **🆕 SSL Verification:** Enabled by default for secure connections
-   **Cookie Fallback:** Optional browser cookies support for compatibility

### Reliability & Error Handling
-   **🆕 Retry Logic:** Automatic retry with configurable attempts (default: 3)
-   **🆕 Timeout Control:** Configurable socket timeout to prevent hangs
-   **🆕 Specific Error Messages:** Clear categorization of network, format, and dependency errors
-   **🆕 Verbose Logging:** Debug mode with detailed execution traces

## Prerequisites

-   Python 3.8+
-   `pipx` (recommended for installation)
-   `ffmpeg` (required by `yt-dlp` for processing video and audio)

## Installation

### Quick Install (Recommended)

Using `pipx` to avoid dependency conflicts:

```bash
pipx install git+https://github.com/vonkoTH/video-downloader.git
```

### Distribution-Specific Installation

For detailed installation instructions for **Arch Linux** and **Gentoo**, see [INSTALL_LINUX.md](INSTALL_LINUX.md).

**Arch Linux:**
```bash
sudo pacman -S python python-pip ffmpeg
pipx install git+https://github.com/vonkoTH/video-downloader.git
```

**Gentoo:**
```bash
sudo emerge dev-lang/python dev-python/pip media-video/ffmpeg
pipx install git+https://github.com/vonkoTH/video-downloader.git
```

## Usage

```bash
video-download [OPTIONS] URL
```

### Arguments

-   `URL`: The URL of the video to download (required).

### Options

#### Format & Output
-   `-f`, `--format [video|audio]`: Download format (default: `video`)
-   `-o`, `--output DIRECTORY`: Output directory (default: `~/Downloads`)
-   `--audio-quality KBPS`: Audio bitrate in kbps (default: `192`)

#### Authentication (Priority Order)
-   `-u`, `--username TEXT`: Username for authentication (highest priority)
-   `-p`, `--password TEXT`: Password for authentication (use with `--username`)
-   `-s`, `--site TEXT`: Site identifier for stored credentials (e.g., 'youtube', 'tiktok')
-   `-c`, `--cookies FILE`: Path to browser cookies file (fallback method)
-   `--no-cookies`: Disable cookie-based authentication entirely

#### Network & Security
-   `--retries INTEGER`: Maximum retry attempts (default: `3`)
-   `--timeout INTEGER`: Socket timeout in seconds (default: `30`)
-   `--no-check-certificate`: Disable SSL verification ⚠️ **insecure, not recommended**

#### Debugging
-   `-v`, `--verbose`: Enable verbose logging
-   `--help`: Show help message and exit

### Examples

#### Basic Usage

1.  **Download a video to your Downloads folder:**

    ```bash
    video-download "https://www.youtube.com/watch?v=DuDX6wNfjqc"
    ```

2.  **Download audio only to a specific folder:**

    ```bash
    video-download --format audio --output ~/Music "https://www.youtube.com/watch?v=DuDX6wNfjqc"
    ```

3.  **Download with custom audio quality:**

    ```bash
    video-download -f audio --audio-quality 320 "https://example.com/video"
    ```

#### Authentication Methods

4.  **🆕 Using username and password (recommended):**

    ```bash
    video-download --username myuser --password mypass "https://example.com/video"
    ```

5.  **🆕 Using stored credentials:**

    ```bash
    # First time: store credentials (feature planned for CLI in 2.1.0)
    # For now, use environment variables:
    export VIDEO_DOWNLOADER_YOUTUBE_USERNAME="myuser"
    export VIDEO_DOWNLOADER_YOUTUBE_PASSWORD="mypass"

    # Then download using stored credentials
    video-download --site youtube "https://www.youtube.com/watch?v=example"
    ```

6.  **🆕 Using environment variables:**

    ```bash
    VIDEO_DOWNLOADER_TIKTOK_USERNAME="user" \
    VIDEO_DOWNLOADER_TIKTOK_PASSWORD="pass" \
    video-download --site tiktok "https://www.tiktok.com/@user/video/123"
    ```

7.  **Using cookies (fallback method):**

    For sites like TikTok that require login, you can use the [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) extension to export cookies from just one site.

    ```bash
    video-download --cookies /path/to/cookies.txt "https://www.tiktok.com/video"
    ```

8.  **🆕 Download public content without authentication:**

    ```bash
    video-download --no-cookies "https://www.youtube.com/watch?v=public_video"
    ```

#### Advanced Options

9.  **🆕 Download with retry and timeout configuration:**

    ```bash
    video-download --retries 5 --timeout 60 "https://example.com/video"
    ```

10. **🆕 Verbose mode for debugging:**

    ```bash
    video-download --verbose "https://example.com/video"
    ```

## Authentication Priority

The tool uses authentication methods in this priority order:

1. **Direct credentials** (`--username` and `--password`) - Highest priority
2. **Stored credentials** (`--site` with stored credentials or environment variables)
3. **Browser cookies** (`--cookies` file)
4. **No authentication** (public content only)

## Security Best Practices

✅ **Recommended:**
- Use `--username`/`--password` for direct authentication
- Store credentials in environment variables for automation
- Keep SSL verification enabled (default)

⚠️ **Not Recommended:**
- Using `--no-check-certificate` (disables SSL security)
- Storing passwords in shell history (use environment variables instead)
- Sharing cookie files (contains session data)

## Troubleshooting

### "ffmpeg not found"

Install ffmpeg for your distribution:

```bash
# Arch Linux
sudo pacman -S ffmpeg

# Gentoo
sudo emerge media-video/ffmpeg
```

### "command not found: video-download"

Add `~/.local/bin` to your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### SSL Certificate Errors

Only use `--no-check-certificate` as a last resort. Instead, update your CA certificates:

```bash
# Arch Linux
sudo pacman -S ca-certificates

# Gentoo
sudo emerge app-misc/ca-certificates
sudo update-ca-certificates
```

For more troubleshooting, see [INSTALL_LINUX.md](INSTALL_LINUX.md).

## What's New in 2.0.0

🔒 **Security:** SSL verification enabled by default, cookie-free authentication
🎯 **Reliability:** Retry logic, timeout control, dependency verification
🐛 **Error Handling:** Specific error types with helpful messages
📊 **Logging:** Verbose mode with debug output
⚙️ **Flexibility:** Configurable audio quality, retries, and timeouts
🐧 **Linux Support:** Verified on Arch Linux and Gentoo

See [CHANGELOG.md](CHANGELOG.md) for detailed changes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.
