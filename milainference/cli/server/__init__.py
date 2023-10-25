from argklass.command import ParentCommand


class Server(ParentCommand):
    """Tools to help user launch and manage servers"""

    name: str = "server"

    @staticmethod
    def module():
        import milainference.cli.server

        return milainference.cli.server


COMMANDS = Server
