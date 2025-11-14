# examples/coordinate_systems.py

import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')

# Import from source directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cubeforge

# Define output directory
output_dir = os.path.dirname(__file__)
os.makedirs(output_dir, exist_ok=True)

print(f"Using cubeforge version: {cubeforge.__version__}")
print(f"Outputting STL files to: {output_dir}")

# --- Example 1: Vertical Tower in Y-up Mode (default) ---
print("\n--- Example 1: Vertical Tower in Y-up Mode ---")
print("Creating a vertical tower stacked along Y axis (Y is up)")

model_y_up = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))
# In Y-up mode, stack along Y to create vertical tower
model_y_up.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)
model_y_up.add_voxel(0, 1, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)
model_y_up.add_voxel(0, 2, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)
model_y_up.add_voxel(0, 3, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)

output_filename = os.path.join(output_dir, "tower_y_up.stl")
model_y_up.save_mesh(output_filename, format='stl_binary', solid_name="TowerYUp")
print(f"Saved '{output_filename}'")
print("NOTE: This will appear rotated 90° in most STL viewers (they expect Z-up)")

# --- Example 2: Vertical Tower in Z-up Mode ---
print("\n--- Example 2: Vertical Tower in Z-up Mode ---")
print("Creating a vertical tower stacked along Z axis (Z is up)")

model_z_up = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))
model_z_up.set_z_up()  # Switch to Z-up mode
# In Z-up mode, stack along Z to create vertical tower
model_z_up.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.CORNER_NEG)
model_z_up.add_voxel(0, 0, 1, anchor=cubeforge.CubeAnchor.CORNER_NEG)
model_z_up.add_voxel(0, 0, 2, anchor=cubeforge.CubeAnchor.CORNER_NEG)
model_z_up.add_voxel(0, 0, 3, anchor=cubeforge.CubeAnchor.CORNER_NEG)

output_filename = os.path.join(output_dir, "tower_z_up.stl")
model_z_up.save_mesh(output_filename, format='stl_binary', solid_name="TowerZUp")
print(f"Saved '{output_filename}'")
print("NOTE: This will appear correctly oriented in STL viewers!")

# --- Example 3: Using BOTTOM_CENTER and TOP_CENTER in Z-up Mode ---
print("\n--- Example 3: Using Anchors in Z-up Mode ---")
print("Demonstrating BOTTOM_CENTER and TOP_CENTER in Z-up (they refer to Z faces)")

model_anchors = cubeforge.VoxelModel(voxel_dimensions=(2.0, 2.0, 1.0))
model_anchors.set_z_up()  # Z is up

# Base block centered at origin on the bottom
model_anchors.add_voxel(0, 0, 0, anchor=cubeforge.CubeAnchor.BOTTOM_CENTER)
# Second block stacked on top, using BOTTOM_CENTER at z=1
model_anchors.add_voxel(0, 0, 1, anchor=cubeforge.CubeAnchor.BOTTOM_CENTER)
# Third block on top of that
model_anchors.add_voxel(0, 0, 2, anchor=cubeforge.CubeAnchor.BOTTOM_CENTER)

output_filename = os.path.join(output_dir, "anchors_z_up.stl")
model_anchors.save_mesh(output_filename, format='stl_binary', solid_name="AnchorsZUp")
print(f"Saved '{output_filename}'")

# --- Example 4: Custom Dimensions in Z-up Mode ---
print("\n--- Example 4: Custom Dimensions in Z-up Mode ---")
print("In Z-up mode, dimensions are (width, depth, height)")

model_custom = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))
model_custom.set_z_up()

# Create a base (wide and shallow)
model_custom.add_voxel(0, 0, 0,
                      anchor=cubeforge.CubeAnchor.CORNER_NEG,
                      dimensions=(3.0, 3.0, 0.5))  # width, depth, height

# Stack a narrow tall column on top
model_custom.add_voxel(1.5, 1.5, 0.5,
                      anchor=cubeforge.CubeAnchor.BOTTOM_CENTER,
                      dimensions=(1.0, 1.0, 3.0))  # width, depth, height

output_filename = os.path.join(output_dir, "custom_dims_z_up.stl")
model_custom.save_mesh(output_filename, format='stl_binary', solid_name="CustomDimsZUp")
print(f"Saved '{output_filename}'")

# --- Example 5: Comparison - Same coordinates, different modes ---
print("\n--- Example 5: Comparison ---")
print("Same coordinates (0,0,0), (1,0,0), (0,1,0) in both modes")

# Y-up mode
model_comp_y = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))
model_comp_y.add_voxels([(0, 0, 0), (1, 0, 0), (0, 1, 0)])
output_filename = os.path.join(output_dir, "comparison_y_up.stl")
model_comp_y.save_mesh(output_filename, format='stl_binary', solid_name="ComparisonYUp")
print(f"Saved '{output_filename}' (Y-up mode)")

# Z-up mode
model_comp_z = cubeforge.VoxelModel(voxel_dimensions=(1.0, 1.0, 1.0))
model_comp_z.set_z_up()
model_comp_z.add_voxels([(0, 0, 0), (1, 0, 0), (0, 1, 0)])
output_filename = os.path.join(output_dir, "comparison_z_up.stl")
model_comp_z.save_mesh(output_filename, format='stl_binary', solid_name="ComparisonZUp")
print(f"Saved '{output_filename}' (Z-up mode)")
print("Load both in an STL viewer to see the difference!")

print("\n" + "="*60)
print("All coordinate system examples completed!")
print("="*60)
print("\nSummary:")
print("- Y-up mode (default): Good for mathematical consistency, but")
print("  models appear rotated in most STL viewers")
print("- Z-up mode: Recommended for 3D printing! Models appear")
print("  correctly oriented in slicers like Cura, PrusaSlicer, etc.")
