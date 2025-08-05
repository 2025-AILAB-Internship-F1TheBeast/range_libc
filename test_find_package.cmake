cmake_minimum_required(VERSION 3.8)

# Test if we can find range_libc
find_package(range_libc QUIET)

if(range_libc_FOUND)
    message(STATUS "✅ SUCCESS: Found range_libc package")
    message(STATUS "  - Libraries: ${range_libc_LIBRARIES}")
    message(STATUS "  - Include dirs: ${range_libc_INCLUDE_DIRS}")
else()
    message(STATUS "❌ FAILED: Could not find range_libc package")
    message(STATUS "  - CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
    message(STATUS "  - CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")
endif()