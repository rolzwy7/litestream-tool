import subprocess
from pathlib import Path

from libs.video.IntermediateVideoFile import IntermediateVideoFile
from libs.video.VideoFile import VideoFile


def mp4box_build_intermediate(intermediate: IntermediateVideoFile, output: Path):
    subprocess.run(
        [
            "MP4Box",
            *["-add", f"{intermediate.path.absolute()}"],
            *["-fps", f"{intermediate.fps}"],
            str(output.absolute()),
        ]
    )
    return VideoFile(output)
