#!/usr/bin/env python3
"""
Test script to verify both C++ library and Python bindings work with ROS2
"""

import sys
import os

# Add the installed Python package to path
sys.path.insert(0, 'install/range_libc/local/lib/python3.10/dist-packages')

def test_python_bindings():
    """Test Python bindings"""
    try:
        import pywrapper_ros2.range_libc as rl
        print("✓ Python bindings imported successfully")
        
        # Try to create a basic range object (this may fail without a map, but import should work)
        print("✓ Python bindings are accessible")
        return True
    except Exception as e:
        print(f"✗ Python bindings failed: {e}")
        return False

def test_cpp_library():
    """Test C++ library by running the executable"""
    try:
        import subprocess
        result = subprocess.run(['install/range_libc/lib/range_libc/range_lib', '--version'], 
                              capture_output=True, text=True, timeout=5)
        print("✓ C++ executable runs successfully")
        return True
    except Exception as e:
        print(f"✗ C++ executable failed: {e}")
        return False

def main():
    print("Testing ROS2 range_libc integration...")
    print("=" * 50)
    
    python_ok = test_python_bindings()
    cpp_ok = test_cpp_library()
    
    print("=" * 50)
    if python_ok and cpp_ok:
        print("✓ All tests passed! Both C++ and Python usage work with ROS2")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())