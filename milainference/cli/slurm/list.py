import os

from milainference.args.arguments import Command
from milainference.core.bash import popen


class List(Command):
    "List user jobs"

    def execute(self, args):
        return popen(["squeue", "-u", os.environ["USER"]])


COMMANDS = List
