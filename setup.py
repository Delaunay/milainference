#!/usr/bin/env python
import os
from pathlib import Path

from setuptools import setup

with open("milainference/core/__init__.py") as file:
    for line in file.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break

assert (
    os.path.exists(os.path.join("milainference", "__init__.py")) is False
), "milainference is a namespace not a module"

extra_requires = {"plugins": ["importlib_resources"]}
extra_requires["all"] = sorted(set(sum(extra_requires.values(), [])))

if __name__ == "__main__":
    setup(
        name="milainference",
        version=version,
        extras_require=extra_requires,
        description="Supporting library for quick inference on the mila cluster",
        long_description=(Path(__file__).parent / "README.rst").read_text(),
        author="Delaunay",
        author_email="pierre.delaunay@mila.quebec",
        license="BSD 3-Clause License",
        url="https://milainference.readthedocs.io",
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Operating System :: OS Independent",
        ],
        packages=[
            "milainference.core",
            "milainference.args",
            "milainference.cli",
            "milainference.cli.server",
            "milainference.cli.slurm",
            "milainference.plugins.example",
        ],
        setup_requires=["setuptools"],
        install_requires=[
            "importlib_resources",
            "vllm",
            "openai",
            "simple_parsing",
            "rich",
        ],
        namespace_packages=[
            "milainference",
            "milainference.plugins",
        ],
        package_data={
            "milainference.data": [
                "milainference/data",
            ],
        },
        entry_points={
            "console_scripts": [
                "milainfer = milainference.core.cli:main",
            ],
        }
    )
