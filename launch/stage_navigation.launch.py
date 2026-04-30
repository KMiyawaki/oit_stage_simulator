import os
from types import SimpleNamespace

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')


def declare_arg(name, default_value, description=""):
    return SimpleNamespace(
        name=name,
        arg=DeclareLaunchArgument(
            name, default_value=default_value, description=description),
        conf=LaunchConfiguration(name))


def generate_launch_description():
    map = declare_arg('map', 'HRC', 'map file name, without .yaml')
    world = declare_arg(
        'world', map.conf, 'World file relative to the project world file, without .world')

    stage = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'stage.launch.py')),
        launch_arguments={'world': world.conf}.items())
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'rviz.launch.py')),
        launch_arguments={'rviz_conf': 'navigation', 'use_sim_time': 'true'}.items())
    amcl = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'amcl.launch.py')),
        launch_arguments={'map': map.conf, 'use_sim_time': 'true'}.items())
    navigation_common = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'navigation_common.launch.py')),
        launch_arguments={'use_sim_time': 'true'}.items())

    return LaunchDescription([map.arg, world.arg, stage, rviz, amcl, navigation_common])
