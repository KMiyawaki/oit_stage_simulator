import math
import os

from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import GroupAction
from oit_stage_simulator.launch_utils import (PackagePath, declare_arg,
                                              if_condition)


def generate_launch_description():
    path = PackagePath()
    joy_yaml = os.path.join(path.config, 'joy.yaml')

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
