Writers
=======

.. currentmodule:: cubeforge

The writer system provides a flexible way to export meshes to different file formats.

Writer Factory
--------------

.. autofunction:: get_writer

Writer Base Class
-----------------

.. autoclass:: MeshWriterBase
   :members:
   :undoc-members:
   :show-inheritance:

STL Writers
-----------

STL ASCII Writer
~~~~~~~~~~~~~~~~

.. autoclass:: StlAsciiWriter
   :members:
   :undoc-members:
   :show-inheritance:

STL Binary Writer
~~~~~~~~~~~~~~~~~

.. autoclass:: StlBinaryWriter
   :members:
   :undoc-members:
   :show-inheritance:

Using Writers
-------------

Direct Writer Usage
~~~~~~~~~~~~~~~~~~~

While most users will use ``VoxelModel.save_mesh()``, you can also use writers directly:

.. code-block:: python

   import cubeforge

   # Create model and generate mesh
   model = cubeforge.VoxelModel()
   model.add_voxel(0, 0, 0)
   triangles = model.generate_mesh()

   # Get a writer and use it
   writer = cubeforge.get_writer('stl_binary')
   writer.write("output.stl", triangles, solid_name="MyShape")

Supported Formats
~~~~~~~~~~~~~~~~~

Currently supported format identifiers:

- ``'stl'``: Binary STL (default)
- ``'stl_binary'``: Binary STL (explicit)
- ``'stl_ascii'``: ASCII STL

Creating Custom Writers
-----------------------

You can extend the writer system by subclassing ``MeshWriterBase``:

.. code-block:: python

   import cubeforge

   class MyCustomWriter(cubeforge.MeshWriterBase):
       def write(self, filename, triangles, **kwargs):
           """Write mesh to custom format."""
           with open(filename, 'w') as f:
               # Implement your custom format here
               for triangle in triangles:
                   normal, v1, v2, v3 = triangle
                   # Write triangle data
                   pass

   # Use your custom writer
   writer = MyCustomWriter()
   model = cubeforge.VoxelModel()
   model.add_voxel(0, 0, 0)
   triangles = model.generate_mesh()
   writer.write("output.custom", triangles)

STL Format Details
------------------

Binary STL Format
~~~~~~~~~~~~~~~~~

The binary STL format structure:

1. 80-byte header (CubeForge uses "cubeforge_model")
2. 4-byte unsigned integer: triangle count
3. For each triangle:

   - 12 bytes: normal vector (3 × 4-byte float)
   - 12 bytes: vertex 1 (3 × 4-byte float)
   - 12 bytes: vertex 2 (3 × 4-byte float)
   - 12 bytes: vertex 3 (3 × 4-byte float)
   - 2 bytes: attribute byte count (unused, set to 0)

Total size: 84 + (50 × triangle_count) bytes

ASCII STL Format
~~~~~~~~~~~~~~~~

The ASCII STL format structure:

.. code-block:: text

   solid <name>
     facet normal nx ny nz
       outer loop
         vertex v1x v1y v1z
         vertex v2x v2y v2z
         vertex v3x v3y v3z
       endloop
     endfacet
     ...
   endsolid <name>

.. note::
   Binary STL files are typically 5-10× smaller than ASCII STL files and load faster in most applications.

File Size Comparison
--------------------

For a typical 1000-voxel model:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Format
     - File Size
     - Notes
   * - Binary STL (optimized)
     - ~5 KB
     - Recommended
   * - Binary STL (unoptimized)
     - ~500 KB
     - Use optimization!
   * - ASCII STL (optimized)
     - ~25 KB
     - Human-readable
   * - ASCII STL (unoptimized)
     - ~2.5 MB
     - Very large
