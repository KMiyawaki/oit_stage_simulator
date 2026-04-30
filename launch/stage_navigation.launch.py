import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from oit_stage_simulator.launch_utils import PackagePath, declare_arg


def generate_launch_description():
    path = PackagePath()
    map = declare_arg('map', 'HRC', 'map file name, without .yaml')
    world = declare_arg(
        'world', map.conf, 'World file relative to the project world file, without .world')

    stage = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'stage.launch.py')),
        launch_arguments={'world': world.conf}.items())
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'rviz.launch.py')),
        launch_arguments={'rviz_conf': 'navigation', 'use_sim_time': 'true'}.items())
    amcl = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'amcl.launch.py')),
        launch_arguments={'map': map.conf, 'use_sim_time': 'true'}.items())
    navigation_common = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'navigation_common.launch.py')),
        launch_arguments={'use_sim_time': 'true'}.items())

    return LaunchDescription([map.arg, world.arg, stage, rviz, amcl, navigation_common])
