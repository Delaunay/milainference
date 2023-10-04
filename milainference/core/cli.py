from milainference.args.discovery import discover_commands
from milainference.args.argformat import HelpAction, HelpActionException



def cli(*args, **kwargs):
    import argparse

    commands = discover_commands()

    parser = argparse.ArgumentParser(*args, **kwargs, add_help=False)
    parser.add_argument(
        "-h", "--help", action=HelpAction, help="show this help message and exit"
    )
    subparsers = parser.add_subparsers(dest="command")

    for cmd in commands.values():
        cmd.arguments(subparsers)

    try:
        args, unknown = parser.parse_known_args()
        vars(args)["args"] = unknown
    
        cmd = vars(args).pop('command')

        if cmd is None:
            parser.print_help()
            return

        return commands[cmd](args)
    except HelpActionException:
        pass


if __name__ == '__main__':
    cli()
