import time
from typing import Protocol

import whisper
from libs.video import VideoFile
from pydub import AudioSegment
from pydub.silence import split_on_silence


class Arguments(Protocol):
    input_video: str


def command(args: Arguments) -> None:
    print("generate_subtitles")

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
    # audio_segment = AudioSegment.from_file(
    #     str(video_file.path), extensions_map[extension]
    # )
    # audio_chunks = split_on_silence(
    #     audio_segment, min_silence_len=150, silence_thresh=-40, keep_silence=True
    # )

    model_name = "small"
    print(">> Model:", model_name)

    start_measure = time.perf_counter()
    model = whisper.load_model(model_name)
    result = model.transcribe(str(video_file.path))
    result_measure = time.perf_counter() - start_measure
    print(f">> Transcription took {result_measure:.2f} seconds")

    print(">> Text:")
    print(f"`{result['text']}`\n")

    print(">> Segments:")
    for segment in result["segments"]:
        print(segment)

    # for idx, chunk in enumerate(audio_chunks):
    #     stem = video_file.path.stem
    #     output_file = video_file.path.parent / f"{stem}_chunk{idx:05d}.mp3"
    #     print(f"> [chunk {idx}] Exporting audio:", output_file)
    #     chunk.export(str(output_file), format="mp3")
    #     result = model.transcribe(str(output_file))
    #     print(f"- result: `{result}`\n")

    # Cleanup
    video_file.video.close()
