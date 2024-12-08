import numpy as np
import open3d as o3d
import argparse
import os
from pathlib import Path

def bin_to_pcd(bin_path, pcd_path=None):
    """
    Convert KITTI format .bin point cloud to .pcd format
    
    Args:
        bin_path (str): Path to input .bin file
        pcd_path (str, optional): Path to output .pcd file. If None, will use same name as input
        
    Returns:
        str: Path to saved .pcd file
    """
    # Create output path if not specified
    if pcd_path is None:
        pcd_path = str(Path(bin_path).with_suffix('.pcd'))
    
    # Read binary point cloud data
    # KITTI format: x, y, z, intensity (float32)
    scan = np.fromfile(bin_path, dtype=np.float32)
    
    # Reshape to get points (N, 4) - x, y, z, intensity
    points = scan.reshape((-1, 4))
    
    # Create Open3D point cloud object
    pcd = o3d.geometry.PointCloud()
    
    # Set xyz coordinates
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])
    
    # If you want to keep intensity as colors, normalize and convert to RGB
    if points.shape[1] >= 4:
        # Normalize intensity to 0-1 range
        intensity = points[:, 3]
        intensity_normalized = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))
        
        # Convert to grayscale RGB
        colors = np.zeros((points.shape[0], 3))
        colors[:, :] = intensity_normalized.reshape(-1, 1)
        pcd.colors = o3d.utility.Vector3dVector(colors)
    
    # Save to PCD file
    o3d.io.write_point_cloud(pcd_path, pcd)
    return pcd_path

def process_directory(input_dir, output_dir=None):
    """
    Convert all .bin files in a directory to .pcd format
    
    Args:
        input_dir (str): Input directory containing .bin files
        output_dir (str, optional): Output directory for .pcd files
    """
    input_dir = Path(input_dir)
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    for bin_file in input_dir.glob('*.bin'):
        if output_dir:
            pcd_path = str(output_dir / bin_file.with_suffix('.pcd').name)
        else:
            pcd_path = None
        print(f"Converting {bin_file.name}...")
        bin_to_pcd(str(bin_file), pcd_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .bin point cloud files to .pcd format")
    parser.add_argument("input", help="Input .bin file or directory")
    parser.add_argument("--output", "-o", help="Output .pcd file or directory (optional)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if input_path.is_dir():
        process_directory(args.input, args.output)
    else:
        bin_to_pcd(args.input, args.output)
    
    print("Conversion completed!")