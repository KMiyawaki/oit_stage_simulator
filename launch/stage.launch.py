from types import SimpleNamespace

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')


def declare_arg(name, default_value, description="", choices=None):
    return SimpleNamespace(
        name=name,
        arg=DeclareLaunchArgument(
            name, default_value=default_value, description=description, choices=choices),
        conf=LaunchConfiguration(name))


def generate_launch_description():
    world = declare_arg(
        'world', 'HRC', 'World file relative to the project world file, without .world')

    world_path = LaunchConfiguration(
        world.arg.name + '_path', default=[pack_dir, '/maps/', world.conf, '.world'])

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
