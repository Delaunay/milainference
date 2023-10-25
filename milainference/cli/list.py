from dataclasses import dataclass


from argklass.command import Command
from milainference.core.server_lookup import get_inference_servers


class List(Command):
    "List all inference server available"

    name: str = "list"

    @dataclass
    class Arguments:
        model: str = None      # Model name to look for

    def execute(self, args):
        servers = get_inference_servers(args.model, pending_ok=True)

        for s in servers:
            status = "PENDING"
            if s["ready"] == "1":
                status = "READY  "

            print(f' - {status} {s["host"]}:{s["port"]} => {s["model"]}')


COMMANDS = List
