import argparse
from types import ModuleType

from commands import (
    bitrate_samples,
    generate_dash,
    generate_subtitles,
    remove_audio,
    separate_audio,
)


class Command:
    def __init__(
        self, module: ModuleType, aliases: list[str], description: str
    ) -> None:
        self.module = module
        self.name = module.__name__.replace("commands.", "")
        self.aliases = aliases
        self.description = description

    def get_command_names(self):
        """
        Returns list of all possible command names (full name and aliases)
        """
        return [self.name, *self.aliases]


COMMANDS = [
    Command(
        bitrate_samples,
        ["bs"],
        "Create samples of given video for different bitrates",
    ),
    Command(generate_dash, ["gd"], "Generate MPEG-DASH package with manifest file"),
    Command(generate_subtitles, ["gs"], "Generate subtitles with Google whisper"),
    Command(remove_audio, ["ra"], "Remove audio from video file"),
    Command(separate_audio, ["sa"], "Seperate audio from fiven video file"),
]

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", help="sub-commands")

# Register parsers
for command in COMMANDS:
    # create subparser and add arguments for command
    command.module.register_arguments(
        subparsers.add_parser(command.name, aliases=command.aliases)
    )


def main():
    # arguments parsed from command line
    args = parser.parse_args()

    for command in COMMANDS:
        if args.command in command.get_command_names():
            # execute command with arguments
            command.module.command(args)  # type: ignore
            break


if __name__ == "__main__":
    main()
