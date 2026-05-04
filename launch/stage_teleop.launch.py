import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from oit_stage_simulator.launch_utils import PackagePath, declare_arg


def generate_launch_description():
    path = PackagePath()
    world = declare_arg(
        'world', '00000000_000000_sample/00000000_000000_sample', 'World file relative to the project world file, without .world')
    teleop = declare_arg(
        'teleop', 'key', 'teleop device type', ['joy', 'key', 'mouse', 'none'])

    stage = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'stage.launch.py')),
        launch_arguments={'world': world.conf}.items())
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'rviz.launch.py')),
        launch_arguments={'rviz_conf': 'simple', 'use_sim_time': 'true'}.items())
    teleop_select = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'teleop_select.launch.py')),
        launch_arguments={'teleop': teleop.conf}.items())

    return LaunchDescription([world.arg, teleop.arg, stage, rviz, teleop_select])
