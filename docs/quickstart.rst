Quick Start Guide
=================

This guide will help you get started with CubeForge quickly.

Creating Your First Model
--------------------------

Here's a simple example that creates an L-shaped structure:

.. code-block:: python

   import cubeforge

   # Create a model with 10x10x10 mm voxels
   model = cubeforge.VoxelModel(voxel_dimensions=(10.0, 10.0, 10.0))

   # Add voxels to form an L-shape
   model.add_voxels([
       (0, 0, 0), (10, 0, 0), (20, 0, 0), (20, 10, 0), (20, 20, 0)
   ], anchor=cubeforge.CubeAnchor.CORNER_NEG)

   # Save as binary STL
   model.save_mesh("l_shape.stl", format='stl_binary', solid_name="LShape")

Understanding Voxel Dimensions
-------------------------------

Voxel dimensions are always specified as ``(x_size, y_size, z_size)`` in axis order:

.. code-block:: python

   # Create a model with non-uniform voxels
   model = cubeforge.VoxelModel(voxel_dimensions=(2.0, 1.0, 3.0))

   # This creates voxels that are:
   # - 2 units wide (X direction)
   # - 1 unit tall (Y direction, or Z in Z-up mode)
   # - 3 units deep (Z direction, or Y in Z-up mode)

Anchor Points
-------------

Anchor points determine where the coordinates you provide correspond to on the voxel:

.. code-block:: python

   import cubeforge

   model = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))

   # Place voxel with minimum corner at origin
   model.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)

   # Place voxel with center at (2, 0, 0)
   model.add_voxel(2, 0, 0, anchor=cubeforge.CubeAnchor.CENTER)

   # Place voxel with maximum corner at (4, 0, 0)
   model.add_voxel(4, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_POS)

Available anchor points:

- ``CORNER_NEG``: Minimum corner (default)
- ``CENTER``: Geometric center
- ``CORNER_POS``: Maximum corner
- ``BOTTOM_CENTER``: Center of bottom face
- ``TOP_CENTER``: Center of top face

Custom Dimensions Per Voxel
----------------------------

You can override dimensions for individual voxels:

.. code-block:: python

   model = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))

   # Add a 1x1x1 base cube
   model.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CENTER)

   # Add a wide, flat 3x0.5x3 cube on top
   model.add_voxel(
       0, 0.5, 0,
       anchor=cubeforge.CubeAnchor.BOTTOM_CENTER,
       dimensions=(3.0, 0.5, 3.0)
   )

Saving to Different Formats
----------------------------

CubeForge supports both ASCII and binary STL formats:

.. code-block:: python

   # Binary STL (default, smaller file size)
   model.save_mesh("output.stl", format='stl_binary')

   # ASCII STL (human-readable, larger file size)
   model.save_mesh("output_ascii.stl", format='stl_ascii')

Next Steps
----------

- Learn about :doc:`coordinate_systems` for 3D printing compatibility
- Discover :doc:`mesh_optimization` to reduce file sizes
- Browse :doc:`examples` for more complex use cases
