Constants
=========

.. currentmodule:: cubeforge

CubeAnchor
----------

.. autoclass:: CubeAnchor
   :members:
   :undoc-members:
   :show-inheritance:

Anchor Points
-------------

The ``CubeAnchor`` enum defines reference points for voxel positioning:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Anchor Point
     - Description
   * - ``CORNER_NEG``
     - Minimum corner (x_min, y_min, z_min). Default anchor point.
   * - ``CENTER``
     - Geometric center of the voxel.
   * - ``CORNER_POS``
     - Maximum corner (x_max, y_max, z_max).
   * - ``BOTTOM_CENTER``
     - Center of the bottom face (min Y in Y-up mode, min Z in Z-up mode).
   * - ``TOP_CENTER``
     - Center of the top face (max Y in Y-up mode, max Z in Z-up mode).

Example Usage
-------------

Using different anchor points::

    import cubeforge

    model = cubeforge.VoxelModel()

    # Place voxel with minimum corner at origin
    model.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)

    # Place voxel centered at (5, 5, 5)
    model.add_voxel(5, 5, 5, anchor=cubeforge.CubeAnchor.CENTER)

    # Place voxel with maximum corner at (10, 10, 10)
    model.add_voxel(10, 10, 10, anchor=cubeforge.CubeAnchor.CORNER_POS)

Coordinate System Behavior
---------------------------

The ``BOTTOM_CENTER`` and ``TOP_CENTER`` anchors behave differently depending on the coordinate system:

**Y-up mode** (default):
  - ``BOTTOM_CENTER``: Center of minimum Y face
  - ``TOP_CENTER``: Center of maximum Y face

**Z-up mode** (recommended for 3D printing):
  - ``BOTTOM_CENTER``: Center of minimum Z face
  - ``TOP_CENTER``: Center of maximum Z face

Example with coordinate systems::

    import cubeforge

    # Y-up mode: TOP_CENTER refers to max Y face
    model_y = cubeforge.VoxelModel(coordinate_system='y_up')
    model_y.add_voxel(0, 5, 0, anchor=cubeforge.CubeAnchor.TOP_CENTER)

    # Z-up mode: TOP_CENTER refers to max Z face
    model_z = cubeforge.VoxelModel(coordinate_system='z_up')
    model_z.add_voxel(0, 0, 5, anchor=cubeforge.CubeAnchor.TOP_CENTER)
