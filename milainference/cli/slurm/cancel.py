import os
import subprocess
from dataclasses import dataclass

from argklass.command import Command
from milainference.core.bash import popen


class Cancel(Command):
    "Cancel jobs"

    name: str = "cancel"

    @dataclass
    class Arguments:
        all: bool = False  # Cancel all the jobs except itself (if running inside a job)

    def execute(self, args):
        if args.all:
            cmd = ["squeue", "-h", "-u", os.environ["USER"], '--format="%A"']
            out = subprocess.check_output(cmd, text=True).replace('"', "")

            jobids = []
            for line in out.splitlines():
                jobids.append(line.strip())

            def notself(job):
                return job != os.getenv("SLURM_JOB_ID")

            jobids = filter(notself, jobids)

        return popen(["scancel", "-u", os.environ["USER"]] + args.args + list(jobids))


COMMANDS = Cancel
