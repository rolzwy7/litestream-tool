from pathlib import Path


class IntermediateVideoFile:
    def __init__(self, filepath: Path, fps: float, bitrate_kbps: int) -> None:
        # Create and validate filepath
        self.path = filepath
        if not (self.path.exists() and self.path.is_file()):
            raise Exception(f"File under `{self.path}` path does not exist")
        self.fps = fps
        self.bitrate_kbps = bitrate_kbps

    def destroy(self):
        """
        Remove this file
        """
        self.path.unlink(missing_ok=True)
