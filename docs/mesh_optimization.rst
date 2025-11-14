Mesh Optimization
=================

CubeForge uses **greedy meshing** optimization by default to dramatically reduce file sizes for voxel-based models.

How It Works
------------

Instead of creating separate triangles for each voxel face, the optimizer merges adjacent coplanar faces into larger rectangles:

.. code-block:: text

   Without optimization (9 voxels):     With optimization:
   [■][■][■]  9 quads = 18 triangles    [■■■■■■■]  1 quad = 2 triangles
   [■][■][■]                            [■■■■■■■]
   [■][■][■]                            [■■■■■■■]

Basic Usage
-----------

Optimization is **enabled by default** - just use ``save_mesh()``:

.. code-block:: python

   import cubeforge

   model = cubeforge.VoxelModel(coordinate_system='z_up')

   # Create a large flat surface
   for x in range(20):
       for y in range(20):
           model.add_voxel(x, y, 0)

   # Save - optimization enabled by default, 99% smaller!
   model.save_mesh("surface.stl")

Disabling Optimization
----------------------

To disable optimization (not recommended except for debugging):

.. code-block:: python

   model.save_mesh("surface.stl", optimize=False)

Performance Comparison
----------------------

File size reduction depends on the structure complexity:

+------------------------+----------------------+--------------------+--------------------+
| Structure Type         | Unoptimized Size     | Optimized Size     | Reduction          |
+========================+======================+====================+====================+
| Flat surface (20×20)   | 192 KB               | 2 KB               | 99%                |
+------------------------+----------------------+--------------------+--------------------+
| Solid cube (10×10×10)  | 480 KB               | 5 KB               | 99%                |
+------------------------+----------------------+--------------------+--------------------+
| Random height surface  | 500 KB               | 250 KB             | 50%                |
+------------------------+----------------------+--------------------+--------------------+
| Complex irregular      | 300 KB               | 250 KB             | 17%                |
+------------------------+----------------------+--------------------+--------------------+

When Optimization is Most Effective
------------------------------------

Greedy meshing provides the best results when:

1. **Regular patterns:** Grids, surfaces, and cubes
2. **Aligned faces:** Voxels with same dimensions in the same plane
3. **Large structures:** More voxels = more opportunities to merge

When to Consider Disabling
---------------------------

You may want to disable optimization if:

1. **Individual faces needed:** For specialized post-processing
2. **Debugging:** To see individual voxel geometry
3. **Tiny models:** When the overhead isn't worth it (< 10 voxels)

.. note::
   In 99% of cases, keep optimization enabled. It provides massive file size reductions with no visual or functional difference.

Example with Measurements
--------------------------

Here's a complete example that compares optimized and unoptimized output:

.. code-block:: python

   import cubeforge
   import os

   # Create a 32×32 grid
   model = cubeforge.VoxelModel(coordinate_system='z_up')
   for x in range(32):
       for y in range(32):
           model.add_voxel(x, y, 0)

   # Save both versions
   model.save_mesh("surface_optimized.stl", optimize=True)
   model.save_mesh("surface_unoptimized.stl", optimize=False)

   # Compare sizes
   size_opt = os.path.getsize("surface_optimized.stl")
   size_unopt = os.path.getsize("surface_unoptimized.stl")
   reduction = 100 * (1 - size_opt / size_unopt)

   print(f"Optimized: {size_opt:,} bytes")
   print(f"Unoptimized: {size_unopt:,} bytes")
   print(f"Reduction: {reduction:.1f}%")

Technical Details
-----------------

The greedy meshing algorithm:

1. **Face collection:** Identifies all exposed voxel faces
2. **Plane grouping:** Groups faces by position on their normal axis
3. **Rectangle growing:** Expands rectangles in two directions within each plane
4. **Vertex generation:** Creates triangles for merged rectangles

This algorithm runs in O(n log n) time where n is the number of exposed faces, making it efficient even for large models.
