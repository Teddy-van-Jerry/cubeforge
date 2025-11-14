Changelog
=========

Version 0.2.2 (2025-11-14)
--------------------------

Bug Fixes
~~~~~~~~~

* Fixed dimension handling for custom per-voxel dimensions in Z-up mode
* Corrected double-swapping issue where dimensions were swapped during storage and again during mesh generation
* Fixed greedy meshing algorithm to properly handle non-uniform voxel dimensions in Z-up mode

Improvements
~~~~~~~~~~~~

* Improved internal dimension storage to maintain consistency across coordinate systems
* Enhanced mesh generation to use pre-swapped dimensions from storage

Version 0.2.1 (2025-11-13)
--------------------------

Features
~~~~~~~~

* Added configurable coordinate systems (Y-up and Z-up modes)
* Added greedy meshing optimization (enabled by default)
* Significant file size reduction (10-100×) for regular structures

API Changes
~~~~~~~~~~~

* Added ``coordinate_system`` parameter to ``VoxelModel.__init__()``
* Added ``optimize`` parameter to ``save_mesh()`` and ``generate_mesh()``
* Removed deprecated ``set_y_up()`` and ``set_z_up()`` methods

Bug Fixes
~~~~~~~~~

* Fixed normal direction for Z-up mode meshes
* Fixed triangle winding order in Z-up mode (handles reflection properly)
* Fixed dimension swapping in coordinate system conversion

Documentation
~~~~~~~~~~~~~

* Added comprehensive coordinate system documentation
* Added mesh optimization guide
* Updated all examples to show both Y-up and Z-up usage

Version 0.2.0 (2025-07-11)
--------------------------

Features
~~~~~~~~

* Renamed core methods for clarity:

  * ``add_cube()`` → ``add_voxel()``
  * ``add_cubes()`` → ``add_voxels()``
  * ``remove_cube()`` → ``remove_voxel()``

* Added support for custom dimensions per voxel
* Changed initialization parameter from ``cube_size`` to ``voxel_dimensions``
* Added support for non-uniform voxel dimensions (different x, y, z sizes)

API Changes
~~~~~~~~~~~

* **Breaking:** ``cube_size`` parameter renamed to ``voxel_dimensions``
* **Breaking:** ``cube_size`` now accepts tuples for non-uniform dimensions
* Old method names kept as aliases for backward compatibility

Version 0.1.x
-------------

* Initial release
* Basic voxel-based mesh generation
* STL export (ASCII and binary)
* Anchor point system
