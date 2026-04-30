
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from oit_stage_simulator.launch_utils import PackagePath, declare_arg


def generate_launch_description():
    path = PackagePath()
    world = declare_arg(
        'world', 'HRC', 'World file relative to the project world file, without .world')

    world_path = LaunchConfiguration(
        world.arg.name + '_path', default=[path.maps, '/', world.conf, '.world'])

    return LaunchDescription([
        world.arg,
        Node(
            package='stage_ros2',
            executable='stage_ros2',
            name='stage',
            remappings=[('base_scan', 'scan'), ('image', 'video_source/raw')],
            parameters=[{"world_file": world_path},
                        {'use_static_transformations': True}]
        )
    ])
