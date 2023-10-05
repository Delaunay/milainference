import re
from dataclasses import dataclass

from milainference.args.arguments import Command
from milainference.core.bash import popen, run


def sbatch(args, sync=False, **kwargs):
    jobid_regex = re.compile(r"Submitted batch job (?P<jobid>[0-9]*)")
    jobid = None

    def readline(line):
        nonlocal jobid
    
        if match := jobid_regex.match(line):
            data = match.groupdict()
            jobid = data["jobid"]

        print(line, end="")

    code = popen(['sbatch'] + args, readline)

    if jobid is not None and sync:
        run(["touch", f"slurm-{jobid}.out"])
        run(["tail", "-f", f"slurm-{jobid}.out"])
        
    return code, jobid


class Sbatch(Command):
    "Launch an inference server"

    @dataclass
    class Arguments:
        sync: bool = False      # Wait for the server to start

    def execute(self, args):
        code, _ = sbatch(args.args, sync=args.sync)
        return code


COMMANDS = Sbatch
