from pathlib import Path

import fire
from pytubefix import YouTube
from pytubefix.streams import Stream
from pytubefix.cli import on_progress

from merge_av import merge_audio_video


def download_stream(
        stream: Stream,
        name: str,
        type: str = "mp4",
        output_path: str = "output"
    ) -> None:
    # yt.streams.filter(progressive=True, file_extension="mp4").first().download(output_path="./output")
    print(f"Downloading {stream.resolution} {type} to {output_path}...")
    if type == "mp4":
        stream.download(output_path, filename=f"{name}.{type}")
    elif type == "mp3":
        stream.download(output_path, filename=f"{name}", mp3=True)
    print(f"Done.")


def run(
    name: str,
    url: str
):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(f"Title:\t{yt.title}")
    print(f"Description:\t{yt.description}")
    streams = yt.streams

    assert len(streams) > 0, f"Video not found for the url {url}"
    output_path = Path("output") / name
    output_path.mkdir(parents=True, exist_ok=True)

    fhd_stream = streams.filter(res="1080p").first()
    mp3_stream = streams.get_audio_only()

    # download_stream(fhd_streams.first())
    if fhd_stream:
        download_stream(fhd_stream, name, "mp4", output_path)
        download_stream(mp3_stream, name, "mp3", output_path)

        print(f"Merging video and audio...")
        merge_audio_video(str(output_path/name)+".mp4", str(output_path/name)+".mp3", str(output_path))


if __name__ == "__main__":
    fire.Fire(run)