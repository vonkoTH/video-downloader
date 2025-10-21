# Installation Guide - Arch Linux & Gentoo

This guide provides specific installation instructions for Arch Linux and Gentoo systems.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- pip or pipx (recommended)
- ffmpeg (required for audio conversion)

---

## Arch Linux Installation

### 1. Install System Dependencies

```bash
# Update system
sudo pacman -Syu

# Install required packages
sudo pacman -S python python-pip ffmpeg

# (Optional) Install pipx for isolated environment
sudo pacman -S python-pipx
pipx ensurepath
```

### 2. Install video-downloader

**Option A: Using pipx (Recommended)**
```bash
pipx install git+https://github.com/vonkoTH/video-downloader.git
```

**Option B: Using pip**
```bash
pip install --user git+https://github.com/vonkoTH/video-downloader.git
```

**Option C: From source**
```bash
git clone https://github.com/vonkoTH/video-downloader.git
cd video-downloader
pip install --user .
```

### 3. Verify Installation

```bash
video-download --help
```

### Arch-Specific Notes
- Arch uses a rolling release model, so all packages are typically up-to-date
- Python packages are installed to `~/.local/bin` by default (ensure it's in your PATH)
- Add to PATH if needed: `export PATH="$HOME/.local/bin:$PATH"` in `~/.bashrc` or `~/.zshrc`

---

## Gentoo Installation

### 1. Install System Dependencies

```bash
# Sync portage tree
sudo emerge --sync

# Install required packages
sudo emerge dev-lang/python:3.11  # or latest available version
sudo emerge dev-python/pip
sudo emerge media-video/ffmpeg

# (Optional) Install pipx
sudo emerge dev-python/pipx
pipx ensurepath
```

### 2. Configure FFmpeg (Gentoo-Specific)

Gentoo allows fine-grained control over FFmpeg features through USE flags. For basic functionality:

```bash
# Check current USE flags
emerge -pv media-video/ffmpeg

# Recommended USE flags for video-downloader
# Add to /etc/portage/package.use/ffmpeg:
# media-video/ffmpeg mp3 x264 opus vorbis aac

# Rebuild if needed
sudo emerge --ask media-video/ffmpeg
```

### 3. Install video-downloader

**Option A: Using pipx (Recommended)**
```bash
pipx install git+https://github.com/vonkoTH/video-downloader.git
```

**Option B: Using pip**
```bash
pip install --user git+https://github.com/vonkoTH/video-downloader.git
```

**Option C: From source**
```bash
git clone https://github.com/vonkoTH/video-downloader.git
cd video-downloader
pip install --user .
```

### 4. Verify Installation

```bash
video-download --help
```

### Gentoo-Specific Notes
- Gentoo compiles packages from source, giving maximum optimization
- USE flags allow customizing FFmpeg capabilities
- Python scripts install to `~/.local/bin` (ensure it's in your PATH)
- Add to PATH: `export PATH="$HOME/.local/bin:$PATH"` in `~/.bashrc`

---

## Dependency Versions

### Minimum Required Versions

| Package | Minimum Version | Arch Package | Gentoo Package |
|---------|----------------|--------------|----------------|
| Python | 3.8 | `python` | `dev-lang/python:3.8` |
| pip | 20.0 | `python-pip` | `dev-python/pip` |
| ffmpeg | 4.0 | `ffmpeg` | `media-video/ffmpeg` |
| yt-dlp | Latest | (via pip) | (via pip) |
| click | 8.0 | (via pip) | (via pip) |
| rich | 10.0 | (via pip) | (via pip) |

### Python Package Dependencies

These are installed automatically via pip/pipx:
- `yt-dlp` - Video download engine
- `click>=8.0` - CLI framework
- `rich>=10.0` - Terminal formatting and progress bars

---

## Post-Installation Configuration

### Configure Authentication (Optional)

For sites requiring authentication, you can store credentials securely:

```bash
# Configuration directory is created automatically
# Location: ~/.config/video-downloader/

# Credentials are stored in:
# ~/.config/video-downloader/credentials.json
```

Use environment variables for automation:
```bash
export VIDEO_DOWNLOADER_YOUTUBE_USERNAME="your_username"
export VIDEO_DOWNLOADER_YOUTUBE_PASSWORD="your_password"
```

---

## Filesystem Hierarchy Standard (FHS) Compliance

This application follows FHS guidelines:

| Type | Location |
|------|----------|
| User binaries | `~/.local/bin/video-download` |
| Configuration | `~/.config/video-downloader/` |
| Downloaded files | `~/Downloads/` (default, configurable) |
| Logs | Stdout/stderr (no persistent logs) |

---

## Troubleshooting

### "ffmpeg not found" error

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**Gentoo:**
```bash
sudo emerge media-video/ffmpeg
```

### "video-download: command not found"

Add `~/.local/bin` to your PATH:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Python version issues (Gentoo)

Gentoo allows multiple Python versions. Select the default:
```bash
eselect python list
sudo eselect python set python3.11  # or your preferred version
```

### SSL Certificate Errors

If you encounter SSL errors on Gentoo:
```bash
# Install/update CA certificates
sudo emerge app-misc/ca-certificates
sudo update-ca-certificates
```

---

## Uninstallation

**Using pipx:**
```bash
pipx uninstall video-downloader
```

**Using pip:**
```bash
pip uninstall video-downloader
```

**Remove configuration:**
```bash
rm -rf ~/.config/video-downloader
```

---

## Additional Resources

- **Arch Wiki - Python**: https://wiki.archlinux.org/title/Python
- **Gentoo Wiki - Python**: https://wiki.gentoo.org/wiki/Python
- **FFmpeg Documentation**: https://ffmpeg.org/documentation.html
- **yt-dlp Documentation**: https://github.com/yt-dlp/yt-dlp

---

## Distribution-Specific Differences

| Feature | Arch Linux | Gentoo |
|---------|-----------|--------|
| Package Manager | pacman | emerge |
| Package Format | Binary (.pkg.tar.zst) | Source (ebuilds) |
| FFmpeg Customization | Limited | Extensive (USE flags) |
| Python Management | Single system Python | Multiple versions (eselect) |
| Installation Speed | Fast (binary) | Slower (compilation) |
| Optimization | Generic | Architecture-specific |

Both distributions are fully supported and tested for compatibility.
