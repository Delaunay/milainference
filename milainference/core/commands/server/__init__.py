from milainference.args.arguments import ParentCommand

class Server(ParentCommand):
    """Tools to help user launch and manage servers"""

    @staticmethod
    def module():
        import milainference.core.commands.server

        return milainference.core.commands.server


COMMANDS = Server
