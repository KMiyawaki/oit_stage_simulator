import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')


def generate_launch_description():
    map_arg = DeclareLaunchArgument('map', default_value='HRC',
                                    description='map file name, without .yaml')
    map = LaunchConfiguration(map_arg.name)

    world_arg = DeclareLaunchArgument('world', default_value=map,
                                      description='World file relative to the project world file, without .world')
    world = LaunchConfiguration(world_arg.name)

    stage = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'stage.launch.py')),
        launch_arguments={'world': world}.items())
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'rviz.launch.py')),
        launch_arguments={'rviz_conf': 'navigation', 'use_sim_time': 'true'}.items())
    amcl = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'amcl.launch.py')),
        launch_arguments={'map': map, 'use_sim_time': 'true'}.items())
    navigation_common = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'navigation_common.launch.py')),
        launch_arguments={'use_sim_time': 'true'}.items())

    return LaunchDescription([map_arg, world_arg, stage, rviz, amcl, navigation_common])
