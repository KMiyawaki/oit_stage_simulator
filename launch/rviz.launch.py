from types import SimpleNamespace

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression

pack_dir = get_package_share_directory('oit_stage_simulator')


def declare_arg(name, default_value, description="", choices=None):
    return SimpleNamespace(
        name=name,
        arg=DeclareLaunchArgument(
            name, default_value=default_value, description=description, choices=choices),
        conf=LaunchConfiguration(name))


def generate_launch_description():
    rviz = declare_arg(
        'rviz_conf', 'simple', 'rviz setting', ['simple', 'mapping', 'navigation', 'none'])

    rviz_conf_path = LaunchConfiguration(
        rviz.arg.name + '_path', default=[pack_dir, '/rviz/', rviz.conf, '.rviz'])

    use_sim_time = declare_arg(
        'use_sim_time', 'false', '', choices=['true', 'false'])

    rviz_node = Node(package='rviz2',
                     executable='rviz2',
                     name='rviz2',
                     output='screen',
                     parameters=[{'use_sim_time': use_sim_time.conf}],
                     condition=IfCondition(PythonExpression(
                         ["'", rviz.conf, "' != 'none'"])),
                     arguments=['-d', rviz_conf_path, '--ros-args', '--log-level', 'rviz2:=WARN'])

    return LaunchDescription([rviz.arg, use_sim_time.arg, rviz_node])
