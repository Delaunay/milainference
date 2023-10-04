from milainference.args.arguments import ParentCommand

class Cmd(ParentCommand):
    """Send an inference request to a server"""

    @staticmethod
    def module():
        import milainference.core.commands.cmd

        return milainference.core.commands.cmd


COMMANDS = Cmd
