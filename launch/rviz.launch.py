
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from oit_stage_simulator.launch_utils import PackagePath, declare_arg


def generate_launch_description():
    path = PackagePath()
    rviz = declare_arg(
        'rviz_conf', 'simple', 'rviz setting', ['simple', 'mapping', 'navigation', 'none'])

    rviz_conf_path = LaunchConfiguration(
        rviz.arg.name + '_path', default=[path.rviz, '/', rviz.conf, '.rviz'])

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
