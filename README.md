# RangeLibc - ROS2 Compatible with CUDA Acceleration

This library provides different implementations of 2D raycasting for 2D occupancy grids, including the Compressed Directional Distance Transform (CDDT) algorithm as proposed in [this publication](http://arxiv.org/abs/1705.01167). The code is written and optimized in C++, with Python wrappers provided for ROS2 compatibility.

## ✨ Features

- 🚀 **ROS2 Compatible**: Full integration with ROS2 Humble and later versions
- ⚡ **Fast 2D Ray Casting**: Multiple optimized algorithms including CDDT
- 🐍 **Dual Language Support**: Both C++ and Python APIs for ROS2 nodes
- 🎯 **CUDA Acceleration**: GPU-accelerated ray casting for Jetson platforms
- 🔧 **Flexible Usage**: Standalone, C++ ROS2 nodes, or Python ROS2 nodes
- 🏗️ **Modern Build System**: Uses colcon build with proper CMake integration
- 📦 **Easy Installation**: Single command builds everything including Python bindings
- 🧪 **Tested**: Verified on NVIDIA Jetson Orin with CUDA 12.6

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
sudo apt update
sudo apt install python3-dev python3-numpy python3-setuptools cython3
```

### ROS2 Package Build (Recommended)

This builds everything in one command - C++ library, Python bindings, and CUDA support:

```bash
# Place in your ROS2 workspace
cd ~/your_ros2_ws/src
git clone https://github.com/your-repo/range_libc
cd ~/your_ros2_ws

# Build with CUDA support (if available)
export CUDACXX=/usr/local/cuda/bin/nvcc  # or your CUDA path
colcon build --packages-select range_libc

# Build without CUDA (for systems without NVIDIA GPU)
colcon build --packages-select range_libc --cmake-args -DWITH_CUDA=OFF

# Source the workspace
source install/setup.bash
```

**That's it!** 🎉 Both C++ library and Python bindings with CUDA support are now ready to use.

## 📖 Usage Examples

### C++ ROS2 Node

```cpp
// In your ROS2 package's CMakeLists.txt
find_package(range_libc REQUIRED)
target_link_libraries(your_node range_libc::range_libc)
```

```cpp
// In your C++ ROS2 node
#include <range_libc/RangeLib.h>

// Create map and ray caster
ranges::OMap omap("map.png", 1.0);
ranges::RayMarching ray_caster(omap, 500.0);  // GPU-accelerated if available

// Cast a ray
float range = ray_caster.calc_range(x, y, theta);
```

### Python ROS2 Node

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import pywrapper_ros2.range_libc as rl

class RaycastingNode(Node):
    def __init__(self):
        super().__init__('raycasting_node')
        
        # Load map and create GPU-accelerated ray caster
        self.omap = rl.PyOMap(b"map.png", 1.0)
        self.ray_caster = rl.PyRayMarching(self.omap, 500.0)
        
    def cast_rays(self, x, y, theta):
        # Fast GPU-accelerated ray casting
        return self.ray_caster.calc_range(x, y, theta)
```

### Standalone Testing

```bash
# Test C++ CUDA executable
./build/range_libc/bin/range_lib --method=RayMarching --map_path=maps/small.map.png

# Test Python CUDA bindings
cd pywrapper_ros2
python3 test.py
```

## ⚙️ Build Options

### CUDA Support

CUDA acceleration is **automatically enabled** if CUDA is detected during build. For manual control:

```bash
# Force enable CUDA
export CUDACXX=/usr/local/cuda/bin/nvcc
colcon build --packages-select range_libc

# Build without CUDA (for systems without NVIDIA GPU)
colcon build --packages-select range_libc --cmake-args -DWITH_CUDA=OFF
```

### Standalone C++ Build

```bash
git clone https://github.com/your-repo/range_libc
cd range_libc
mkdir build && cd build
cmake -DWITH_CUDA=ON ..  # Enable CUDA
make
```

### Python Bindings Only

```bash
cd range_libc/pywrapper_ros2
# With CUDA
WITH_CUDA=ON python3 setup.py build_ext --inplace
# Without CUDA  
python3 setup.py build_ext --inplace
```

## 🤖 Platform Support

### NVIDIA Jetson (Orin, Xavier, TX2, TX1)

Optimized for NVIDIA Jetson platforms with automatic CUDA architecture detection:

```bash
# Jetson setup (works on all Jetson platforms)
cd ~/your_ros2_ws/src
git clone https://github.com/your-repo/range_libc
cd ~/your_ros2_ws

# Build automatically detects Jetson GPU architecture
export CUDACXX=/usr/local/cuda/bin/nvcc
colcon build --packages-select range_libc
```

**Supported Architectures:**
- Jetson Orin: `sm_87` (tested)
- Jetson Xavier: `sm_72` 
- Jetson TX2: `sm_62`
- Jetson TX1: `sm_53`

### x86_64 with NVIDIA GPU

```bash
# Desktop/Server with NVIDIA GPU
export CUDACXX=/usr/local/cuda/bin/nvcc
colcon build --packages-select range_libc --cmake-args -DCUDA_ARCHITECTURES="75;86" # Adjust for your GPU
```

## 🧪 Testing & Validation

Run the comprehensive test suite to verify your installation:

```bash
# Run integration tests (from range_libc directory)
python3 test_integration.py
```

Expected output:
```
🎉 SUCCESS: All tests passed!
✓ C++ CUDA library works in ROS2
✓ Python CUDA bindings work in ROS2
✓ Ready for both C++ and Python ROS2 nodes with GPU acceleration!
```

## 🔧 Troubleshooting

### Common Issues

**CUDA not found:**
```bash
# Make sure CUDA path is correct
export CUDACXX=/usr/local/cuda-12.6/bin/nvcc  # Adjust version
```

**Permission errors during build:**
```bash
# Clean build directory
rm -rf build/ install/ log/
colcon build --packages-select range_libc
```

**Python import errors:**
```bash
# Source ROS2 workspace
source install/setup.bash
# Or add to Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)/install/range_libc/local/lib/python3.10/dist-packages
```

## 📄 License

This code is licensed under Apache 2.0. Copyright 2017 Corey H. Walsh. 

You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0

## 🎯 Performance

RangeLibc provides significant performance improvements over standard ray casting:

- **CPU Ray Marching**: ~10x faster than Bresenham's line
- **GPU Ray Marching**: ~100x faster for batch operations
- **CDDT Algorithm**: Near constant-time performance regardless of map size

![Range Method Performance Comparison](./media/comparison.png)

## 🚀 What's New in ROS2 Version

- ✅ **Full ROS2 Integration**: Native colcon build support
- ✅ **Dual Language APIs**: Both C++ and Python work seamlessly  
- ✅ **CUDA Acceleration**: GPU support for Jetson and desktop
- ✅ **Modern CMake**: Proper target exports and dependency management
- ✅ **Easy Installation**: Single command builds everything
- ✅ **Comprehensive Testing**: Automated validation of all features

## 📁 Project Structure

```
range_libc/
├── 🏗️ Build & Config
│   ├── CMakeLists.txt          # Modern CMake with ROS2 integration
│   ├── package.xml             # ROS2 package manifest
│   └── test_integration.py     # Comprehensive test suite
├── 🔧 Core Library  
│   ├── includes/
│   │   ├── RangeLib.h         # Main RangeLib source code
│   │   ├── CudaRangeLib.h     # CUDA function headers
│   │   ├── kernels.cu         # CUDA kernels for GPU acceleration
│   │   ├── RangeUtils.h       # Utility functions
│   │   └── lru_cache.h        # LRU cache implementation
│   ├── main.cpp               # Standalone C++ example & benchmarks
│   └── vendor/                # Third-party dependencies
│       ├── gflags/           # Google flags library
│       ├── lodepng/          # PNG loading/saving
│       └── distance_transform.h
├── 🐍 Python Integration
│   └── pywrapper_ros2/        # ROS2-compatible Python bindings
│       ├── RangeLibc.pyx      # Cython wrapper
│       ├── setup.py           # Python build configuration
│       ├── __init__.py        # Python package init
│       └── test.py            # Python usage examples
├── 🗺️ Test Data
│   └── maps/                  # Example PNG maps for testing
│       ├── small.map.png
│       ├── basement_fixed.png
│       └── [various test maps]
├── 📊 Performance
│   ├── make_plots.py          # Benchmark visualization
│   └── media/                 # Performance comparison charts
└── 🚀 ROS2 Artifacts (generated by colcon build)
    ├── build/                 # Build artifacts
    ├── install/               # Installed C++ library & Python packages
    └── log/                   # Build logs
```

## Cite

This library accompanies the following [publication](http://arxiv.org/abs/1705.01167).

    @article{walsh17,
        author = {Corey Walsh and 
                  Sertac Karaman},
        title  = {CDDT: Fast Approximate 2D Ray Casting for Accelerated Localization},
        volume = {abs/1705.01167},
        url    = {http://arxiv.org/abs/1705.01167},
        year   = {2017}}

## Code structure

```
range_libc_dist/
├── build
│   └── bin          # this is where compiled binaries will be placed
├── CMakeLists.txt   # compilation rules - includes, etc
├── includes
│   ├── lru_cache.h  # implementation of LRU_cache, optionally used
│   ├── RangeLib.h   # main RangeLib source code
│   ├── CudaRangeLib.h # cuda function header file
│   ├── kernels.cu   # cuda kernels for super fast 2D ray casting
│   └── RangeUtils.h # various utility functions
├── license.txt
├── main.cpp         # example c++ usage and simple benchmarks
├── make_plots.py    # turns fine-grained benchmark information into violin plots
├── tmp/             # make this directory for saving fine-grained timing information
├── maps             # example PNG maps
│   └── [various .png files]
├── pywrapper
│   ├── RangeLibc.pyx # wrapper file for using RangeLib from Python
│   ├── setup.py     # compilation rules for Cython
│   └── test.py      # example Python usage
├── README.md
└── vendor           # various dependencies, see in here for licenses
    ├── distance_transform.h # for computing euclidean distance transform
    ├── gflags       # command line flag library from Google
    └── lodepng      # simple PNG loading/saving library
```

## RangeLibc Algorithms Overview

  * [Bresenham's Line (BL)](#bresenhams-line-bl)
  * [Ray Marching (RM/RMGPU)](#ray-marching-rm)
  * [Compressed Directional Distance Transform (CDDT/PCDDT)](#compressed-directional-distance-transform-cddt-ours)
  * [Giant Lookup Table (GLT)](#giant-lookup-table-glt)

![Range Method Performance Comparison](./media/comparison.png)

The above benchmarks were performed on an NVIDIA Jetson TX1 with a single thread. For a better treatment, see the paper associated with this library: [http://arxiv.org/abs/1705.01167](http://arxiv.org/abs/1705.01167)

<!--- ///////////////////////////// Bresenham's Line Description ////////////////////////////// -->

### Bresenham's Line (BL)

Bresenham's line algorithm [1] is one of the most widely used methods for two dimensional ray casting in occupancy grids. The algorithm incrementally determines the set of pixels that approximate the trajectory of a query ray starting from the query point (x,y)_{query} and progressing in the theta_{query} direction one pixel at a time. The algorithm terminates once the nearest occupied pixel is discovered, and the euclidean distance between that occupied pixel and (x,y)_{query} is reported. This algorithm is widely implemented in particle filters due to its simplicity and ability to operate on a dynamic map. The primary disadvantage is that it is slow, potentially requiring hundreds of memory accesses for a single ray cast. While average performance is highly environment dependent, Bresenham's Line algorithm is linear in map size in the worst case.

<!--- /////////////////////////////// Ray Marching Description //////////////////////////////// -->
### Ray Marching (RM/RMGPU)

Ray marching [2] is a well known algorithm, frequently used to accelerate fractal or volumetric graphical rendering applications. The basic idea can be understood very intuitively. Imagine that you are in an unknown environment, with a blindfold on. If an oracle tells you the distance to the nearest obstacle, you can surely move in any direction by at most that distance without colliding with any obstacle. By applying this concept recursively, one can step along a particular ray by the minimum distance to the nearest obstacle until colliding with some obstacle. The following figure demonstrates this idea graphically (from [3]).

![Ray Marching](./media/spheretrace.jpg)

In the occupancy grid world, it is possible to precompute the distance to the nearest obstacle for every discrete state in the grid via the euclidean distance transform.

This method is implemented both for the CPU and GPU in RangeLibc. The GPU implementation is the fastest available method for large batches of queries.

#### Pseudocode:

```
# compute the distance transform of the map
def precomputation(omap):
	distance_transform = euclidean_dt(omap)

# step along the (x,y,theta) ray until colliding with an obstacle
def calc_range(x,y,theta):
	t = 0.0
	coeff = 0.99
	while t < max_range:
		px, py = x + cos(theta) * t, y + sin(theta) * t

		if px or py out of map bounds:
			return max_range

		dist = distance_transform[px,py]
		if dist == 0.0:
			return sqrt((x - px)^2 + (y - py)^2)

		t += max(dist*coeff, 1.0)

```

#### Analysis

Precomputation: O(|theta_discretization|\*|edge pixels in occupancy grid|+|theta_discretization|\*|occupied pixels|\*log(|occupied pixels|))
Pruning: O(|map width|\*|map height|\*|theta_discretization|\*log(min(|occupied pixels|, longest map dimension)))
Calc range: O(log(min(|occupied pixels|, longest map dimension)))
Memory: O(|theta_discretization|\*|edge pixels|) - in practice much smaller, due to pruning

**Pros**

- Fast calc_range on average
- Space efficent
- Easy to implement, and easy to implement on a GPU
- Fairly fast to compute distance transform
- Extends easily to 3D

**Cons**

- Poor worst case performance - degenerate case similar to Bresenham's line
- High degree of control flow divergence (for parallelization)
- Not great for incrementally changing the map

<!--- /////////////////////////////////// CDDT Description //////////////////////////////////// -->

### Compressed Directional Distance Transform (CDDT/PCDDT) (ours)

The Compressed Directional Distance Transform (CDDT) algorithm uses a compressed data structure to represent map geometry in a way which allows for fast queries. An optional pruning step removes unneeded elements in the data structure for slightly faster operation (PCDDT). For a full description of the algorithm, see the associated paper: [http://arxiv.org/abs/1705.01167](http://arxiv.org/abs/1705.01167)

#### Pseudocode:

```
# for the given theta, determine a translation that will ensure the 
# y coordinate of every pixel in the rotated map will be positive
def y_offset(theta):
	pass

# give the range of y coordinates that the pixel overlaps with
def y_bounds(pixel):
	return range(min(pixel.corners.y), max(pixel.corners.y))

# build the CDDT datastructure
def precomputation(omap):
	# prune any unimportant geometry from the map
	edgeMap = morphological_edge_transform(omap)

	# build the empty LUT data structure
	compressed_lut = []
	for each theta in |theta_discretization|:
		projection_lut = []
		for each i in range(lut_widths[theta]):
			projection_lut.append([])
		compressed_lut.append(projection_lut)

	# populate the LUT data structure
	for each theta in |theta_discretization|:
		for each occupied pixel (x,y) in omap:
			pixel.rotate(theta)
			pixel.translate(y_offset(theta))
			lut_indices = y_bounds(pixel)
			
			for each index in lut_indices:
				compressed_lut[theta][index].append(pixel.center.x)

	# sort each LUT bin for faster access via binary search
	for each theta in |theta_discretization|:
		for each i in compressed_lut[theta].size():
			sort(compressed_lut[theta][i])

# (optional) remove unused entries from the LUT to save space
# highly recommended for static maps
def prune():
	# build an empty table of sets to keep track of which
	# indices in the CDDT data structure are used
	collision_table = []
	for theta in range(theta_discretization):
		collision_row = []
		for i in range(compressed_lut[theta].size()):
			collision_row.append(set())
		collision_table.append(collision_row)

	# ray cast from every possible (x,y,theta) state, keeping track
	# of which LUT entries are used
	for x in range(omap.width):
		for y in range(omap.height):
			for theta in range(theta_discretization):
				# keep track of which object in the LUT is found to collide
				# with the following ray cast query
				calc_range(x,y,theta) implies (lut_bin, lut_bin_index)
				collision_table[theta][lut_bin].add(lut_bin_index)

	# remove any element of the LUT that is not in the collision table
	for theta in range(theta_discretization):
		for i in range(compressed_lut[theta].size()):
			new_lut_bin = []
			for obstacle in compressed_lut[theta][i]:
				if obstacle in collision_table:
					new_lut_bin.append(obstacle)
				else: continue
			compressed_lut[theta][i] = new_lut_bin

# compute the distance to the nearest obstacle in the (x,y,theta) direction
def calc_range(x,y,theta):
	angle_index, discrete_angle, flipped_search = discretize_theta(theta)
	lut_x, lut_y = rotate(x, y, discrete_angle)

	if omap.occupied(x,y):
		return 0.0

	lut_bin = compressed_lut[angle_index][(int)lut_y]
	if flipped_search:
		nearest_obstacle_x = lut_bin.next_lesser_element(lut_x)
	else:
		nearest_obstacle_x = lut_bin.next_greater_element(lut_x)
	
	distance = abs(nearest_obstacle_x - lut_x)
	return distance
```

#### Analysis

Precomputation: O(|width|\*|height|) for 2D grid. In general O(dk) where d is the dimensionality of the grid, and k is the number of grid locations.
Calc range: worst case O(|longest map dimension|), on average much faster (close to logarithmic performance in scene size)
Memory: O(|width|\*|height|) for 2D grid. In general O(k) where k is the number of grid locations.

**Pros**

- Fast calc_range, in practice nearly constant time
- Radial symmetry optimizations can provide additional speed in the right context
- Potential for online incremental compressed LUT modification for use in SLAM (would need to store additional metadata)
- Space efficent
- Fast construction time

**Cons**

- Slow pruning time (optional)
- Approximate due to the discrete theta space
- Can be difficult to implement well
- Curse of dimensionality in higher dimensions


<!--- //////////////////////////////////// LUT Description //////////////////////////////////// -->

### Giant Lookup Table (GLT)

Precompute distances for all possible (x,y,theta) states and store the results in a big table for fast lookup.

#### Pseudocode:

```
# For every (x,y,theta) in a predefined grid, use Besenham's line or 
# ray maching to build the table
def precomputation(omap):
	giant_LUT[width][height][theta_discretization] = -1
	for x in range(omap.width):
		for y in range(omap.height):
			for theta in range(theta_discretization):
				giant_LUT[x][y][theta] = calc_range(x,y,theta)

# simply read from the table
# note: interpolation between the two closest discrete 
#       thetas would be more accurate but slower
def calc_range(x,y,theta):
	return giant_LUT[int(x), int(y), discrete(theta)]
```

#### Analysis

Precomputation: O(|theta_discretization|\*|width|\*|height|\*O(calc_range))
Memory: O(|theta_discretization|\*|width|\*|height|)
Calc range: O(1)

**Pros**

- Very fast calc_range
- Easy to implement

**Cons**

- Very slow construction time
- Approximate due to the discrete theta space
- Very large memory requirement
- Curse of dimensionality in higher dimensions


## References

1.  J. Bresenham. "Algorithm for Computer Control of a Digital Plotter," IBM Systems Journal, vol. 4, no. 1, pp. 25-30, 1965.
2.  K. Perlin and E. M. Hoffert. "Hypertexture," Computer Graphics, vol 23, no. 3, pp. 297-306, 1989.
3. M. Pharr, and R. Fernando. "Chapter 8. Per-Pixel Displacement Mapping with Distance Functions" in GPU gems 2: Programming techniques for high-performance graphics and general-purpose computation, 3rd ed. United States: Addison-Wesley Educational Publishers, 2005.
