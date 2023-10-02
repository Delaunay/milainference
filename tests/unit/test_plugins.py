import milainference.plugins
from milainference.core import discover_plugins


def test_plugins():
    plugins = discover_plugins(milainference.plugins)

    assert len(plugins) == 1
