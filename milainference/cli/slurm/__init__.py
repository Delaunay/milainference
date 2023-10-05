from milainference.args.arguments import ParentCommand


class Slurm(ParentCommand):
    """Tools to interface with slurm"""

    @staticmethod
    def module():
        import milainference.cli.slurm

        return milainference.cli.slurm


COMMANDS = Slurm
