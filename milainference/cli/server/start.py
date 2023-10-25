from argklass.argformat import HelpAction
from argklass.command import Command

from milainference.core.api_server import arguments, main


class Start(Command):
    """Start an inference server"""

    name: str = "start"

    @classmethod
    def arguments(cls, subparsers):
        """Define the arguments of this command"""
        parser = subparsers.add_parser(cls.name, description=cls.help(), add_help=False)
        parser.add_argument(
            "-h", "--help", action=HelpAction, help="show this help message and exit"
        )

        try:
            arguments(parser)
        except ImportError:
            print()
            print("     /!\\ server start commandis disabled, vllm is not installed")
            print()

    def execute(self, args):
        main(args)


COMMANDS = Start
