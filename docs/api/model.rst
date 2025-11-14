VoxelModel
==========

.. currentmodule:: cubeforge

.. autoclass:: VoxelModel
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

Class Overview
--------------

The ``VoxelModel`` class is the main interface for creating voxel-based 3D models in CubeForge.

Key Methods
-----------

Model Creation
~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   VoxelModel.__init__

Adding Voxels
~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   VoxelModel.add_voxel
   VoxelModel.add_voxels

Removing Voxels
~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   VoxelModel.remove_voxel
   VoxelModel.clear

Mesh Generation
~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   VoxelModel.generate_mesh
   VoxelModel.save_mesh

Example Usage
-------------

Basic usage::

    import cubeforge

    # Create a model
    model = cubeforge.VoxelModel(
        voxel_dimensions=(1.0, 1.0, 1.0),
        coordinate_system='z_up'
    )

    # Add voxels
    model.add_voxel(0, 0, 0)
    model.add_voxel(1, 0, 0)

    # Generate and save mesh
    model.save_mesh("output.stl")
