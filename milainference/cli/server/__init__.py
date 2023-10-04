from milainference.args.arguments import ParentCommand

class Server(ParentCommand):
    """Tools to help user launch and manage servers"""

    @staticmethod
    def module():
        import milainference.cli.server

        return milainference.cli.server


COMMANDS = Server
