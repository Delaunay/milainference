import os
from dataclasses import dataclass

from argklass.command import Command

from milainference.core.bash import popen


class List(Command):
    "List user jobs"

    name: str = "list"

    @dataclass
    class Arguments:
        pass

    def execute(self, args):
        return popen(["squeue", "-u", os.environ["USER"]] + args.args)


COMMANDS = List
