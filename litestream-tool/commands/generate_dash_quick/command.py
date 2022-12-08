import json
import subprocess
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from libs.video import VideoFile


class Arguments(Protocol):
    video: str


def command(args: Arguments) -> None:
    video = VideoFile(args.video)
    dur = video.duration
    segment_ms = 4000

    video.print_info()

    # Create output directory
    output_dir = video.path.parent / str(uuid4())
    main_dir = output_dir / "main"

    print("[*] Trying to create output directory ")
    try:
        output_dir.mkdir()
        print("Output directory:", output_dir)
    except Exception as e:
        print(f"[-] Output dir {output_dir} doesn't exists")
        raise

    print("[*] Trying to create main (only) chapter")
    try:
        main_dir.mkdir()
        print("Main directory:", main_dir)
    except Exception as e:
        print(f"[-] Main dir {main_dir} doesn't exists")
        raise

    command = [
        "MP4Box",
        # Segments the given file into X ms chunks.
        *["-dash", f"{segment_ms}"],
        # To force 1 subsegment per segment value must be the same as dash
        *["-frag", f"{segment_ms}"],
        # Forces segments to start random access points, i.e. keyframes.
        "-rap",
        # Output manifest
        *["-out", main_dir / f"manifest.mpd"],
        # Prefix name of the segments
        *["-segment-name", f"$RepresentationID$_$Number%04d$"],
        # Positional arguments
        # trackID=N: only use the track ID N from the source file
        # :id=NAME: set the representation ID to NAME.
        # :period=NAME: set the representation's period to NAME.
        # :asID=VALUE: set the AdaptationSet ID to VALUE (unsigned int)
        # :dur=VALUE: process VALUE seconds (fraction) from the media.
        # f"{video.path.absolute()}#video:trackID=1:id=video1:period=p0:asID=1:dur={dur}",
        # f"{video.path.absolute()}#audio:trackID=1:id=audio1:period=p0:asID=11:dur={dur}",
        f"{video.path.absolute()}#video",
        f"{video.path.absolute()}#audio",
    ]
    subprocess.run(command)

    # Save chapters.json file
    chapters_desc = [
        {
            "id": 1,
            "description": "Recording",
            "chapter_name": "main",
            "outfile": "main.mp4",
            "start": "00:00:00",
            "end": video.duration_humanformat,
            "title": video.path.stem,
            "duration": video.get_hms_duration(),
            "dir": "main",
        }
    ]
    with (output_dir / "chapters.json").open("wb") as dst:
        dst.write(json.dumps(chapters_desc, indent=4).encode("utf8"))

    # Clean
    video.video.close()

    print("\n\n[+] Done.")

    print(f"\n[>] Result: {output_dir}")
