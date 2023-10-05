from dataclasses import dataclass
import os

from milainference.args.arguments import Command
from milainference.core.bash import popen


class List(Command):
    "List user jobs"
    
    @dataclass
    class Arguments:
        pass

    def execute(self, args):
        return popen(["squeue", "-u", os.environ["USER"]])


COMMANDS = List
