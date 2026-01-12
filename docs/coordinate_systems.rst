Coordinate Systems
==================

CubeForge supports two coordinate system modes to ensure compatibility with different 3D tools and workflows.

Y-up Mode (Default)
-------------------

In Y-up mode, the Y axis represents the vertical/height direction:

- Coordinates: ``(x, y, z)`` where y is up
- Dimensions: ``(x_size, y_size, z_size)`` where ``y_size`` is the vertical dimension
- ``BOTTOM_CENTER``/``TOP_CENTER`` anchors refer to Y faces (top/bottom)

.. note::
   Models created in Y-up mode will appear rotated 90° in most STL viewers and 3D printing slicers, which expect Z-up orientation.

Example:

.. code-block:: python

   import cubeforge

   # Create model in Y-up mode (default)
   model = cubeforge.VoxelModel(
       voxel_dimensions=(1.0, 1.0, 1.0),
       coordinate_system='y_up'
   )

   # Stack voxels vertically along Y axis
   for y in range(5):
       model.add_voxel(0, y, 0)

   model.save_mesh("tower_y_up.stl")

Z-up Mode (Recommended for 3D Printing)
----------------------------------------

In Z-up mode, the Z axis represents the vertical/height direction:

- Coordinates: ``(x, y, z)`` where z is up
- Dimensions: ``(x_size, y_size, z_size)`` where ``z_size`` is the vertical dimension
- ``BOTTOM_CENTER``/``TOP_CENTER`` anchors refer to Z faces (top/bottom)

.. important::
   This mode ensures exported STL files appear correctly oriented in most 3D printing slicers and CAD programs.

Example:

.. code-block:: python

   import cubeforge

   # Create model in Z-up mode (recommended for 3D printing)
   model = cubeforge.VoxelModel(
       voxel_dimensions=(1.0, 1.0, 1.0),
       coordinate_system='z_up'
   )

   # Stack voxels vertically along Z axis
   for z in range(5):
       model.add_voxel(0, 0, z)

   model.save_mesh("tower_z_up.stl")

Dimension Ordering
------------------

.. important::
   Dimensions are **always** specified as ``(x_size, y_size, z_size)`` in axis order, regardless of coordinate system. The coordinate system only determines which axis is vertical.

Creating Vertical Structures for 3D Printing
---------------------------------------------

Here's a complete example of creating a vertical tower correctly oriented for 3D printing:

.. code-block:: python

   import cubeforge

   # Use Z-up mode for correct STL orientation
   model = cubeforge.VoxelModel(
       voxel_dimensions=(1.0, 1.0, 1.0),
       coordinate_system='z_up'
   )

   # Build a tower with varying cross-sections
   for z in range(10):
       size = max(1.0, 3.0 - (z // 3))  # Taper in grid-aligned steps
       model.add_voxel(
           0, 0, z,
           dimensions=(size, size, 1.0),
           anchor=cubeforge.CubeAnchor.BOTTOM_CENTER
       )

   # Save - will appear correctly oriented in slicers!
   model.save_mesh("tapered_tower.stl", format='stl_binary')

Comparing Y-up vs Z-up
-----------------------

The following example creates the same structure in both modes:

.. code-block:: python

   import cubeforge

   # Y-up mode: height varies along Y
   model_y = cubeforge.VoxelModel(
       voxel_dimensions=(1.0, 1.0, 1.0),
       coordinate_system='y_up'
   )
   for y in range(5):
       model_y.add_voxel(0, y, 0)
   model_y.save_mesh("tower_y_up.stl")

   # Z-up mode: height varies along Z
   model_z = cubeforge.VoxelModel(
       voxel_dimensions=(1.0, 1.0, 1.0),
       coordinate_system='z_up'
   )
   for z in range(5):
       model_z.add_voxel(0, 0, z)
   model_z.save_mesh("tower_z_up.stl")

When viewed in an STL viewer, ``tower_z_up.stl`` will appear upright, while ``tower_y_up.stl`` will appear rotated 90°.

Implementation Details
----------------------

Internally, CubeForge:

1. Always stores voxels in Y-up representation
2. Swaps Y and Z coordinates when in Z-up mode at API boundaries
3. Swaps Y and Z in output vertices and normals when generating meshes in Z-up mode
4. Reverses triangle winding order in Z-up mode (because swapping creates a reflection)

This ensures consistent behavior while maintaining compatibility with standard STL conventions.
