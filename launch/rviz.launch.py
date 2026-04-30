from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression

pack_dir = get_package_share_directory('oit_stage_simulator')


def generate_launch_description():
    rviz_arg = DeclareLaunchArgument('rviz_conf', default_value='simple',
                                     description='rviz setting', choices=['simple', 'check_urdf', 'mapping', 'navigation', 'lidar', 'none'])
    rviz_conf = LaunchConfiguration(rviz_arg.name)
    rviz_conf_path = LaunchConfiguration(
        rviz_arg.name + '_path', default=[pack_dir, '/rviz/', rviz_conf, '.rviz'])

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='false', choices=['true', 'false'])
    use_sim_time = LaunchConfiguration(use_sim_time_arg.name)

    rviz = Node(package='rviz2',
                executable='rviz2',
                name='rviz2',
                output='screen',
                parameters=[{'use_sim_time': use_sim_time}],
                condition=IfCondition(PythonExpression(
                    ["'", rviz_conf, "' != 'none'"])),
                arguments=['-d', rviz_conf_path, '--ros-args', '--log-level', 'rviz2:=WARN'])

    return LaunchDescription([rviz_arg, use_sim_time_arg, rviz])
