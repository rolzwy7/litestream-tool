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
    duration = video.duration  # seconds

    # Get bitrate
    bitrate_bps = int(video_path.stat().st_size * 8 / duration)

    # Cut video to max 10 seconds from the start
    clip_duration = duration if duration < 10 else 10
    video = video.subclip(0, clip_duration)

    # Save
    for quality_prct in range(10, 100 + 10, 10):
        it_bitrate = int(bitrate_bps * (quality_prct / 100))

        # replace filename in absolute path
        filename = f"{quality_prct}_percent_{it_bitrate}_{video_path.name}"
        filename = str(video_path.absolute()).replace(video_path.name, filename)

        print("> Bitrate:", quality_prct, "|", it_bitrate, "bps")
        video.write_videofile(filename, bitrate=f"{it_bitrate}")
