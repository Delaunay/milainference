from dataclasses import dataclass
import re
import subprocess

import pkg_resources

from milainference.args.arguments import Command

def _run(cmd):
    # Mock this for testing
    return subprocess.run(cmd)


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

        cmd = (
            ["sbatch"]
            + args.args
            + [
                sbatch_script,
                args.model,
                args.path,
            ]
        )

        jobid_regex = re.compile(r"Submitted batch job (?P<jobid>[0-9]*)")
        jobid = None

        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False,
        ) as process:
            try:
                while process.poll() is None:
                    process.stdout.flush()
                    line = process.stdout.readline()
                    if match := jobid_regex.match(line):
                        data = match.groupdict()
                        jobid = data["jobid"]

                    print(line, end="")

            except KeyboardInterrupt:
                print("Stopping due to user interrupt")
                process.kill()
                return -1

        if jobid is not None and args.sync:
            _run(["touch", f"slurm-{jobid}.out"])
            _run(["tail", "-f", f"slurm-{jobid}.out"])
        else:
            print(jobid)

        return 0


COMMANDS = Server
