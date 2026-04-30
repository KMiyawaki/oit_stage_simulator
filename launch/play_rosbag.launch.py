import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess,
                            IncludeLaunchDescription)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression

pack_dir = get_package_share_directory('oit_stage_simulator')
ws_dir = pack_dir.replace('install/oit_stage_simulator/share', 'src')
slam_toolbox_dir = get_package_share_directory('slam_toolbox')


def generate_launch_description():
    bag_arg = DeclareLaunchArgument(
        'bag', default_value='rosbag2_2023_10_30-16_34_39')
    bag = LaunchConfiguration(bag_arg.name)
    bag_path = LaunchConfiguration(
        bag_arg.name + '_path', default=[ws_dir, '/bags/', bag])

    slam_arg = DeclareLaunchArgument('slam', default_value='cartographer',
                                     choices=['slam_toolbox', 'cartographer', 'none'])
    slam = LaunchConfiguration(slam_arg.name)

    rviz_conf_arg = DeclareLaunchArgument(
        'rviz_conf', default_value=PythonExpression(["'simple'", " if '", slam, "' == 'none' else 'mapping'"]))
    rviz_conf = LaunchConfiguration(rviz_conf_arg.name)

    slam_toolbox_offline_yaml = os.path.join(
        pack_dir, 'config', 'slam_toolbox_offline.yaml')

    slam_offline = Node(
        parameters=[slam_toolbox_offline_yaml],
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        condition=IfCondition(PythonExpression(
            ["'", slam, "' == 'slam_toolbox'"]))
    )

    cartographer = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'cartographer.launch.py')),
        launch_arguments={'use_sim_time': 'true'}.items(),
        condition=IfCondition(PythonExpression(["'", slam, "' == 'cartographer'"])))

    rviz = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        os.path.join(pack_dir, 'launch', 'rviz.launch.py')),
        launch_arguments={'rviz_conf': rviz_conf,
                          'use_sim_time': 'true'}.items())

    bag_play = ExecuteProcess(
        cmd=['ros2', 'bag', 'play', bag_path],
        output='screen'
    )

    return LaunchDescription([bag_arg, slam_arg, rviz_conf_arg, slam_offline, cartographer, rviz, bag_play])
