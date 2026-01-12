Examples
========

This page provides several complete examples demonstrating CubeForge's features.

Simple L-Shape
--------------

Create a basic L-shaped structure:

.. code-block:: python

   import cubeforge

   model = cubeforge.VoxelModel(voxel_dimensions=(10.0, 10.0, 10.0))
   model.add_voxels([
       (0, 0, 0), (10, 0, 0), (20, 0, 0), (20, 10, 0), (20, 20, 0)
   ], anchor=cubeforge.CubeAnchor.CORNER_NEG)

   model.save_mesh("l_shape.stl", format='stl_binary', solid_name="LShape")

Non-Uniform Voxels
------------------

Create a structure with non-cubic voxels:

.. code-block:: python

   import cubeforge

   # Define non-uniform dimensions (width=2, height=1, depth=3)
   model = cubeforge.VoxelModel(voxel_dimensions=(2.0, 1.0, 3.0))

   # Add voxels aligned to the grid
   model.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)
   model.add_voxel(2, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)
   model.add_voxel(0, 1, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)

   model.save_mesh("non_uniform.stl", format='stl_binary')

.. note::
   Per-voxel dimensions are snapped to the model grid spacing (multiples of ``voxel_dimensions``).

Anchor Point Demonstration
---------------------------

Demonstrate different anchor points:

.. code-block:: python

   import cubeforge

   model = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))

   # Place voxels using different anchors
   model.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)
   model.add_voxel(2.5, 0.5, 0.5, anchor=cubeforge.CubeAnchor.CENTER)
   model.add_voxel(5, 1, 1, anchor=cubeforge.CubeAnchor.CORNER_POS)
   model.add_voxel(7, 0, 0.5, anchor=cubeforge.CubeAnchor.BOTTOM_CENTER)
   model.add_voxel(9.5, 1, 0.5, anchor=cubeforge.CubeAnchor.TOP_CENTER)

   model.save_mesh("anchor_demo.stl")

Random Height Surface (Y-up)
-----------------------------

Create a surface with random heights using Y-up mode:

.. code-block:: python

   import cubeforge
   import random

   grid_size = 32
   voxel_dim = (1.0, 0.77, 0.23)

   model = cubeforge.VoxelModel(
       voxel_dimensions=voxel_dim,
       coordinate_system='y_up'
   )

   for x in range(grid_size):
       for z in range(grid_size):
           # Random height between 1 and 6 voxel layers
           height_layers = random.randint(1, 6)
           height = voxel_dim[1] * height_layers

           model.add_voxel(
               x * voxel_dim[0],
               0,
               z * voxel_dim[2],
               dimensions=(voxel_dim[0], height, voxel_dim[2]),
               anchor=cubeforge.CubeAnchor.CORNER_NEG
           )

   model.save_mesh("surface_y_up.stl", format='stl_binary')

Random Height Surface (Z-up)
-----------------------------

Same structure in Z-up mode for correct 3D printing orientation:

.. code-block:: python

   import cubeforge
   import random

   grid_size = 32
   voxel_dim = (1.0, 0.77, 0.23)

   model = cubeforge.VoxelModel(
       voxel_dimensions=voxel_dim,
       coordinate_system='z_up'
   )

   for x in range(grid_size):
       for y in range(grid_size):
           # Random height between 1 and 6 voxel layers
           height_layers = random.randint(1, 6)
           height = voxel_dim[2] * height_layers

           model.add_voxel(
               x * voxel_dim[0],
               y * voxel_dim[1],
               0,
               dimensions=(voxel_dim[0], voxel_dim[1], height),
               anchor=cubeforge.CubeAnchor.CORNER_NEG
           )

   model.save_mesh("surface_z_up.stl", format='stl_binary')

Stacked Tower with Varying Dimensions
--------------------------------------

Create a tower with different sized sections:

.. code-block:: python

   import cubeforge

   model = cubeforge.VoxelModel(
       voxel_dimensions=(1.0, 1.0, 1.0),
       coordinate_system='z_up'
   )

   # Base: wide and short
   model.add_voxel(
       0, 0, 0,
       dimensions=(5.0, 5.0, 2.0),
       anchor=cubeforge.CubeAnchor.BOTTOM_CENTER
   )

   # Middle: medium sized
   model.add_voxel(
       0, 0, 2.0,
       dimensions=(3.0, 3.0, 3.0),
       anchor=cubeforge.CubeAnchor.BOTTOM_CENTER
   )

   # Top: narrow and tall
   model.add_voxel(
       0, 0, 5.0,
       dimensions=(1.0, 1.0, 4.0),
       anchor=cubeforge.CubeAnchor.BOTTOM_CENTER
   )

   model.save_mesh("tower.stl", format='stl_binary')

Comparing Optimization
----------------------

Compare file sizes with and without optimization:

.. code-block:: python

   import cubeforge
   import os

   # Create a 20×20 surface
   model = cubeforge.VoxelModel(coordinate_system='z_up')
   for x in range(20):
       for y in range(20):
           model.add_voxel(x, y, 0)

   # Save both versions
   model.save_mesh("optimized.stl", optimize=True)
   model.save_mesh("unoptimized.stl", optimize=False)

   # Print file sizes
   opt_size = os.path.getsize("optimized.stl")
   unopt_size = os.path.getsize("unoptimized.stl")

   print(f"Optimized: {opt_size:,} bytes")
   print(f"Unoptimized: {unopt_size:,} bytes")
   print(f"Reduction: {100 * (1 - opt_size / unopt_size):.1f}%")

More Examples
-------------

You can find more examples in the `examples/ directory <https://github.com/Teddy-van-Jerry/cubeforge/tree/master/examples>`_ of the GitHub repository, including:

- ``create_shapes.py``: Comprehensive examples of all features
- ``coordinate_systems.py``: Comparing Y-up vs Z-up modes
- ``mesh_optimization.py``: Performance measurements for optimization
