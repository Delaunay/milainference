import time
from dataclasses import dataclass

from argklass.command import Command

from milainference.core.metadata import job_metadata
from milainference.core.server_lookup import get_inference_servers


def waitfor(servers):
    start = time.time()
    ready = len(servers) == 0
    selected_server = None
    newlist = []
    start = time.time()
    newline = False

    while not ready:
        print(
            f"\rWaiting on {len(servers)} servers for {time.time() - start:.2f}s",
            end="",
        )
        newline = True

        for server in servers:
            info = job_metadata(server["job_id"])

            if info.get("ready", "0") == "1":
                ready = True
                selected_server = server
                break

            if len(info) != 0:
                newlist.append(server)

        time.sleep(1)
        servers = newlist
        newlist = []

        if len(servers) == 0:
            break

    if newline:
        print()

    return selected_server


class WaitFor(Command):
    """Wait for a model to come online"""

    name: str = "waitfor"

    @dataclass
    class Arguments:
        model: str = None  # Model name

    def execute(self, args):
        servers = get_inference_servers(args.model, pending_ok=True)

        try:
            selected_server = waitfor(servers)

            if selected_server:
                print("The following server is ready")
                print(f"   {selected_server}")
            else:
                print("No pending server found")
        except KeyboardInterrupt:
            pass


COMMANDS = WaitFor
