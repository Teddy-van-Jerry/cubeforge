Installation
============

Requirements
------------

CubeForge requires Python 3.8 or higher.

Install from PyPI
-----------------

The easiest way to install CubeForge is using pip:

.. code-block:: bash

   pip install cubeforge

This will install the latest stable version from PyPI.

Install from Source
-------------------

If you want to install the development version or contribute to the project, you can install from source:

.. code-block:: bash

   git clone https://github.com/Teddy-van-Jerry/cubeforge.git
   cd cubeforge
   pip install -e .

The ``-e`` flag installs the package in editable mode, which is useful for development.

Verify Installation
-------------------

You can verify that CubeForge is installed correctly by importing it in Python:

.. code-block:: python

   import cubeforge
   print(cubeforge.__version__)

This should print the version number without any errors.
