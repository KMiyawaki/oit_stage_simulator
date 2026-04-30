import os
from types import SimpleNamespace

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')
slam_toolbox_dir = get_package_share_directory('slam_toolbox')


def declare_arg(name, default_value, description="", choices=None):
    return SimpleNamespace(
        name=name,
        arg=DeclareLaunchArgument(
            name, default_value=default_value, description=description, choices=choices),
        conf=LaunchConfiguration(name))


def generate_launch_description():
    world = declare_arg(
        'world', 'HRC', 'World file relative to the project world file, without .world')
    teleop = declare_arg(
        'teleop', 'key', 'teleop device type', ['joy', 'key', 'mouse', 'none'])

    slam_launch = os.path.join(
        slam_toolbox_dir, 'launch', 'online_async_launch.py')
    slam_toolbox_online_yaml = os.path.join(
        pack_dir, 'config', 'slam_toolbox_online.yaml')

    stage = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'stage.launch.py')),
        launch_arguments={'world': world.conf}.items())
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'rviz.launch.py')),
        launch_arguments={'use_sim_time': 'true', 'rviz_conf': 'mapping'}.items())
    teleop_select = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'teleop_select.launch.py')),
        launch_arguments={'teleop': teleop.conf}.items())
    slam = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        slam_launch), launch_arguments={'use_sim_time': 'true', 'slam_params_file': slam_toolbox_online_yaml}.items())

    return LaunchDescription([world.arg, teleop.arg, stage, rviz, teleop_select, slam])
