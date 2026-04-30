import math
import os
from types import SimpleNamespace

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression

pack_dir = get_package_share_directory('oit_stage_simulator')


def declare_arg(name, default_value, description="", choices=None):
    return SimpleNamespace(
        name=name,
        arg=DeclareLaunchArgument(
            name, default_value=default_value, description=description, choices=choices),
        conf=LaunchConfiguration(name))


def if_condition(conf, op, value):
    if type(value) == str:
        return IfCondition(PythonExpression(["'", conf, "'", op, "'", value, "'"]))
    else:
        return IfCondition(PythonExpression([conf, op, value]))


def generate_launch_description():
    joy_yaml = os.path.join(pack_dir, 'config', 'joy.yaml')

    teleop = declare_arg(
        'teleop', 'key', 'teleop device type', ['joy', 'key', 'mouse', 'none'])

    joy = GroupAction(actions=[
        Node(package='joy',
             executable='joy_node',
             name='joy_node',
             output='screen'),
        Node(package='teleop_twist_joy',
             executable='teleop_node',
             name='teleop_node',
             output='screen',
             parameters=[joy_yaml])],
        condition=if_condition(teleop.conf, '==', 'joy'))

    key = Node(package='key_teleop',
               executable='key_teleop',
               name='key_teleop',
               output='screen',
               prefix='xterm -e',
               remappings=[('key_vel', 'cmd_vel')],
               parameters=[{'forward_rate': 0.2, 'backward_rate': 0.2,
                            'rotation_rate': math.radians(60.0),
                            'twist_stamped_enabled': False}],
               condition=if_condition(teleop.conf, '==', 'key'))

    mouse = Node(package='mouse_teleop',
                 executable='mouse_teleop',
                 name='mouse_teleop',
                 output='screen',
                 remappings=[('mouse_vel', 'cmd_vel')],
                 condition=if_condition(teleop.conf, '==', 'mouse'))

    return LaunchDescription([teleop.arg, joy, key, mouse])
