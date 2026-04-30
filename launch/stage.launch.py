from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')


def generate_launch_description():
    world_arg = DeclareLaunchArgument('world', default_value='HRC',
                                      description='World file relative to the project world file, without .world')
    world = LaunchConfiguration(world_arg.name)
    world_path = LaunchConfiguration(
        world_arg.name + '_path', default=[pack_dir, '/maps/', world, '.world'])

    return LaunchDescription([
        world_arg,
        Node(
            package='stage_ros2',
            executable='stage_ros2',
            name='stage',
            remappings=[('base_scan', 'scan'), ('image', 'video_source/raw')],
            parameters=[{"world_file": world_path},
                        {'use_static_transformations': True}]
        )
    ])
