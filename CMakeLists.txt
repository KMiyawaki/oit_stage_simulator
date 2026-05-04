cmake_minimum_required(VERSION 3.8)
project(oit_stage_simulator)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

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

# Install Python modules to the site-packages directory to make them importable
ament_python_install_package(${PROJECT_NAME})

# Install scripts
file(GLOB ALL_SCRIPTS 
  "scripts/*.sh"
  "scripts/*.py"
)
if(ALL_SCRIPTS)
  install(PROGRAMS
    ${ALL_SCRIPTS}
    DESTINATION lib/${PROJECT_NAME}
  )
endif()

# Install assets
install(DIRECTORY 
  config
  launch
  maps
  rviz
  DESTINATION share/${PROJECT_NAME}
)

# Must be called at the end to finalize the ROS 2 package configuration
ament_package()
