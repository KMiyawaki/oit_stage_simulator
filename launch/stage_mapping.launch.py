import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from oit_stage_simulator.launch_utils import PackagePath, declare_arg

slam_toolbox_dir = get_package_share_directory('slam_toolbox')


def generate_launch_description():
    path = PackagePath()
    world = declare_arg(
        'world', 'HRC', 'World file relative to the project world file, without .world')
    teleop = declare_arg(
        'teleop', 'key', 'teleop device type', ['joy', 'key', 'mouse', 'none'])

    slam_launch = os.path.join(
        slam_toolbox_dir, 'launch', 'online_async_launch.py')
    slam_toolbox_online_yaml = os.path.join(
        path.config, 'slam_toolbox_online.yaml')

    stage = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'stage.launch.py')),
        launch_arguments={'world': world.conf}.items())
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'rviz.launch.py')),
        launch_arguments={'use_sim_time': 'true', 'rviz_conf': 'mapping'}.items())
    teleop_select = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(path.launch, 'teleop_select.launch.py')),
        launch_arguments={'teleop': teleop.conf}.items())
    slam = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        slam_launch), launch_arguments={'use_sim_time': 'true', 'slam_params_file': slam_toolbox_online_yaml}.items())

    return LaunchDescription([world.arg, teleop.arg, stage, rviz, teleop_select, slam])
