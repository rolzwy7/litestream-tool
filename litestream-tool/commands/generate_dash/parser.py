def register_arguments(subparser):
    subparser.add_argument("stream_id", help="Stream identifier, example: `my-stream`")
    subparser.add_argument("output_dir", help="Destination directory for output/build")
    subparser.add_argument(
        "--videos",
        required=True,
        nargs="+",
        help="List of video files. Ordering matters.",
    )
    subparser.add_argument(
        "--bitrate",
        type=int,
        required=True,
        help="Bitrate of the best quality",
    )
