

from dataclasses import dataclass
import time

from milainference.args.arguments import Command
from milainference.core.server_lookup import get_inference_servers
from milainference.core.metadata import job_metadata


class WaitFor(Command):
    """Wait for a model to come online"""

    @dataclass
    class Arguments:
        model: str = None   # Model name

    def execute(self, args):
        servers = get_inference_servers(args.model, pending_ok=True)
        ready = len(servers) == 0
        selected_server = None
        newlist = []
        start = time.time()
        newline = False

        try:
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
        except KeyboardInterrupt:
            pass

        if newline:
            print()

        if selected_server:
            print("The following server is ready")
            print(f"   {selected_server}")
        else:
            print("No pending server found")


COMMANDS = WaitFor
