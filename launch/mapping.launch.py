import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            TimerAction)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression

pack_dir = get_package_share_directory('oit_stage_simulator')
slam_toolbox_dir = get_package_share_directory('slam_toolbox')


def generate_launch_description():
    teleop_arg = DeclareLaunchArgument('teleop', default_value='joy',
                                       description='teleop device type', choices=['joy', 'key', 'mouse', 'none'])
    teleop = LaunchConfiguration(teleop_arg.name)

    slam_arg = DeclareLaunchArgument('slam', default_value='cartographer',
                                     choices=['slam_toolbox', 'cartographer'])
    slam = LaunchConfiguration(slam_arg.name)

    slam_launch = os.path.join(
        slam_toolbox_dir, 'launch', 'online_async_launch.py')
    slam_toolbox_online_yaml = os.path.join(
        pack_dir, 'config', 'slam_toolbox_online.yaml')
    cartographer_launch = os.path.join(
        pack_dir, 'launch', 'cartographer.launch.py')

    devices = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'devices.launch.py')))
    teleop_select = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'teleop_select.launch.py')),
        launch_arguments={'teleop': teleop}.items())
    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'rviz.launch.py')),
        launch_arguments={'use_sim_time': 'false', 'rviz_conf': 'mapping'}.items())
    slam_toolbox = IncludeLaunchDescription(PythonLaunchDescriptionSource(slam_launch),
                                            launch_arguments={
                                                'use_sim_time': 'false', 'slam_params_file': slam_toolbox_online_yaml}.items(),
                                            condition=IfCondition(PythonExpression(["'", slam, "' == 'slam_toolbox'"])))
    cartographer = IncludeLaunchDescription(PythonLaunchDescriptionSource(cartographer_launch),
                                            launch_arguments={
                                                'use_sim_time': 'false'}.items(),
                                            condition=IfCondition(PythonExpression(["'", slam, "' == 'cartographer'"])))

    timer = TimerAction(period=7.5, actions=[rviz, slam_toolbox, cartographer])

    return LaunchDescription([teleop_arg, slam_arg, devices, teleop_select, timer])
