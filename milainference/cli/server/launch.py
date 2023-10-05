from dataclasses import dataclass

import pkg_resources

from milainference.args.arguments import Command
from milainference.cli.slurm.sbatch import sbatch


class Server(Command):
    "Launch an inference server"

    @dataclass
    class Arguments:
        model: str              # Model name to start
        path: str               # Path to model weights
        sync: bool = False      # Wait for the server to start

    def execute(self, args):
        sbatch_script = pkg_resources.resource_filename(
            __name__, "scripts/inference_server_SHARED.sh"
        )

        if args.model is None:
            args.model = list(filter(lambda s: len(s) != 0, args.path.split("/")))[-1]

        assert args.model != ""

        cmd = [args.args] + [
            sbatch_script,
                args.model,
                args.path,
        ]

        code, _ = sbatch(cmd, sync=args.sync)

        return code


COMMANDS = Server
