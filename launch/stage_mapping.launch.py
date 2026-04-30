import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')
slam_toolbox_dir = get_package_share_directory('slam_toolbox')


def generate_launch_description():
    world_arg = DeclareLaunchArgument('world', default_value='HRC',
                                      description='World file relative to the project world file, without .world')
    world = LaunchConfiguration(world_arg.name)

    teleop_arg = DeclareLaunchArgument('teleop', default_value='key',
                                       description='teleop device type', choices=['joy', 'key', 'mouse', 'none'])
    teleop = LaunchConfiguration(teleop_arg.name)

    slam_launch = os.path.join(
        slam_toolbox_dir, 'launch', 'online_async_launch.py')
    slam_toolbox_online_yaml = os.path.join(
        pack_dir, 'config', 'slam_toolbox_online.yaml')

    stage = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'stage.launch.py')),
        launch_arguments={'world': world}.items())
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'rviz.launch.py')),
        launch_arguments={'use_sim_time': 'true', 'rviz_conf': 'mapping'}.items())
    teleop_select = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'teleop_select.launch.py')),
        launch_arguments={'teleop': teleop}.items())
    slam = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        slam_launch), launch_arguments={'use_sim_time': 'true', 'slam_params_file': slam_toolbox_online_yaml}.items())

    return LaunchDescription([world_arg, teleop_arg, stage, rviz, teleop_select, slam])
