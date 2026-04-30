import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            TimerAction)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')


def generate_launch_description():
    map_arg = DeclareLaunchArgument('map', default_value='test',
                                    description='map file name, without .yaml')
    map = LaunchConfiguration(map_arg.name)

    devices = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'devices.launch.py')))
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'rviz.launch.py')),
        launch_arguments={'rviz_conf': 'navigation', 'use_sim_time': 'false'}.items())
    amcl = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'amcl.launch.py')),
        launch_arguments={'map': map, 'use_sim_time': 'false'}.items())
    navigation_common = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'navigation_common.launch.py')),
        launch_arguments={'use_sim_time': 'false'}.items())

    timer = TimerAction(period=7.5, actions=[rviz, amcl, navigation_common])

    return LaunchDescription([map_arg, devices, timer])
