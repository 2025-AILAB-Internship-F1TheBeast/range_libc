cmake_minimum_required(VERSION 3.8)
project(range_libc LANGUAGES CXX CUDA)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# Library source files (excluding main.cpp for executable)
file(GLOB LIB_SRCS 
	"vendor/lodepng/lodepng.cpp" )

# Executable source files
file(GLOB EXEC_SRCS 
	main.cpp 
	"vendor/lodepng/lodepng.cpp" )

option(WITH_CUDA "Compile CUDA ray cast varients" ON)
# set(CHUNK_SIZE 16384)
# set(CHUNK_THREADS 256)
set(CHUNK_SIZE 262144)
set(CHUNK_THREADS 256)
# set(CHUNK_SIZE 65536)
# set(CHUNK_THREADS 256)


set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib")
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

SET(BASEPATH "${CMAKE_SOURCE_DIR}") 
add_definitions ( -DBASEPATH=${BASEPATH} )
add_subdirectory(${BASEPATH}/vendor/gflags)

# Use the basepath as a search location for includes
include_directories(${BASEPATH})

include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
if(COMPILER_SUPPORTS_CXX11)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
elseif(COMPILER_SUPPORTS_CXX0X)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
else()
        message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

# set(CMAKE_CXX_FLAGS "-march=native -fverbose-asm -ffast-math -fno-math-errno -g -save-temps ${CMAKE_CXX_FLAGS}")
# set(CMAKE_CXX_FLAGS "-march=native -ffast-math -fno-math-errno -g -rdynamic -save-temps ${CMAKE_CXX_FLAGS}")
set(CMAKE_CXX_FLAGS "-march=native -ffast-math -fno-math-errno ${CMAKE_CXX_FLAGS} -O3")
# set(CMAKE_CXX_FLAGS "-fverbose-asm -ffast-math -fno-math-errno -save-temps ${CMAKE_CXX_FLAGS}")
# set(CMAKE_CXX_FLAGS "-g -save-temps ${CMAKE_CXX_FLAGS}")

set(CMAKE_BUILD_TYPE Release)

if (WITH_CUDA)
	add_definitions(-DUSE_CUDA=1)
	add_definitions(-DCHUNK_SIZE=${CHUNK_SIZE})
	add_definitions(-DNUM_THREADS=${CHUNK_THREADS})

	# Library CUDA sources (excluding main.cpp)
	file(GLOB CUDA_LIB_SRCS 
		"includes/kernels.cu"
		"vendor/lodepng/lodepng.cpp" )
	
	# Executable CUDA sources
	file(GLOB CUDA_EXEC_SRCS 
		main.cpp 
		"includes/kernels.cu"
		"vendor/lodepng/lodepng.cpp" )

	# Modern CMake CUDA support
	find_package(CUDAToolkit REQUIRED)
	
	# Create shared library for ROS2 nodes
	add_library(${PROJECT_NAME} SHARED ${CUDA_LIB_SRCS})
	target_link_libraries(${PROJECT_NAME} gflags pthread CUDA::cudart)
	set_target_properties(${PROJECT_NAME} PROPERTIES 
		CUDA_SEPARABLE_COMPILATION ON
		CUDA_ARCHITECTURES "87"
	)
	
	# Create executable for testing
	add_executable(range_lib ${CUDA_EXEC_SRCS})
	target_link_libraries(range_lib gflags pthread CUDA::cudart)
	set_target_properties(range_lib PROPERTIES 
		CUDA_SEPARABLE_COMPILATION ON
		CUDA_ARCHITECTURES "87"
	)

else()
	add_definitions(-DUSE_CUDA=0)
	
	# Create shared library for ROS2 nodes
	add_library(${PROJECT_NAME} SHARED ${LIB_SRCS})
	target_link_libraries(${PROJECT_NAME} gflags pthread)
	
	# Create executable for testing
	add_executable(range_lib ${EXEC_SRCS})
	target_link_libraries(range_lib gflags pthread)
endif()

# Install headers
install(
  DIRECTORY includes/
  DESTINATION include/${PROJECT_NAME}
)

# Install library
install(
  TARGETS ${PROJECT_NAME}
  EXPORT ${PROJECT_NAME}_targets
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
)

# Install executable (optional, for testing)
install(
  TARGETS range_lib
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python wrapper
ament_python_install_package(pywrapper_ros2)

# Export targets for other ROS2 packages to use
ament_export_targets(${PROJECT_NAME}_targets HAS_LIBRARY_TARGET)
ament_export_dependencies()
ament_export_include_directories(include)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()