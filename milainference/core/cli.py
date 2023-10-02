
from argparse import ArgumentParser
import re
import subprocess

import pkg_resources
import openai

from .client import init_client
from .server_lookup import find_suitable_inference_server




def arguments():
    parser = ArgumentParser()

    subparser = parser.add_subparsers(dest="cmd")
    clt = subparser.add_parser("client")
    clt.add_argument("--model", type=str, help="Model name")
    clt.add_argument("--prompt", type=str, help="Prompt")
    clt.add_argument("--short", action="store_true", help="Only print the result and nothing else")

    srv = subparser.add_parser("server", help="Launch an inference server")
    srv.add_argument("--model", type=str, help="Model name to start")
    srv.add_argument("--sync", action="store_true", help="Wait for the server to strt")

    lst = subparser.add_parser("list", help="List all inference server available")
    lst.add_argument("--model", type=str, help="Model name to start")

    return parser.parse_args()


def client(args):
    model = init_client(args.model)

    completion = openai.Completion.create(
        model=model,
        prompt=args.prompt
    )

    if args.short:
        for choices in completion['choices']:
            print(choices['text'])
    else:
        print(completion)


def server(args):
    sbatch_script = pkg_resources.resource_filename(
        __name__, "scripts/inference_server_SHARED.sh"
    )

    cmd = [
        'sbatch',
        sbatch_script,
        args.model,
    ]

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
                line = process.stdout.readline()
                
                if match := jobid_regex.match(line):
                    data = match.groupdict()
                    jobid = data['jobid']
                
                print(line, end='')
    
        except KeyboardInterrupt:
            print("Stopping due to user interrupt")
            process.kill()
            return -1

    if jobid is not None and args.sync:
        subprocess.run(["touch", f"slurm-{jobid}.out"])
        subprocess.run(["tail", "-f", f"slurm-{jobid}.out"])
    else:
        print(jobid)
    
    return 0


def listsrv(args):
    """List all available server"""
    servers = find_suitable_inference_server(args.model)

    for s in servers:
        print(f' - {s["host"]}:{s["port"]} => {s["model"]}')


def nocmd(cmd):
    print("Command {cmd} is not recognized")
    return


def main():
    args = arguments()

    commands = {
        'client': client,
        'server': server,
        'list': listsrv
    }

    cmd = vars(args).pop('cmd')
    if cmd not in commands:
        return nocmd(cmd)

    return commands.get(cmd)(args)