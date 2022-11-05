import datetime
from pathlib import Path
from typing import Union

import moviepy.editor as mp


class VideoFile:
    def __init__(self, filepath: Union[str, Path]) -> None:
        # Create and validate filepath
        self.path = Path(filepath) if isinstance(filepath, str) else filepath
        if not (self.path.exists() and self.path.is_file()):
            raise Exception(f"File under `{self.path}` path does not exist")
        self.bytes_size = self.path.stat().st_size

        # Create moviepy clip
        self.video = mp.VideoFileClip(str(self.path))

        # Save video file details
        self.fps = self.video.fps
        self.duration = self.video.duration
        self.bitrate_bps = int((self.bytes_size) * 8 / self.duration)
        self.bitrate_kbps = int(self.bitrate_bps / 1024)
        self.resolution = self.video.size

    def print_info(self) -> None:
        """
        Print video file details
        """
        print(
            f"""\r
        \rFilepath   : {self.path}
        \rSize       : {self.bytes_size} B | {self.bytes_size/(1024**2):.2f} MB
        \rDuration   : {self.duration} s
        \rBitrate    : {self.bitrate_bps} bps | {self.bitrate_kbps} kbps
        \rResolution : {self.resolution[0]}x{self.resolution[1]}
        \rFPS        : {self.fps}
        """
        )

    def get_hms_duration(self):
        dur = int(self.video.duration)
        h = dur // (60 * 60)
        dur -= h * (60 * 60)
        m = dur // 60
        dur -= m * 60
        s = dur
        return {
            "h": h,
            "m": m,
            "s": s,
        }

    def destroy(self):
        """
        Remove this file
        """
        self.path.unlink(missing_ok=True)
