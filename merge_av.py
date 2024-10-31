from pathlib import Path

import fire
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip
)


def merge_audio_video(
        video_pth: str,
        audio_pth: str,
        output_dir: str = "./output"
) -> None:
    video = VideoFileClip(video_pth)
    audio = AudioFileClip(audio_pth)
    output_pth = Path(output_dir) / "final.mp4"
    final_video = video.set_audio(audio)
    final_video.write_videofile(str(output_pth))


if __name__ == "__main__":
    fire.Fire(merge_audio_video)