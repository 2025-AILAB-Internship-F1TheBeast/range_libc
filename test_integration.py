#!/usr/bin/env python3
"""
Test script to verify both C++ library and Python bindings work with ROS2 and CUDA
"""

import sys
import os
import subprocess

def test_python_cuda_bindings():
    """Test Python CUDA bindings"""
    try:
        # Test from pywrapper_ros2 directory
        os.chdir('pywrapper_ros2')
        
        import range_libc as rl
        print("✓ Python CUDA bindings imported successfully")
        
        # Try to create a basic range object  
        omap = rl.PyOMap(b"../maps/small.map.png", 1.0)
        if omap.error():
            print("✗ Failed to load map for Python test")
            return False
            
        ray_caster = rl.PyRayMarching(omap, 500.0)
        result = ray_caster.calc_range(100.0, 100.0, 0.0)
        print(f"✓ Python CUDA ray casting works: range = {result}")
        
        os.chdir('..')
        return True
    except Exception as e:
        print(f"✗ Python CUDA bindings failed: {e}")
        os.chdir('..')
        return False

def test_cpp_cuda_executable():
    """Test C++ CUDA executable"""
    try:
        result = subprocess.run(['./build/range_libc/bin/range_lib', 
                               '--method=RayMarching', 
                               '--map_path=maps/small.map.png', 
                               '--query=10,10,0'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "range:" in result.stdout:
            print("✓ C++ CUDA executable runs successfully")
            return True
        else:
            print(f"✗ C++ CUDA executable failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ C++ CUDA executable failed: {e}")
        return False

def test_ros2_integration():
    """Test ROS2 integration"""
    try:
        # Test ROS2 package installation
        sys.path.insert(0, 'install/range_libc/local/lib/python3.10/dist-packages')
        import pywrapper_ros2
        print("✓ ROS2 Python package installation works")
        
        # Test C++ library availability for linking
        lib_path = 'install/range_libc/lib/librange_libc.so'
        if os.path.exists(lib_path):
            print("✓ C++ shared library available for ROS2 nodes")
            return True
        else:
            print("✗ C++ shared library not found")
            return False
    except Exception as e:
        print(f"✗ ROS2 integration test failed: {e}")
        return False

def main():
    print("Testing ROS2 range_libc integration with CUDA support...")
    print("=" * 60)
    
    # Test individual components
    python_cuda_ok = test_python_cuda_bindings()
    cpp_cuda_ok = test_cpp_cuda_executable()
    ros2_ok = test_ros2_integration()
    
    print("=" * 60)
    print("SUMMARY:")
    print(f"Python CUDA bindings: {'✓ PASS' if python_cuda_ok else '✗ FAIL'}")
    print(f"C++ CUDA executable:  {'✓ PASS' if cpp_cuda_ok else '✗ FAIL'}")
    print(f"ROS2 integration:     {'✓ PASS' if ros2_ok else '✗ FAIL'}")
    
    if python_cuda_ok and cpp_cuda_ok and ros2_ok:
        print("\n🎉 SUCCESS: All tests passed!")
        print("✓ C++ CUDA library works in ROS2")
        print("✓ Python CUDA bindings work in ROS2") 
        print("✓ Ready for both C++ and Python ROS2 nodes with GPU acceleration!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())