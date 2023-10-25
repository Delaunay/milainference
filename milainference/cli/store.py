from dataclasses import dataclass
import os

from argklass.command import Command
from milainference.core.metadata import job_metadata
from milainference.core.bash import run


def set_comment(comment: str):
    jobid = os.environ.get("SLURM_JOB_ID")

    command = [
        "scontrol",
        "update",
        "job",
        f"{jobid}",
        f"comment={comment}",
    ]

    run(command)


def update_comment(*metdata):
    original = job_metadata()

    for kv in metdata:
        k, v = kv.split("=")
        original[k] = v

    newcomment = []
    for k, v in original.items():
        newcomment.append(f"{k}={v}")
    newcomment = "|".join(newcomment)

    set_comment(newcomment)
    print(newcomment)


class Store(Command):
    """Store slurm job metadata
    
    Examples
    --------

    .. code-block::

       milainfer store model=$MODEL host=$HOST port=$PORT shared=y ready=0

       milainfer store --update ready=1

    """
    name: str = "store"

    @dataclass
    class Arguments:
        update: bool = False    # Only update modified keys

    def execute(self, args):
        jobid = os.environ.get("SLURM_JOB_ID")

        if jobid is not None:
            if args.update:
                update_comment(*args.args)
            else:
                metadata = "|".join(args.args)
                set_comment(metadata)
                print(metadata)

        else:
            raise RuntimeError("Could not find job id inside environment")


COMMANDS = Store
