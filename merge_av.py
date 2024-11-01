import subprocess
from pathlib import Path


class Merge_AV:
    @staticmethod
    def simple_merge(
            video_pth: Path,
            audio_pth: Path,
            output_pth: Path = Path("./output/final.mp4")
    ) -> None:
        """
        Merges video and audio files using ffmpeg.

        Args:
            video_pth (Path): Path to the video file.
            audio_pth (Path): Path to the audio file.
            output_dir (Path, optional): Output directory. Defaults to "./output".

        Raises:
            FileNotFoundError: If the executable (ffmpeg) is not found.
            subprocess.CalledProcessError: If ffmpeg returns a non-zero exit code.
            subprocess.TimeoutExpired: If the process times out.
        """
        try:
            print(f"Processing video...")
            _completed_proc = subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-i", str(video_pth),
                    "-i", str(audio_pth),
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-map", "0:v:0",
                    "-map", "1:a:0",
                    str(output_pth)
                ],
                timeout=120,
                # capture_output=True,
                check=True
            )
            print(f"file name:\t{output_pth} \nDone!")
        except FileNotFoundError as exc:
            print(f"Process failed because the executable could not be found.\n{exc}")
        except subprocess.CalledProcessError as exc:
            print(
                f"Process failed because ffmpeg did not return a successful return code. "
                f"Returned {exc.returncode}\n{exc}"
            )
        except subprocess.TimeoutExpired as exc:
            print(f"Process timed out.\n{exc}")
    