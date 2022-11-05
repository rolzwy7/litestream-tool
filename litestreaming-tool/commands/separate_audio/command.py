from pathlib import Path
from typing import Protocol

import moviepy.editor as mp
from libs.video import VideoFile
from pydub import AudioSegment


class Arguments(Protocol):
    input_video: str


def command(args: Arguments) -> None:
    print("separate_audio")

    video_file = VideoFile(args.input_video)
    extension = video_file.path.suffix.strip(".")
    extensions_map = {
        "aiff": "aac",
        "wma": "wma",
        "mp4": "mp4",
        "mp3": "mp3",
        "wav": "wav",
        "ogg": "ogg",
        "flv": "flv",
    }
    audio_segment = AudioSegment.from_file(
        str(video_file.path), extensions_map[extension]
    )
    output_file = video_file.path.parent / f"{video_file.path.stem}_audio.mp3"
    audio_segment.export(str(output_file), format="mp3")
