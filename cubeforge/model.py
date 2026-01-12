# cubeforge/model.py
import logging
from .constants import CubeAnchor
from .writers import get_writer # Use the generalized writer system

# --- Logging Configuration Removed ---
# Get a logger instance for this module. Configuration is left to the application.
logger = logging.getLogger(__name__)


class VoxelModel:
    """
    Represents a 3D model composed of voxels.
    Each voxel can have independent dimensions (width, height, depth).

    Allows adding voxels based on coordinates and anchor points, and exporting
    the resulting shape using various mesh writers. Logging messages are emitted
    via the standard 'logging' module; configuration is up to the application.
    """
    def __init__(self, voxel_dimensions=(1.0, 1.0, 1.0), coordinate_system='y_up'):
        """
        Initializes the VoxelModel.

        Args:
            voxel_dimensions (tuple): A tuple of three positive numbers (x_size, y_size, z_size)
                                     representing the default size of each voxel along each axis.
                                     Always in (x, y, z) order regardless of coordinate system.
            coordinate_system (str): The coordinate system to use. Either 'y_up' (default)
                                    or 'z_up'. Use 'z_up' for 3D printing to ensure correct
                                    orientation in most slicers.
                                    - 'y_up': Y axis is vertical (mathematical convention)
                                    - 'z_up': Z axis is vertical (3D printing convention)
        """
        if not (isinstance(voxel_dimensions, (tuple, list)) and
                len(voxel_dimensions) == 3 and
                all(isinstance(dim, (int, float)) and dim > 0 for dim in voxel_dimensions)):
            raise ValueError("voxel_dimensions must be a tuple or list of three positive numbers.")
        if coordinate_system not in ('y_up', 'z_up'):
            raise ValueError("coordinate_system must be either 'y_up' or 'z_up'.")

        self.voxel_dimensions = tuple(float(dim) for dim in voxel_dimensions)
        # Stores voxel data as a dictionary:
        # key: integer grid coordinate (ix, iy, iz)
        # value: tuple of dimensions (width, height, depth) for that voxel
        self._voxels = {}
        # Coordinate system: 'y_up' (default) or 'z_up'
        self._coordinate_system = coordinate_system
        self._dimension_snap_warning_emitted = False
        logger.info(f"VoxelModel initialized with default voxel_dimensions={self.voxel_dimensions}, coordinate_system={coordinate_system}")

    def _swap_yz_if_needed(self, x, y, z):
        """Helper method to swap Y and Z coordinates when in Z-up mode."""
        if self._coordinate_system == 'z_up':
            return x, z, y
        return x, y, z

    def _calculate_min_corner(self, x, y, z, anchor, dimensions):
        """
        Calculates the minimum corner coordinates based on anchor point and voxel dimensions.

        Internal helper method used by add_voxel and remove_voxel.

        Args:
            x (float): X-coordinate of the anchor point.
            y (float): Y-coordinate of the anchor point.
            z (float): Z-coordinate of the anchor point.
            anchor (CubeAnchor): The anchor type.
            dimensions (tuple): The (width, height, depth) of the voxel.

        Returns:
            tuple: (min_x, min_y, min_z) coordinates of the voxel's minimum corner.

        Raises:
            ValueError: If an invalid anchor point is provided.
        """
        size_x, size_y, size_z = dimensions
        half_x, half_y, half_z = size_x / 2.0, size_y / 2.0, size_z / 2.0

        if anchor == CubeAnchor.CORNER_NEG:
            min_x, min_y, min_z = x, y, z
        elif anchor == CubeAnchor.CENTER:
            min_x, min_y, min_z = x - half_x, y - half_y, z - half_z
        elif anchor == CubeAnchor.CORNER_POS:
            min_x, min_y, min_z = x - size_x, y - size_y, z - size_z
        elif anchor == CubeAnchor.BOTTOM_CENTER:
            # In Y-up: center of min Y face; In Z-up: center of min Z face
            if self._coordinate_system == 'z_up':
                min_x, min_y, min_z = x - half_x, y - half_y, z
            else:
                min_x, min_y, min_z = x - half_x, y, z - half_z
        elif anchor == CubeAnchor.TOP_CENTER:
            # In Y-up: center of max Y face; In Z-up: center of max Z face
            if self._coordinate_system == 'z_up':
                min_x, min_y, min_z = x - half_x, y - half_y, z - size_z
            else:
                min_x, min_y, min_z = x - half_x, y - size_y, z - half_z
        else:
            raise ValueError(f"Invalid anchor point: {anchor}")

        return min_x, min_y, min_z

    def add_voxel(self, x, y, z, anchor=CubeAnchor.CORNER_NEG, dimensions=None):
        """
        Adds a voxel to the model. Replaces add_cube.

        Args:
            x (float): X-coordinate of the voxel's anchor point.
            y (float): Y-coordinate of the voxel's anchor point (Y-up mode) or
                      depth coordinate (Z-up mode).
            z (float): Z-coordinate of the voxel's anchor point (Y-up mode) or
                      vertical coordinate (Z-up mode).
            anchor (CubeAnchor): The reference point within the voxel that
                                (x, y, z) corresponds to. Defaults to
                                CubeAnchor.CORNER_NEG.
            dimensions (tuple, optional): Custom dimensions (x_size, y_size, z_size) for this voxel.
                                          Always in (x, y, z) order regardless of coordinate system.
                                          Dimensions are snapped to the model's voxel grid spacing.
                                          If None, the model's default dimensions are used.
        """
        # Swap coordinates if in Z-up mode
        x, y, z = self._swap_yz_if_needed(x, y, z)

        # Get dimensions and validate
        if dimensions is None:
            voxel_dims = self.voxel_dimensions
        else:
            voxel_dims = tuple(float(d) for d in dimensions)
            if not (isinstance(voxel_dims, (tuple, list)) and
                    len(voxel_dims) == 3 and
                    all(isinstance(d, (int, float)) and d > 0 for d in voxel_dims)):
                raise ValueError("Custom dimensions must be a tuple or list of three positive numbers.")
            # Swap custom dimensions if in Z-up mode to convert to internal Y-up representation
            if self._coordinate_system == 'z_up':
                voxel_dims = (voxel_dims[0], voxel_dims[2], voxel_dims[1])
            voxel_dims, snapped = self._snap_dimensions(voxel_dims)
            if snapped and not self._dimension_snap_warning_emitted:
                grid_dim_x, grid_dim_y, grid_dim_z = self._grid_dimensions()
                logger.warning(
                    "Custom voxel dimensions snapped to grid spacing (%.6f, %.6f, %.6f).",
                    grid_dim_x,
                    grid_dim_y,
                    grid_dim_z
                )
                self._dimension_snap_warning_emitted = True

        min_x, min_y, min_z = self._calculate_min_corner(x, y, z, anchor, voxel_dims)

        # Calculate grid coordinates based on minimum corner and *default* dimensions
        # This ensures voxels snap to a consistent grid.
        # In Z-up mode, we need to use swapped dimensions for grid calculation
        # because internally we work in Y-up space
        grid_dim_x, grid_dim_y, grid_dim_z = self.voxel_dimensions
        if self._coordinate_system == 'z_up':
            grid_dim_y, grid_dim_z = grid_dim_z, grid_dim_y

        raw_x = min_x / grid_dim_x
        raw_y = min_y / grid_dim_y
        raw_z = min_z / grid_dim_z
        grid_x = round(raw_x)
        grid_y = round(raw_y)
        grid_z = round(raw_z)
        # Warn if rounding actually occurred (i.e., not exactly on grid)
        if (grid_x != raw_x) or (grid_y != raw_y) or (grid_z != raw_z):
            logger.warning(
                f"Voxel at ({x}, {y}, {z}) with anchor {anchor} and dimensions {voxel_dims} "
                f"does not align exactly to grid; rounded from ({raw_x:.6f}, {raw_y:.6f}, {raw_z:.6f}) "
                f"to ({grid_x}, {grid_y}, {grid_z})"
            )

        grid_coord = (grid_x, grid_y, grid_z)
        self._voxels[grid_coord] = voxel_dims
        # logger.debug(f"Added voxel at grid {grid_coord} (from anchor {anchor} at ({x},{y},{z}))")

    # Alias add_cube to add_voxel for backward compatibility (optional, but can be helpful)
    add_cube = add_voxel

    def add_voxels(self, coordinates, anchor=CubeAnchor.CORNER_NEG, dimensions=None):
        """
        Adds multiple voxels from an iterable. Replaces add_cubes.

        Args:
            coordinates (iterable): An iterable of (x, y, z) tuples or lists.
            anchor (CubeAnchor): The anchor point to use for all voxels added
                                in this call.
            dimensions (tuple, optional): The dimensions to apply to all voxels
                                          in this call. Dimensions are snapped
                                          to the model's voxel grid spacing.
                                          If None, defaults are used.
        """
        for x_coord, y_coord, z_coord in coordinates:
            self.add_voxel(x_coord, y_coord, z_coord, anchor, dimensions)

    # Alias add_cubes to add_voxels
    add_cubes = add_voxels

    def remove_voxel(self, x, y, z, anchor=CubeAnchor.CORNER_NEG):
        """
        Removes a voxel from the model based on its anchor coordinates. Replaces remove_cube.

        Args:
            x (float): X-coordinate of the voxel's anchor point.
            y (float): Y-coordinate of the voxel's anchor point (Y-up mode) or
                      depth coordinate (Z-up mode).
            z (float): Z-coordinate of the voxel's anchor point (Y-up mode) or
                      vertical coordinate (Z-up mode).
            anchor (CubeAnchor): The reference point within the voxel that
                                (x, y, z) corresponds to.
        """
        # Swap coordinates if in Z-up mode
        x, y, z = self._swap_yz_if_needed(x, y, z)

        # Note: Removal does not need custom dimensions, as it identifies the
        # voxel by its position on the grid, which is calculated using default dimensions.
        min_x, min_y, min_z = self._calculate_min_corner(x, y, z, anchor, self.voxel_dimensions)

        raw_x = min_x / self.voxel_dimensions[0]
        raw_y = min_y / self.voxel_dimensions[1]
        raw_z = min_z / self.voxel_dimensions[2]
        grid_x = round(raw_x)
        grid_y = round(raw_y)
        grid_z = round(raw_z)
        if (grid_x != raw_x) or (grid_y != raw_y) or (grid_z != raw_z):
            logger.warning(
                f"Voxel removal at ({x}, {y}, {z}) with anchor {anchor} "
                f"does not align exactly to grid; rounded from "
                f"({raw_x:.6f}, {raw_y:.6f}, {raw_z:.6f}) to "
                f"({grid_x}, {grid_y}, {grid_z})"
            )

        grid_coord = (grid_x, grid_y, grid_z)
        if grid_coord in self._voxels:
            del self._voxels[grid_coord]
        # logger.debug(f"Attempted removal at grid {grid_coord}")

    # Alias remove_cube to remove_voxel
    remove_cube = remove_voxel

    def clear(self):
        """Removes all voxels from the model."""
        self._voxels.clear()
        logger.info("VoxelModel cleared.")

    def _grid_dimensions(self):
        grid_dim_x, grid_dim_y, grid_dim_z = self.voxel_dimensions
        if self._coordinate_system == 'z_up':
            grid_dim_y, grid_dim_z = grid_dim_z, grid_dim_y
        return grid_dim_x, grid_dim_y, grid_dim_z

    def _snap_to_grid(self, value, grid_dim, eps=1e-9):
        layers = int(round(value / grid_dim))
        if layers < 1:
            layers = 1
        snapped = layers * grid_dim
        return snapped, abs(snapped - value) > eps

    def _snap_dimensions(self, dimensions):
        grid_dim_x, grid_dim_y, grid_dim_z = self._grid_dimensions()
        snapped_dims = []
        changed = False
        for value, grid_dim in zip(dimensions, (grid_dim_x, grid_dim_y, grid_dim_z)):
            snapped, did_change = self._snap_to_grid(value, grid_dim)
            snapped_dims.append(snapped)
            changed = changed or did_change
        return tuple(snapped_dims), changed

    def _voxel_min_corner(self, grid_coord):
        grid_dim_x, grid_dim_y, grid_dim_z = self._grid_dimensions()
        gx, gy, gz = grid_coord
        return gx * grid_dim_x, gy * grid_dim_y, gz * grid_dim_z

    def _can_use_greedy_meshing(self):
        if not self._voxels:
            return False
        default_dims = self._grid_dimensions()
        return all(dims == default_dims for dims in self._voxels.values())

    def _append_face_rectangles(self, triangles, axis, direction, pos_on_axis, rectangles):
        normal = [0, 0, 0]
        normal[axis] = 1 if direction == 1 else -1
        normal = tuple(normal)

        output_normal = normal
        swap_output = self._coordinate_system == 'z_up'
        if swap_output:
            output_normal = (normal[0], normal[2], normal[1])

        for u0, v0, u1, v1 in rectangles:
            u_length = u1 - u0
            v_length = v1 - v0
            if u_length <= 0 or v_length <= 0:
                continue

            verts = self._build_rect_vertices(axis, direction, pos_on_axis,
                                              u0, v0, u_length, v_length)
            if swap_output:
                verts = [(v[0], v[2], v[1]) for v in verts]
                triangles.append((output_normal, verts[0], verts[2], verts[1]))
                triangles.append((output_normal, verts[0], verts[3], verts[2]))
            else:
                triangles.append((output_normal, verts[0], verts[1], verts[2]))
                triangles.append((output_normal, verts[0], verts[2], verts[3]))

    def _heightmap_mesh(self, optimize=False):
        grid_dim_x, grid_dim_y, grid_dim_z = self._grid_dimensions()
        eps = 1e-9

        heights = {}
        base_gy = None
        for (gx, gy, gz), (size_x, size_y, size_z) in self._voxels.items():
            if base_gy is None:
                base_gy = gy
            elif gy != base_gy:
                return None

            if abs(size_x - grid_dim_x) > eps or abs(size_z - grid_dim_z) > eps:
                return None

            key = (gx, gz)
            if key in heights:
                return None
            heights[key] = size_y

        if not heights:
            return []

        base_y = base_gy * grid_dim_y

        snapped = False
        quantized = {}
        for key, height in heights.items():
            layers = int(round(height / grid_dim_y))
            if layers < 1:
                layers = 1
            quant_height = layers * grid_dim_y
            if abs(quant_height - height) > eps:
                snapped = True
            quantized[key] = quant_height

        if snapped:
            logger.warning(
                "Heightmap meshing snapped voxel heights to grid spacing %.6f to avoid partial-height artifacts.",
                grid_dim_y
            )

        heights = quantized
        triangles = []

        unique_heights = sorted({0.0} | set(heights.values()))
        cells = list(heights.items())

        if optimize:
            uniform_dims = self._grid_dimensions()
            temp_model = VoxelModel(voxel_dimensions=self.voxel_dimensions, coordinate_system=self._coordinate_system)
            temp_model._voxels = {}
            for (gx, gz), height in heights.items():
                if height <= eps:
                    continue
                layers = int(round(height / grid_dim_y))
                for layer in range(layers):
                    temp_model._voxels[(gx, base_gy + layer, gz)] = uniform_dims
            return temp_model._greedy_mesh()

        for i in range(len(unique_heights) - 1):
            h0 = unique_heights[i]
            h1 = unique_heights[i + 1]
            if h1 <= h0 + eps:
                continue
            y0 = base_y + h0
            y1 = base_y + h1

            for (gx, gz), height in cells:
                if height <= h0 + eps:
                    continue
                x0 = gx * grid_dim_x
                x1 = x0 + grid_dim_x
                z0 = gz * grid_dim_z
                z1 = z0 + grid_dim_z

                if heights.get((gx - 1, gz), 0.0) <= h0 + eps:
                    rect = (y0, z0, y1, z1)
                    self._append_face_rectangles(triangles, axis=0, direction=0, pos_on_axis=x0, rectangles=[rect])
                if heights.get((gx + 1, gz), 0.0) <= h0 + eps:
                    rect = (y0, z0, y1, z1)
                    self._append_face_rectangles(triangles, axis=0, direction=1, pos_on_axis=x1, rectangles=[rect])
                if heights.get((gx, gz - 1), 0.0) <= h0 + eps:
                    rect = (x0, y0, x1, y1)
                    self._append_face_rectangles(triangles, axis=2, direction=0, pos_on_axis=z0, rectangles=[rect])
                if heights.get((gx, gz + 1), 0.0) <= h0 + eps:
                    rect = (x0, y0, x1, y1)
                    self._append_face_rectangles(triangles, axis=2, direction=1, pos_on_axis=z1, rectangles=[rect])

                if not optimize:
                    if height <= h1 + eps:
                        rect_top = (z0, x0, z1, x1)
                        self._append_face_rectangles(triangles, axis=1, direction=1, pos_on_axis=y1, rectangles=[rect_top])

                    if i == 0:
                        rect_bottom = (z0, x0, z1, x1)
                        self._append_face_rectangles(triangles, axis=1, direction=0, pos_on_axis=y0, rectangles=[rect_bottom])

        return triangles

    def _greedy_mesh(self):
        """
        Generates an optimized mesh using greedy meshing algorithm.
        Merges adjacent coplanar faces into larger rectangles to reduce triangle count.

        Returns:
            list: A list of tuples, where each tuple is a triangle defined as
                (normal, vertex1, vertex2, vertex3).
        """
        if not self._voxels:
            return []

        logger.info(f"Generating optimized mesh using greedy meshing for {len(self._voxels)} voxels...")
        triangles = []

        # For each axis direction, collect exposed faces and merge them
        # Axes: 0=X, 1=Y, 2=Z; Directions: 0=negative, 1=positive
        for axis in range(3):  # X, Y, Z
            for direction in [0, 1]:  # negative, positive
                # Get all exposed faces for this direction
                faces = self._collect_faces_for_direction(axis, direction)

                # Group faces by their position along the normal axis (slices)
                slices = {}
                for face in faces:
                    slice_pos = face['pos_on_axis']
                    if slice_pos not in slices:
                        slices[slice_pos] = []
                    slices[slice_pos].append(face)

                # Apply greedy meshing to each slice
                for slice_pos, slice_faces in slices.items():
                    merged = self._greedy_merge_slice(slice_faces, axis)
                    triangles.extend(merged)

        logger.info(f"Greedy mesh generation complete. Optimized to {len(triangles)} triangles.")
        return triangles

    def _collect_faces_for_direction(self, axis, direction):
        """
        Collects all exposed faces for a given axis direction.

        Args:
            axis (int): 0=X, 1=Y, 2=Z
            direction (int): 0=negative face, 1=positive face

        Returns:
            list: List of face dictionaries with position and size information
        """
        faces = []
        offset = [0, 0, 0]
        offset[axis] = -1 if direction == 0 else 1

        for (gx, gy, gz), (size_x, size_y, size_z) in self._voxels.items():
            neighbor_coord = (gx + offset[0], gy + offset[1], gz + offset[2])
            neighbor_dims = self._voxels.get(neighbor_coord)

            # Dimensions are already stored in internal Y-up representation
            build_size_x, build_size_y, build_size_z = size_x, size_y, size_z
            grid_dim_x, grid_dim_y, grid_dim_z = self.voxel_dimensions
            if self._coordinate_system == 'z_up':
                grid_dim_y, grid_dim_z = grid_dim_z, grid_dim_y

            # Face is exposed if no neighbor or neighbor has different dimensions
            if not neighbor_dims or neighbor_dims != (size_x, size_y, size_z):
                # Calculate face position in world coordinates
                min_cx = gx * grid_dim_x
                min_cy = gy * grid_dim_y
                min_cz = gz * grid_dim_z

                # Position along the normal axis
                pos_on_axis = [min_cx, min_cy, min_cz][axis]
                if direction == 1:  # Positive face
                    pos_on_axis += [build_size_x, build_size_y, build_size_z][axis]

                # The two axes perpendicular to the normal
                u_axis = (axis + 1) % 3
                v_axis = (axis + 2) % 3

                u_pos = [min_cx, min_cy, min_cz][u_axis]
                v_pos = [min_cx, min_cy, min_cz][v_axis]
                u_size = [build_size_x, build_size_y, build_size_z][u_axis]
                v_size = [build_size_x, build_size_y, build_size_z][v_axis]

                faces.append({
                    'axis': axis,
                    'direction': direction,
                    'pos_on_axis': pos_on_axis,
                    'u_pos': u_pos,
                    'v_pos': v_pos,
                    'u_size': u_size,
                    'v_size': v_size,
                    'grid_coord': (gx, gy, gz),
                    'dimensions': (size_x, size_y, size_z)
                })

        return faces

    def _greedy_merge_slice(self, faces, axis):
        """
        Merges coplanar faces in a slice using greedy meshing algorithm.

        Args:
            faces (list): List of face dictionaries in the same slice
            axis (int): The normal axis (0=X, 1=Y, 2=Z)

        Returns:
            list: List of triangles for the merged faces
        """
        if not faces:
            return []

        triangles = []
        direction = faces[0]['direction']
        pos_on_axis = faces[0]['pos_on_axis']

        # Build a grid of faces by their u,v positions and sizes
        # Face positions are in internal Y-up space, so use swapped grid dims if needed
        grid_dims = list(self.voxel_dimensions)
        if self._coordinate_system == 'z_up':
            grid_dims[1], grid_dims[2] = grid_dims[2], grid_dims[1]

        face_grid = {}
        for face in faces:
            # Use grid coordinates for lookup (only works for uniform voxels)
            u_idx = int(round(face['u_pos'] / grid_dims[(axis + 1) % 3]))
            v_idx = int(round(face['v_pos'] / grid_dims[(axis + 2) % 3]))
            u_size = face['u_size']
            v_size = face['v_size']

            key = (u_idx, v_idx, u_size, v_size)
            face_grid[key] = face

        # Greedy meshing: merge adjacent faces with same dimensions
        used = set()
        sorted_faces = sorted(face_grid.items(), key=lambda x: (x[0][1], x[0][0]))  # Sort by v, then u

        for (u_idx, v_idx, u_size, v_size), face in sorted_faces:
            if (u_idx, v_idx) in used:
                continue

            # Try to extend in u direction
            u_end = u_idx
            while (u_end + 1, v_idx, u_size, v_size) in face_grid and (u_end + 1, v_idx) not in used:
                u_end += 1

            # Try to extend in v direction
            v_end = v_idx
            can_extend = True
            while can_extend:
                # Check if entire row exists for v_end + 1
                for u in range(u_idx, u_end + 1):
                    if (u, v_end + 1, u_size, v_size) not in face_grid or (u, v_end + 1) in used:
                        can_extend = False
                        break
                if can_extend:
                    v_end += 1

            # Mark all merged faces as used
            for v in range(v_idx, v_end + 1):
                for u in range(u_idx, u_end + 1):
                    used.add((u, v))

            # Create merged rectangle
            u_axis_idx = (axis + 1) % 3
            v_axis_idx = (axis + 2) % 3

            # Use the already-swapped grid_dims from above
            u_start = u_idx * grid_dims[u_axis_idx]
            v_start = v_idx * grid_dims[v_axis_idx]
            u_length = (u_end - u_idx + 1) * u_size
            v_length = (v_end - v_idx + 1) * v_size

            # Build vertices for the merged rectangle
            verts = self._build_rect_vertices(axis, direction, pos_on_axis,
                                              u_start, v_start, u_length, v_length)

            # Create normal
            normal = [0, 0, 0]
            normal[axis] = 1 if direction == 1 else -1
            normal = tuple(normal)

            # Swap Y/Z for Z-up mode
            if self._coordinate_system == 'z_up':
                verts = [(v[0], v[2], v[1]) for v in verts]
                normal = (normal[0], normal[2], normal[1])

            # Create triangles with proper winding
            if self._coordinate_system == 'z_up':
                triangles.append((normal, verts[0], verts[2], verts[1]))
                triangles.append((normal, verts[0], verts[3], verts[2]))
            else:
                triangles.append((normal, verts[0], verts[1], verts[2]))
                triangles.append((normal, verts[0], verts[2], verts[3]))

        return triangles

    def _build_rect_vertices(self, axis, direction, pos_on_axis, u_start, v_start, u_length, v_length):
        """
        Builds the 4 vertices of a rectangle for a given axis direction.

        Returns:
            list: List of 4 vertex tuples in counter-clockwise order
        """
        u_axis = (axis + 1) % 3
        v_axis = (axis + 2) % 3

        # Build 4 corners
        verts = []
        for v_offset in [0, v_length]:
            for u_offset in [0, u_length]:
                vert = [0, 0, 0]
                vert[axis] = pos_on_axis
                vert[u_axis] = u_start + u_offset
                vert[v_axis] = v_start + v_offset
                verts.append(tuple(vert))

        # Reorder for CCW winding based on axis and direction
        # Order: bottom-left, bottom-right, top-right, top-left
        if axis == 0:  # X axis (YZ plane)
            if direction == 0:  # -X face
                verts = [verts[0], verts[2], verts[3], verts[1]]
            else:  # +X face
                verts = [verts[0], verts[1], verts[3], verts[2]]
        elif axis == 1:  # Y axis (XZ plane)
            if direction == 0:  # -Y face (looking up from below)
                verts = [verts[0], verts[2], verts[3], verts[1]]
            else:  # +Y face (looking down from above)
                verts = [verts[0], verts[1], verts[3], verts[2]]
        else:  # Z axis (XY plane)
            if direction == 0:  # -Z face
                verts = [verts[0], verts[2], verts[3], verts[1]]
            else:  # +Z face
                verts = [verts[0], verts[1], verts[3], verts[2]]

        return verts

    def generate_mesh(self, optimize=True):
        """
        Generates a list of triangles representing the exposed faces of the voxels.

        Ensures consistent counter-clockwise winding order (right-hand rule)
        for outward-facing normals.

        Args:
            optimize (bool): If True, uses greedy meshing algorithm to merge adjacent
                           coplanar faces, significantly reducing triangle count.
                           Default: True (recommended for most use cases).

        Returns:
            list: A list of tuples, where each tuple is a triangle defined as
                (normal, vertex1, vertex2, vertex3). Coordinates are in
                the model's world space. Returns an empty list if no voxels
                have been added.
        """
        if not self._voxels:
            return []

        use_greedy = optimize and self._can_use_greedy_meshing()
        if use_greedy:
            return self._greedy_mesh()

        heightmap_triangles = self._heightmap_mesh(optimize=optimize)
        if heightmap_triangles is not None:
            if optimize:
                logger.warning("Using heightmap meshing for non-uniform voxel dimensions.")
            return heightmap_triangles

        if optimize:
            logger.warning("Greedy meshing disabled for non-uniform voxel dimensions; using partial adjacency meshing.")

        logger.info(f"Generating mesh for {len(self._voxels)} voxels...")
        triangles = []
        eps = 1e-9

        faces_data = [
            (0, 1, (1, 0, 0)),  # +X
            (0, 0, (-1, 0, 0)), # -X
            (1, 1, (0, 1, 0)),  # +Y
            (1, 0, (0, -1, 0)), # -Y
            (2, 1, (0, 0, 1)),  # +Z
            (2, 0, (0, 0, -1)), # -Z
        ]

        processed_faces = 0
        for grid_coord, voxel_dims in self._voxels.items():
            min_cx, min_cy, min_cz = self._voxel_min_corner(grid_coord)
            min_corner = (min_cx, min_cy, min_cz)
            size_x, size_y, size_z = voxel_dims
            sizes = (size_x, size_y, size_z)

            gx, gy, gz = grid_coord
            for axis, direction, offset in faces_data:
                neighbor_coord = (gx + offset[0], gy + offset[1], gz + offset[2])
                neighbor_dims = self._voxels.get(neighbor_coord)

                pos_on_axis = min_corner[axis] + (sizes[axis] if direction == 1 else 0)
                u_axis = (axis + 1) % 3
                v_axis = (axis + 2) % 3
                u_start = min_corner[u_axis]
                v_start = min_corner[v_axis]
                u_length = sizes[u_axis]
                v_length = sizes[v_axis]

                rectangles = [(u_start, v_start, u_start + u_length, v_start + v_length)]

                if neighbor_dims:
                    neighbor_min = self._voxel_min_corner(neighbor_coord)
                    neighbor_sizes = neighbor_dims
                    neighbor_plane = neighbor_min[axis] if direction == 1 else neighbor_min[axis] + neighbor_sizes[axis]

                    if abs(pos_on_axis - neighbor_plane) <= eps:
                        n_u_start = neighbor_min[u_axis]
                        n_v_start = neighbor_min[v_axis]
                        n_u_length = neighbor_sizes[u_axis]
                        n_v_length = neighbor_sizes[v_axis]

                        x0 = u_start
                        x1 = u_start + u_length
                        y0 = v_start
                        y1 = v_start + v_length
                        nx0 = n_u_start
                        nx1 = n_u_start + n_u_length
                        ny0 = n_v_start
                        ny1 = n_v_start + n_v_length

                        ix0 = max(x0, nx0)
                        ix1 = min(x1, nx1)
                        iy0 = max(y0, ny0)
                        iy1 = min(y1, ny1)

                        if ix1 > ix0 + eps and iy1 > iy0 + eps:
                            rectangles = []
                            if ix0 > x0 + eps:
                                rectangles.append((x0, y0, ix0, y1))
                            if ix1 < x1 - eps:
                                rectangles.append((ix1, y0, x1, y1))
                            if iy0 > y0 + eps:
                                rectangles.append((ix0, y0, ix1, iy0))
                            if iy1 < y1 - eps:
                                rectangles.append((ix0, iy1, ix1, y1))

                if rectangles:
                    processed_faces += len(rectangles)
                    self._append_face_rectangles(triangles, axis, direction, pos_on_axis, rectangles)

        logger.info(f"Mesh generation complete. Emitted {processed_faces} face segments, resulting in {len(triangles)} triangles.")
        return triangles

    def save_mesh(self, filename, format='stl_binary', optimize=True, **kwargs):
        """
        Generates the mesh and saves it to a file using the specified format.

        Args:
            filename (str): The path to the output file.
            format (str): The desired output format identifier (e.g/,
                        'stl_binary', 'stl_ascii'). Case-insensitive.
                        Defaults to 'stl_binary'.
            optimize (bool): If True, uses greedy meshing to reduce triangle count
                           by merging adjacent coplanar faces. Can reduce file size
                           by 10-100x for regular voxel structures. Default: True.
            **kwargs: Additional arguments passed directly to the specific
                    file writer (e.g., 'solid_name' for STL formats).
        """
        triangles = self.generate_mesh(optimize=optimize)
        if not triangles:
            logger.warning("No voxels in the model. Mesh file will not be generated.")
            return

        try:
            writer = get_writer(format)
            writer.write(triangles, filename, **kwargs)
            # No need for logger.info here, the writer handles its own success message
        except ValueError as e:
            logger.error(f"Failed to save mesh: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred during mesh saving to '{filename}': {e}")
            raise
