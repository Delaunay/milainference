import glob
import os
import traceback

from milainference.args.argformat import HelpAction, HelpActionException


def _resolve_factory_module(base_file_name, base_module, function_name, module_path):
    module_file = module_path.split(os.sep)[-1]

    if module_file == base_file_name:
        return

    module_name = module_file.split(".py")[0]

    try:
        module = __import__(".".join([base_module, module_name]), fromlist=[""])
    
        if hasattr(module, function_name):
            return getattr(module, function_name)

    except ImportError:
        print(traceback.format_exc())
        return
    


def fetch_factories(registry, base_module, base_file_name, function_name="COMMANDS"):
    """Loads all the defined commands"""
    module_path = os.path.abspath(base_file_name)

    for module_path in glob.glob(
        os.path.join(module_path, "[A-Za-z]*"), recursive=False
    ):
        _, tail = os.path.split(module_path)
        cmd = tail.replace('.py', '')

        cmdcls = _resolve_factory_module(base_file_name, base_module, function_name, module_path)
        
        if cmdcls is not None:
            if not hasattr(cmdcls, 'name'):
                cmdcls.name = cmd
            
            registry.insert_commands(cmdcls)


# pylint: disable=too-few-public-methods
class CommandRegistry:
    """Simple class to keep track of all the commands we find"""

    def __init__(self):
        self.found_commands = {}

    def insert_commands(self, cmds):
        """Insert a command into the registry makes sure it is unique"""
        if not isinstance(cmds, list):
            cmds = [cmds]

        for cmdcls in cmds:
            cmd = cmdcls()

            if cmd.name != cmd.name.strip():
                print(f"Warning: {cmd.name} has white space before or after the name")

            assert (
                cmd.name not in self.found_commands
            ), f"Duplicate command name: {cmd.name}"
            self.found_commands[cmd.name] = cmd


def _discover_commands(module):
    """Discover all the commands we can find (plugins and built-in)"""

    base = os.path.dirname(module.__file__)
    name = module.__name__

    registry = CommandRegistry()
    fetch_factories(registry, name, base)

    return registry


def discover_commands(module):
    return _discover_commands(module).found_commands

