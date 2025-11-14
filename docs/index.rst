CubeForge
=======================

**CubeForge** is a Python library designed to easily generate 3D mesh files (currently STL format) by defining models voxel by voxel. It allows for flexible voxel dimensions and positioning using various anchor points.

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

Features
--------

- **Voxel-based Modeling:** Define 3D shapes by adding individual voxels (cubes).
- **Non-Uniform Voxel Dimensions:** Specify default non-uniform dimensions for a model, and override dimensions on a per-voxel basis.
- **Flexible Anchoring:** Position voxels using different anchor points like corners or centers.
- **Configurable Coordinate Systems:** Choose between Y-up (default) or Z-up coordinate systems for compatibility with different tools.
- **Mesh Optimization:** Optional greedy meshing algorithm reduces file sizes by 10-100× for regular structures.
- **STL Export:** Save the generated mesh to both ASCII and Binary STL file formats.
- **Simple API:** Easy-to-use interface with the core VoxelModel class.

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install cubeforge

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import cubeforge

   # Create a model with default 1x1x1 voxel dimensions
   model = cubeforge.VoxelModel()

   # Add some voxels
   model.add_voxel(0, 0, 0)
   model.add_voxel(1, 0, 0)
   model.add_voxel(1, 1, 0)

   # Save the mesh as a binary STL file
   model.save_mesh("my_shape.stl", format='stl_binary')

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   coordinate_systems
   mesh_optimization
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/model
   api/constants
   api/writers

.. toctree::
   :maxdepth: 1
   :caption: Development

   changelog
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
