import json
import subprocess
from pathlib import Path

from libs.video import IntermediateVideoFile, VideoFile
from utils.mp4box import mp4box_build_intermediate


class Chapter:
    def __init__(
        self,
        chapter_dir: Path,
        original_video: VideoFile,
        intermediate_videos: list[IntermediateVideoFile],
    ) -> None:
        self.chapter_dir = chapter_dir
        self.original_video = original_video
        self.intermediate_videos = intermediate_videos
        self.videos: list[VideoFile] = []

    def create_chapter_dir(self):
        self.chapter_dir.mkdir()

    def build_intermediates(self):
        for intermediate_video in self.intermediate_videos:
            self.videos.append(
                mp4box_build_intermediate(
                    intermediate_video,
                    self.chapter_dir / f"{intermediate_video.path.name}.mp4",
                )
            )

    def generate_dash(self, segment_ms: int = 4000):
        dur = self.original_video.duration

        command = [
            "MP4Box",
            # Segments the given file into X ms chunks.
            *["-dash", f"{segment_ms}"],
            # To force 1 subsegment per segment value must be the same as dash
            *["-frag", f"{segment_ms}"],
            # Forces segments to start random access points, i.e. keyframes.
            "-rap",
            # Output manifest
            *["-out", self.chapter_dir / f"manifest.mpd"],
            # Prefix name of the segments
            *["-segment-name", f"$RepresentationID$_$Number%04d$"],
            # Positional arguments
            # trackID=N: only use the track ID N from the source file
            # :id=NAME: set the representation ID to NAME.
            # :period=NAME: set the representation's period to NAME.
            # :asID=VALUE: set the AdaptationSet ID to VALUE (unsigned int)
            # :dur=VALUE: process VALUE seconds (fraction) from the media.
            *[
                f"{video.path.absolute()}#video:trackID=1:id=video{idx+1}:period=p0:asID={idx+1}:dur={dur}"
                for idx, video in enumerate(self.videos)
            ],
            f"{self.original_video.path.absolute()}#audio:trackID=1:id=audio1:period=p0:asID=11:dur={dur}",
        ]
        subprocess.run(command)

    def clean(self):
        for intermediate_video in self.intermediate_videos:
            intermediate_video.destroy()

        for video in self.videos:
            video.video.close()
            video.destroy()
