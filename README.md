# Point Cloud Converter (.bin to .pcd)

A Python tool to convert point cloud data from binary (.bin) format to PCD format. This is particularly useful when working with KITTI dataset or similar LiDAR point cloud data.

## Features

- Convert single .bin file to .pcd format
- Batch convert all .bin files in a directory
- Preserves intensity information as color in the PCD file
- Simple command-line interface

## Requirements

```bash
numpy
open3d
```

Install requirements using:
```bash
pip install numpy open3d
```

## Usage

### Convert a single file:
```bash
python bin_to_pcd.py input.bin
# or specify output path
python bin_to_pcd.py input.bin -o output.pcd
```

### Convert all files in a directory:
```bash
python bin_to_pcd.py input_directory/
# or specify output directory
python bin_to_pcd.py input_directory/ -o output_directory/
```

## Notes

- The script assumes KITTI format point cloud data where each point is stored as 4 float32 values: x, y, z, intensity
- Intensity values are normalized and stored as colors in the PCD file
- Output PCD files can be viewed with tools like CloudCompare or using Open3D

## License

MIT License