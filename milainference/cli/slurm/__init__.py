from argklass.command import ParentCommand


class Slurm(ParentCommand):
    """Tools to interface with slurm"""

    name: str = "slurm"

    @staticmethod
    def module():
        import milainference.cli.slurm

        return milainference.cli.slurm


COMMANDS = Slurm
