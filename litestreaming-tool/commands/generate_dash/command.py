import json
from pathlib import Path
from typing import Protocol

from libs.video import Chapter, VideoFile
from utils import transform_to_chapter_dir, x264


class Arguments(Protocol):
    stream_id: str
    output_dir: str
    videos: list[str]
    bitrate: int


def command(args: Arguments) -> None:
    stream_id = args.stream_id.lower()
    output_dir = Path(args.output_dir)
    bitrate = args.bitrate

    if output_dir.exists() and not output_dir.is_dir():
        raise Exception(f"Build dir {output_dir} is not directory")

    # Create and print info about chapter video files
    videos: list[VideoFile] = [VideoFile(video) for video in args.videos]
    for video in videos:
        video.print_info()

    # Create stream dir
    stream_dir = output_dir / stream_id
    try:
        stream_dir.mkdir()
    except Exception as e:
        print(f"[-] Output dir {output_dir} doesn't exists")
        raise

    chapters = [
        Chapter(
            stream_dir / transform_to_chapter_dir(video.path.stem),
            video,
            [
                x264(video, video.fps, bitrate),
                x264(video, video.fps, int(0.5 * bitrate)),
                x264(video, video.fps, int(0.25 * bitrate)),
            ],
        )
        for video in videos
    ]

    for chapter in chapters:
        chapter.create_chapter_dir()
        chapter.build_intermediates()
        chapter.generate_dash()

    # Create chapters.json manifest file
    json_dict = []
    for video in videos:
        json_dict.append(
            {
                "title": video.path.stem,
                "duration": video.get_hms_duration(),
                "dir": transform_to_chapter_dir(video.path.stem),
            }
        )
    with (stream_dir / "chapters.json").open("wb") as dst:
        dst.write(json.dumps(json_dict, indent=4).encode("utf8"))

    print("\n\n[*] Cleaning.")

    for chapter in chapters:
        chapter.clean()

    print("\n\n[+] Done.")
