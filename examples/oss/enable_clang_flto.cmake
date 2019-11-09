# NOTE: lto supports: 3.9~
# cmake_minimum_required(VERSION 3.9)

set(CMAKE_C_COMPILER   "/usr/bin/clang"   CACHE STRING "clang compiler"   FORCE)
set(CMAKE_CXX_COMPILER "/usr/bin/clang++" CACHE STRING "clang++ compiler" FORCE)

# FYI
# [CMake support for GCC's link time optimization \(LTO\) \- Stack Overflow]( https://stackoverflow.com/questions/31355692/cmake-support-for-gccs-link-time-optimization-lto )

# NOTE: set below code to each build target
# set(flto_target_names CMAKE_C_FLAGS CMAKE_CXX_FLAGS CMAKE_EXE_LINKER_FLAGS CMAKE_SHARED_LINKER_FLAGS)
# foreach(list_name IN LISTS flto_target_names)
  # set(${list_name} "${${list_name}} -flto")
# endforeach()

# NOTE: maybe you can use below command
# or -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=TRUE
# set(CMAKE_INTERPROCEDURAL_OPTIMIZATION CACHE BOOL TRUE FORCE)
# set_property(TARGET xxx PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
