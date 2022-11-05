import subprocess
from pathlib import Path

from libs.video.IntermediateVideoFile import IntermediateVideoFile
from libs.video.VideoFile import VideoFile


def x264(video: VideoFile, target_fps: float, target_bitrate_kbps: int):

    output = Path(
        str(video.path.absolute()).replace(
            video.path.name,
            f"{video.path.stem}_{target_fps}_{target_bitrate_kbps}.264",
        )
    )

    subprocess.run(
        [
            "x264",
            # Specify framerate
            *["--fps", f"{target_fps}"],
            # Use a preset to select encoding settings
            # choices:
            # ultrafast,superfast,veryfast,faster,fast
            # medium,slow,slower,veryslow,placebo
            *["--preset", "slow"],
            # Set bitrate (kbit/s)
            *["--bitrate", f"{target_bitrate_kbps}"],
            # Max local bitrate (kbit/s)
            *["--vbv-maxrate", f"{target_bitrate_kbps * 2}"],
            # Set size of the VBV buffer (kbit)
            *["--vbv-bufsize", f"{target_bitrate_kbps * 4}"],
            # Sets the maximum interval between keyframes. This setting is important
            # as we will later split the video into segments and at the beginning of
            # each segment should be a keyframe. Therefore,
            # --keyint
            # should match the desired segment length in seconds mulitplied with the
            # frame rate. Here: 4 seconds * 24 frames/seconds = 96 frames.
            *["--keyint", f"{int(target_fps * 4)}"],
            *["--min-keyint", f"{int(target_fps * 4)}"],
            # Completely disables adaptive keyframe decision.
            "--no-scenecut",
            # Only one pass encoding is used. Can be set to 2 to further improve quality,
            # but takes a long time.
            *["--pass", f"{1}"],
            # Is used to change the resolution. Can be omitted
            # if the resolution should stay the same as in the source video.
            # *["--video-filter", f"resize:width={width},height={height}"],
            # Output
            *["--output", str(output.absolute())],
            # Input
            video.path.absolute(),
        ]
    )
    return IntermediateVideoFile(output, target_fps, target_bitrate_kbps)
