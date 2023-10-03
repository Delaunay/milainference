import json
import os

import importlib_resources


_datapath = importlib_resources.files("milainference.data")
_namespaces = None


def huggingface_namespace_to_path(namespace):
    global _namespaces

    if _namespaces is None:
        with open(_datapath / "namespace.json", encoding="utf-8") as file:
            _namespaces = json.load(file)

    return _namespaces.get(namespace)


def model_name_to_loc(model):
    try:
        namespace, name = model.splt("/")
        p = huggingface_namespace_to_path(namespace)
        return os.path.join(p, name)
    except:
        return model
