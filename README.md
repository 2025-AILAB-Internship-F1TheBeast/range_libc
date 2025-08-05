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

### Build & Install C++ Library
```bash
git clone <repo-url>
cd range_libc

# Clean build and system-wide installation
mkdir build && cd build

# With CUDA (if available)
cmake .. -DWITH_CUDA=ON
make -j$(nproc)
sudo make install
sudo ldconfig

# Without CUDA (recommended for most systems)
cmake .. -DWITH_CUDA=OFF
make -j$(nproc)
sudo make install
sudo ldconfig

# Test installation
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

### Using in Other CMake Projects
After system-wide installation, other projects can easily use RangeLibc:

```cmake
# In your CMakeLists.txt
find_package(range_libc REQUIRED)

# Link to your target
target_link_libraries(your_target range_libc::range_libc)

# Or fallback approach (if find_package doesn't work)
find_path(RANGELIBC_INCLUDE_DIR NAMES RangeLib.h PATHS /usr/local/include/range_libc)
find_library(RANGELIBC_LIBRARY NAMES range_libc PATHS /usr/local/lib)
target_include_directories(your_target PRIVATE ${RANGELIBC_INCLUDE_DIR})
target_link_libraries(your_target ${RANGELIBC_LIBRARY})
```

### Python Example
```python
import range_libc as rl

omap = rl.PyOMap(b"map.png", 1.0)
ray_caster = rl.PyRayMarching(omap, 500.0)
range_val = ray_caster.calc_range(x, y, theta)
```

## Build Results

### System-Wide Installation
After `sudo make install`:
- `/usr/local/lib/librange_libc.so` - C++ shared library
- `/usr/local/include/range_libc/` - Header files (RangeLib.h, etc.)
- `/usr/local/share/range_libc/cmake/` - CMake config files
- Other projects can find it with `find_package(range_libc)`

### Local Build
- `build/lib/librange_libc.so` - Local C++ shared library
- `build/bin/range_lib` - Test executable  
- `pywrapper_ros2/range_libc.cpython-*.so` - Python module

## Algorithms

- **Bresenham's Line (BL)**: Classic pixel-by-pixel ray tracing
- **Ray Marching (RM)**: Distance transform-based stepping  
- **CDDT/PCDDT**: Compressed lookup tables for near-constant time
- **Giant LUT (GLT)**: Precomputed table for all poses

Performance: Ray Marching ~3x faster than Bresenham, CDDT near-constant time.

## Python 3 Updates & System Integration

### ✅ Completed Updates:
- **Python 2 → 3 Migration**: All code updated (`print()`, `range()`, `map()`, etc.)
- **String Encoding**: Fixed file paths with proper bytes encoding (`b"path"`)
- **Modern Timing**: Updated to `time.perf_counter()` for better performance measurement
- **Build Scripts**: All compile scripts now use `python3`
- **System Installation**: Added proper CMake config files for system-wide installation
- **Dual Build Support**: Both ROS2 colcon and direct CMake builds work
- **Cross-Platform**: Works with and without CUDA, conditional compilation

### ⚙️ Build System Improvements:
- **Conditional CUDA**: Only enables CUDA language support when needed
- **Modern CMake**: Creates proper `range_libc::range_libc` targets
- **Dual Installation**: Both `/usr/local/lib/cmake/` and `/usr/local/share/range_libc/cmake/`
- **Automatic Discovery**: Other projects can find it with `find_package(range_libc)`

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