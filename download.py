"""
YouTube Video Downloader and Converter

This script downloads YouTube videos in 1080p resolution and converts them to MP4 format.

Example usage:
    python download.py --name="sample video" --url="https://www.youtube.com/watch?v=wDchsz8nmbo&pp=ygUMc2FtcGxlIHZpZGVv"
"""

from pathlib import Path
from argparse import ArgumentParser

from pytubefix import YouTube
from pytubefix.streams import Stream
from pytubefix.cli import on_progress

from merge_av import Merge_AV


def download_stream(
        stream: Stream,
        name: str,
        type: str = "mp4",
        output_path: str = "output"
    ) -> None:
    """
    Downloads a YouTube stream.

    Args:
        stream (Stream): The stream to download.
        name (str): The filename without extension.
        type (str, optional): The file extension. Defaults to "mp4".
        output_path (str, optional): The output directory. Defaults to "output".
    """
    # yt.streams.filter(progressive=True, file_extension="mp4").first().download(output_path="./output")
    if type == "mp4":
        stream.download(output_path, filename=f"{name}.{type}")
    elif type == "mp3":
        stream.download(output_path, filename=f"{name}", mp3=True)


def run(
    name: str,
    url: str
) -> None:
    """
    Downloads a YouTube video and merges audio and video.

    Args:
        name (str): The filename without extension.
        url (str): The YouTube video URL.
    """
    # Initialize YouTube object with progress callback
    yt = YouTube(url, on_progress_callback=on_progress)

    # Print video metadata
    print(f"Title:\t{yt.title}")
    print(f"Description:\t{yt.description}")

    # Get available streams
    streams = yt.streams
    assert len(streams) > 0, f"Video not found for the url {url}"

    output_path = Path("output") / name
    output_path.mkdir(parents=True, exist_ok=True)

    fhd_stream = streams.filter(res="1080p").first()
    # 4k_stream = streams.filter(res="2160p").first()
    mp3_stream = streams.get_audio_only()

    # Download video
    if fhd_stream:
        download_stream(fhd_stream, name, "mp4", output_path)
        download_stream(mp3_stream, name, "mp3", output_path)

        Merge_AV.simple_merge(
            (output_path/name).with_suffix(".mp4"), 
            (output_path/name).with_suffix(".mp3"),
            output_path/"final.mp4"
        )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--name", "-n", required=True, help="video name without file extension")
    parser.add_argument("--url", "-u", required=True, help="youtube video url in quotes")
    args = parser.parse_args()
    run(**vars(args))