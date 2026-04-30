import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')


def generate_launch_description():
    map_arg = DeclareLaunchArgument('map', default_value='test',
                                    description='map file name, without .yaml')
    map = LaunchConfiguration(map_arg.name)
    map_path = LaunchConfiguration(
        map_arg.name + '_path', default=[pack_dir, '/maps/', map, '.yaml'])

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='false')
    use_sim_time = LaunchConfiguration(use_sim_time_arg.name)

    amcl_params = os.path.join(pack_dir, 'config', 'amcl.yaml')

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        respawn=True,
        respawn_delay=2.0,
        parameters=[{'yaml_filename': map_path, 'use_sim_time': use_sim_time}])

    amcl = Node(package='nav2_amcl',
                executable='amcl',
                name='amcl',
                output='screen',
                parameters=[amcl_params, {'use_sim_time': use_sim_time}])

    lifecycle_nodes = ['map_server', 'amcl']
    lifecycle_manager_localization = Node(package='nav2_lifecycle_manager',
                                          executable='lifecycle_manager',
                                          name='lifecycle_manager_localization',
                                          output='screen',
                                          parameters=[{
                                              'use_sim_time': use_sim_time,
                                              'autostart': True,
                                              'node_names': lifecycle_nodes}])

    return LaunchDescription([map_arg, use_sim_time_arg, map_server, amcl, lifecycle_manager_localization])
