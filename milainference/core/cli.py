from argparse import ArgumentParser
import re
import subprocess
import os

import pkg_resources
import openai

from .client import init_client
from .server_lookup import get_inference_servers, parse_meta


def _run(cmd):
    # Mock this for testing
    return subprocess.run(cmd)


def arguments():
    parser = ArgumentParser()

    subparser = parser.add_subparsers(dest="cmd")
    clt = subparser.add_parser("client")
    clt.add_argument("--prompt", type=str, help="Prompt")
    clt.add_argument("--model", type=str, help="Model name", default=None)
    clt.add_argument(
        "--short", action="store_true", help="Only print the result and nothing else"
    )

    srv = subparser.add_parser("server", help="Launch an inference server")
    srv.add_argument("--model", type=str, help="Model name to start", default=None)
    srv.add_argument("--path", type=str, help="Model path")
    srv.add_argument("--sync", action="store_true", help="Wait for the server to strt")
    srv.add_argument("args", nargs="*", action="append", help="Slurm arguments")

    lst = subparser.add_parser("list", help="List all inference server available")
    lst.add_argument("--model", type=str, help="Model name to start", default=None)

    store = subparser.add_parser("store", help="Store metadata")
    store.add_argument("--update", action="store_true", help="Only update modified keys")
    store.add_argument("args", nargs="*", action="append", help="Key=Value pairs")

    clt = subparser.add_parser("waitfor", help="Wait for a model to come online")
    clt.add_argument("--model", type=str, help="Model name")

    return parser.parse_args()


def client(args):
    model = init_client(args.model)

    completion = openai.Completion.create(model=model, prompt=args.prompt)

    if args.short:
        for choices in completion["choices"]:
            print(choices["text"])
    else:
        print(completion)


def server(args):
    sbatch_script = pkg_resources.resource_filename(
        __name__, "scripts/inference_server_SHARED.sh"
    )

    if args.model is None:
        args.model = args.path.split('/')[-1]

    cmd = [
        "sbatch",
        sbatch_script,
        args.model,
        args.path,
    ] + args.args[0]

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


def listsrv(args):
    """List all available server"""
    servers = get_inference_servers(args.model)

    for s in servers:
        print(f' - {s["host"]}:{s["port"]} => {s["model"]}')


def nocmd(cmd):
    print("Command {cmd} is not recognized")
    return


def job_metadata(jobid=None):
    if jobid is None:
        jobid = os.environ.get("SLURM_JOB_ID")
    
    command = ["squeue", "-h", f"--job={jobid}", '--format="%k"']
    
    output = subprocess.check_output(command, text=True)
    
    s = 0
    e = len(output)
    
    if output[s] == '"':
        s += 1
        
    if output[e - 1] == '"':
        e -= 1
    
    output = output[s:e]
    
    
    meta = dict()
    for line in output.splitlines():
        meta.update(parse_meta(line))

    return meta


def set_comment(comment: str):
    jobid = os.environ.get("SLURM_JOB_ID")

    command = [
        "scontrol",
        "update",
        "job",
        f"{jobid}",
        f"comment={comment}",
    ]

    _run(command)


def update_comment(*metdata):
    original = job_metadata()

    for kv in metdata:
        k, v = kv.split('=')
        original[k] = v

    newcomment = []
    for k, v in original.items():
        newcomment.append(f'{k}={v}')
    newcomment = '|'.join(newcomment)

    set_comment(newcomment)
    print(newcomment)


def store(args):
    """
    Examples
    --------

    .. code-block::

       milainfer store model=$MODEL host=$HOST port=$PORT shared=y ready=0

       milainfer store --update ready=1
    
    """
    jobid = os.environ.get("SLURM_JOB_ID")

    if jobid is not None:

        if args.update:
            update_comment(*args.args[0])
        else:
            metadata = "|".join(args.args[0])
            set_comment(metadata)
            print(metadata)
    
    else:
        raise RuntimeError("Could not find job id inside environment")


def waitfor(args):
    servers = get_inference_servers(args.model, pending_ok=True)
    ready = False
    selected_server = None

    while not ready:
        for server in servers:
            info = job_metadata(server["job_id"])

            if info.get("ready", '0') == 1:
                ready = True
                selected_server = server
                break

    print("The following server is ready")
    print(f"   {selected_server}")



def main():
    args = arguments()

    commands = {
        "client": client,
        "server": server,
        "list": listsrv,
        "store": store,
        "waitfor": waitfor,
    }

    cmd = vars(args).pop("cmd")
    if cmd not in commands:
        return nocmd(cmd)

    return commands.get(cmd)(args)
