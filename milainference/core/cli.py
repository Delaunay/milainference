import argparse

from argklass.argformat import HelpAction, HelpActionException
from argklass.plugin import discover_module_commands

import milainference.cli
import milainference.plugins


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(
        "milainfer",
        description="Tool to help launching inference server",
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action=HelpAction,
        help="show this help message and exit",
    )

    subparsers = parser.add_subparsers(dest="command")
    commands = discover_module_commands(
        milainference.cli, milainference.plugins
    ).found_commands

    for cmd in commands.values():
        cmd.arguments(subparsers)

    try:
        args, unknown = parser.parse_known_args()
        vars(args)["args"] = unknown

        cmd = vars(args).pop("command")

        if cmd is None:
            parser.print_help()
            return

        return commands[cmd](args)
    except HelpActionException:
        pass


if __name__ == "__main__":
    main()
