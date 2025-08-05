# RangeLibc - Fast 2D Ray Casting

High-performance 2D ray casting library with CUDA acceleration for robotics applications. Provides multiple optimized algorithms including the Compressed Directional Distance Transform (CDDT).

## Features

- 🚀 **Fast Ray Casting**: Multiple algorithms (Bresenham, Ray Marching, CDDT, Giant LUT)
- ⚡ **CUDA Acceleration**: GPU support for batch operations
- 🐍 **Python 3 & C++**: Modern Python bindings and C++ library
- 🤖 **ROS2 Compatible**: Works with ROS2 packages and nodes
- 🔧 **Flexible Build**: CMake, Python setup, or ROS2 colcon

## Quick Start

### Prerequisites
```bash
sudo apt install python3-dev python3-numpy cython3 build-essential cmake
```

### Build C++ Library
```bash
git clone <repo-url>
cd range_libc

# With CUDA (if available)
mkdir build && cd build && cmake .. -DWITH_CUDA=ON && make -j$(nproc)

# Without CUDA
mkdir build && cd build && cmake .. -DWITH_CUDA=OFF && make -j$(nproc)

# Test
./bin/range_lib --method=RayMarching --map_path=../maps/small.map.png
```

### Build Python Bindings
```bash
cd pywrapper_ros2

# With CUDA
./compile_with_cuda.sh

# Without CUDA  
./compile.sh

# Test
python3 -c "import range_libc; print('Success!')"
```

### ROS2 Integration
```bash
# In ROS2 workspace
cd ~/ros2_ws/src
git clone <repo-url>
cd ~/ros2_ws

# Build
colcon build --packages-select range_libc --cmake-args -DWITH_CUDA=OFF
source install/setup.bash
```

## Usage

### C++ Example
```cpp
#include <range_libc/RangeLib.h>

ranges::OMap omap("map.png", 1.0);
ranges::RayMarching ray_caster(omap, 500.0);
float range = ray_caster.calc_range(x, y, theta);
```

### Python Example
```python
import range_libc as rl

omap = rl.PyOMap(b"map.png", 1.0)
ray_caster = rl.PyRayMarching(omap, 500.0)
range_val = ray_caster.calc_range(x, y, theta)
```

## Build Results

After building you'll have:
- `build/lib/librange_libc.so` - C++ shared library
- `build/bin/range_lib` - Test executable  
- `pywrapper_ros2/range_libc.cpython-*.so` - Python module

## Algorithms

- **Bresenham's Line (BL)**: Classic pixel-by-pixel ray tracing
- **Ray Marching (RM)**: Distance transform-based stepping  
- **CDDT/PCDDT**: Compressed lookup tables for near-constant time
- **Giant LUT (GLT)**: Precomputed table for all poses

Performance: Ray Marching ~3x faster than Bresenham, CDDT near-constant time.

## Python 3 Updates

All Python code updated from Python 2:
- `print()` functions, `range()` instead of `xrange()`
- Fixed string encoding for file paths (`b"path"`)
- Modern timing with `time.perf_counter()`
- Updated compile scripts to use `python3`

## Citation

```bibtex
@article{walsh17,
    author = {Corey Walsh and Sertac Karaman},
    title  = {CDDT: Fast Approximate 2D Ray Casting for Accelerated Localization},
    url    = {http://arxiv.org/abs/1705.01167},
    year   = {2017}
}
```

## License

Apache 2.0 - Copyright 2017 Corey H. Walsh