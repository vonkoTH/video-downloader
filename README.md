# Video and Audio Downloader

A desktop application for downloading video and audio from various web sources, built with Python and yt-dlp.

## Description

This application allows users to specify a URL, choose between video (MP4) and audio (MP3) formats, and select a destination folder for the downloaded files. The backend leverages the powerful `yt-dlp` library, ensuring compatibility with a wide range of websites.

The application is designed to be straightforward and efficient, featuring a responsive interface that remains active during the download process by utilising multithreading.

## Features

-   **Modern GUI:** A clean and user-friendly interface built with the `customtkinter` library, which supports system appearance themes (light/dark).
-   **Video and Audio Formats:** Option to download content as either an MP4 video file or an MP3 audio file.
-   **Asynchronous Downloads:** Downloads are handled in a separate thread to prevent the UI from freezing.
-   **Download Progress:** A progress bar and status labels provide real-time feedback on the download status.
-   **Custom Download Location:** Users can specify a directory where the files will be saved.
-   **Cookie Support:** Option to use a browser cookies file to download content from websites that require a login (e.g., TikTok, Vimeo).

## Prerequisites

Before running the application, ensure you have the following installed:

-   Python 3.x
-   `ffmpeg`: This is a required dependency for `yt-dlp` to process and convert video and audio files. It must be installed and available in your system's PATH (especially on windows).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lordvonko/video-downloader.git
    cd video-downloader
    ```

2.  **Create and activate a virtual environment (recommended, (do it)):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS and Linux
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application:**
    ```bash
    python app.py
    ```
  * **ay, no more sites with ads; privacy and speed are better.**


2.  **Paste the URL** of the video you wish to download into the URL entry field.

3.  **Select the desired format** (`Video (MP4)` or `Audio (MP3)`) from the dropdown menu.

4.  **(Optional, but recommended) Select a destination folder** by clicking the "Select Folder" button. If no folder is selected, files will be saved to your user's "Downloads" directory by default.

5.  **Click the "Download" button** to begin the download.

### Using Cookies for Authenticated Downloads

Some websites require you to be logged in to access certain content. To download from these sites, you can provide the application with a cookies file from your browser.

1.  **Export your browser cookies:** You will need to use a browser extension to export your cookies for the relevant website into a standard Netscape format text file (usually a `.txt` file). Common extensions for this are "Get cookies.txt" for BRAVE (use brave privacy is power)  or "cookies.txt" for Firefox (use brave)

2.  **Load the cookies file:** In the application, click the **"Select Cookies"** button and choose the `.txt` file you exported.

3.  **Download:** Proceed with the download as usual. The application will use the cookies to authenticate with the website.


## You're welcome.
