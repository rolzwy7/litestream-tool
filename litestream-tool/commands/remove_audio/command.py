from pathlib import Path
from typing import Protocol

import moviepy.editor as mp


class Arguments(Protocol):
    input_video: str


def command(args: Arguments) -> None:
    video_path = Path(args.input_video)

    if not (video_path.exists() and video_path.is_file()):
        raise Exception(f"File under `{video_path}` path does not exist")

    # Create video clip
    video = mp.VideoFileClip(str(video_path), audio=False)

    # Save no-audio file in the same location, under different name
    dst_path = str(video_path.absolute()).replace(
        video_path.name, f"{video_path.stem}_no_audio{video_path.suffix}"
    )
    video.write_videofile(dst_path)

    print("[*] Saved: ", dst_path)
