milainference
=============================

|pypi| |py_versions| |codecov| |docs| |tests| |style|

.. |pypi| image:: https://img.shields.io/pypi/v/milainference.svg
    :target: https://pypi.python.org/pypi/milainference
    :alt: Current PyPi Version

.. |py_versions| image:: https://img.shields.io/pypi/pyversions/milainference.svg
    :target: https://pypi.python.org/pypi/milainference
    :alt: Supported Python Versions

.. |codecov| image:: https://codecov.io/gh/Delaunay/milainference/branch/master/graph/badge.svg?token=40Cr8V87HI
   :target: https://codecov.io/gh/Delaunay/milainference

.. |docs| image:: https://readthedocs.org/projects/milainference/badge/?version=latest
   :target:  https://milainference.readthedocs.io/en/latest/?badge=latest

.. |tests| image:: https://github.com/Delaunay/milainference/actions/workflows/test.yml/badge.svg?branch=master
   :target: https://github.com/Delaunay/milainference/actions/workflows/test.yml

.. |style| image:: https://github.com/Delaunay/milainference/actions/workflows/style.yml/badge.svg?branch=master
   :target: https://github.com/Delaunay/milainference/actions/workflows/style.yml



.. code-block:: bash

   pip install milainference


Examples
--------


.. code-block:: bash

   ssh mila

   salloc ....

   # Launch a server (launch a slurm job and exit)
   milainfer server launch --model Llama-2-7b-chat-hf /network/weights/llama.var/llama2/Llama-2-7b-chat-hf --sync --time=00:30:00

   # List all the available inference servers
   milainfer list

   # Wait for a specific model to be online
   milainfer waitfor --model Llama-2-7b-chat-hf

   # Get on a compute node and use the server for inference
   milainfer client --prompt "Give me good advices"
