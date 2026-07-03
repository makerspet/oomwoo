cmake_minimum_required(VERSION 3.8)
project(oomwoo_gazebo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)

install(DIRECTORY urdf config rviz launch worlds sdf sdf/meshes
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  oomwoo_gazebo/bump_recovery.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
