# examples/create_shapes.py

import logging # Import the logging library
import random # Import the random library

# --- Configure Logging for this script ---
# This setup will affect all loggers used by the cubeforge library
# when called from this script.
log_level = logging.INFO # Set desired level: DEBUG, INFO, WARNING, ERROR, CRITICAL
log_format = '%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
logging.basicConfig(level=log_level, format=log_format)
# -----------------------------------------


# import directly from the source directory.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cubeforge

# Define output directory relative to this script
output_dir = os.path.dirname(__file__)
os.makedirs(output_dir, exist_ok=True) # Ensure the directory exists

# Now that logging is configured, this message will appear
logging.info(f"Using cubeforge version: {cubeforge.__version__}")
logging.info(f"Outputting STL files to: {output_dir}")

# --- Example 1: Simple L-Shape (Binary STL, Cubic Voxels) ---
print("\n--- Creating Example 1: L-Shape (Binary STL, Cubic Voxels) ---")
# Use voxel_dimensions instead of cube_size
model1 = cubeforge.VoxelModel(voxel_dimensions=(10.0, 10.0, 10.0))
# Coordinates now relate to the voxel dimensions
model1.add_voxels([
    (0, 0, 0), (10, 0, 0), (20, 0, 0), (20, 10, 0), (20, 20, 0)
], anchor=cubeforge.CubeAnchor.CORNER_NEG)

output_filename1 = os.path.join(output_dir, "l_shape_binary.stl") # Use output_dir
model1.save_mesh(output_filename1, format='stl_binary', solid_name="LShapeBinary")
print(f"Saved '{output_filename1}'")


# --- Example 2: Single Cube (ASCII STL, Cubic Voxel) ---
print("\n--- Creating Example 2: Single Cube (ASCII STL, Cubic Voxel) ---")
model2 = cubeforge.VoxelModel(voxel_dimensions=(5.0, 5.0, 5.0))
model2.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CENTER)

output_filename2 = os.path.join(output_dir, "center_cube_ascii.stl") # Use output_dir
model2.save_mesh(output_filename2, format='stl_ascii', solid_name="CenterCubeASCII")
print(f"Saved '{output_filename2}'")


# --- Example 3: Anchor Demonstration (Binary STL, Cubic Voxels) ---
print("\n--- Creating Example 3: Anchor Demonstration (Binary STL, Cubic Voxels) ---")
model3 = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))
model3.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)
model3.add_voxel(2.5, 0.5, 0.5, anchor=cubeforge.CubeAnchor.CENTER) # Center of 1x1x1 is (0.5, 0.5, 0.5) from corner
model3.add_voxel(5, 1, 1, anchor=cubeforge.CubeAnchor.CORNER_POS) # Corner pos of 1x1x1 is (1,1,1) from corner
model3.add_voxel(7, 0, 0.5, anchor=cubeforge.CubeAnchor.BOTTOM_CENTER) # Bottom center of 1x1x1 is (0.5, 0, 0.5) from corner
model3.add_voxel(9.5, 1, 0.5, anchor=cubeforge.CubeAnchor.TOP_CENTER) # Top center of 1x1x1 is (0.5, 1, 0.5) from corner

output_filename3 = os.path.join(output_dir, "anchor_demo_binary.stl") # Use output_dir
model3.save_mesh(output_filename3, solid_name="AnchorDemoBinary")
print(f"Saved '{output_filename3}'")


# --- Example 4: Non-Uniform Voxel Shape (Binary STL) ---
print("\n--- Creating Example 4: Non-Uniform Voxel Shape (Binary STL) ---")
# Define non-uniform dimensions (width=2, height=1, depth=3)
model4 = cubeforge.VoxelModel(voxel_dimensions=(2.0, 1.0, 3.0))
# Add a few voxels using corner anchor
model4.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG) # Voxel from (0,0,0) to (2,1,3)
model4.add_voxel(2, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG) # Voxel from (2,0,0) to (4,1,3)
model4.add_voxel(0, 1, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG) # Voxel from (0,1,0) to (2,2,3)

output_filename4 = os.path.join(output_dir, "non_uniform_voxels.stl") # Use output_dir
model4.save_mesh(output_filename4, format='stl_binary', solid_name="NonUniformVoxels")
print(f"Saved '{output_filename4}'")


# --- Example 5: Trying an unsupported format (will raise error) ---
print("\n--- Creating Example 5: Unsupported Format (Expect Error) ---")
model5 = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0)) # Use new init
model5.add_voxel(0,0,0) # Use new method name
try:
    # Use output_dir for the test file as well
    model5.save_mesh(os.path.join(output_dir, "test.obj"), format='obj')
except ValueError as e:
    # This error message will now be logged because basicConfig was called
    logging.error(f"Caught expected error during unsupported format test: {e}")
    print(f"Caught expected error: {e}") # Also print to console
except Exception as e:
    logging.exception(f"Caught unexpected error during unsupported format test: {e}") # Log traceback
    print(f"Caught unexpected error: {e}")


# --- Example 6: Random Height Surface (Binary STL) ---
print("\n--- Creating Example 6: Random Height Surface (Binary STL) ---")
grid_size_x = 32
grid_size_z = 32
min_height = 1 # Minimum number of voxels vertically
max_additional_height = 5 # Max random voxels to add on top
voxel_dim = (1.0, 1.0, 1.0) # Use 1x1x1 voxels for stacking

model6 = cubeforge.VoxelModel(voxel_dimensions=voxel_dim)

for x in range(grid_size_x):
    for z in range(grid_size_z):
        total_height = min_height + random.random() * max_additional_height
        # Add voxel using corner anchor. Coordinates are direct due to 1x1x1 dimension.
        model6.add_voxel(x * voxel_dim[0],
                         0,
                         z * voxel_dim[2],
                         dimensions=(voxel_dim[0], total_height, voxel_dim[2]),
                         anchor=cubeforge.CubeAnchor.CORNER_NEG)

output_filename6 = os.path.join(output_dir, "random_height_surface.stl") # Use output_dir
model6.save_mesh(output_filename6, format='stl_binary', solid_name="RandomHeightSurface")
print(f"Saved '{output_filename6}'")


print("\nAll examples finished.")
