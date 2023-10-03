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

   # Launch a server (launch a slurm job and exit)
   milainfer server --model meta-llama/Llama-2-7b-chat-hf

   # List all the available inference servers
   milainfer list

   # Get on a compute node and use the server for inference
   salloc ....
   milainfer client --prompt "Give me good advices"


Issues
------

* Detect a server that is in the process of being operational but that is not yet ready
   * we need to add a state to the job metadata
   * scontrol update job $SLURM_JOB_ID comment="model=$MODEL|host=$HOST|port=$PORT|state=0|shared=y"
   * ...
   * scontrol update job $SLURM_JOB_ID comment="model=$MODEL|host=$HOST|port=$PORT|state=1|shared=y"
   * PROBLEM: are we going to be able ot change the state when the server is really ready ?
   

* Detect a server that is operational but that is about to NOT be
   * Job time out: this is easy to detect
