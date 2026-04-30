import os

from launch_ros.actions import Node

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from oit_stage_simulator.launch_utils import PackagePath, declare_arg


def generate_launch_description():
    path = PackagePath()
    map = declare_arg('map', 'HRC', 'map file name, without .yaml')
    map_path = LaunchConfiguration(
        map.arg.name + '_path', default=[path.maps, '/', map.conf, '.yaml'])
    use_sim_time = declare_arg(
        'use_sim_time', 'false', '', choices=['true', 'false'])

    amcl_params = os.path.join(path.config, 'amcl.yaml')

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        respawn=True,
        respawn_delay=2.0,
        parameters=[{'yaml_filename': map_path, 'use_sim_time': use_sim_time.conf}])

    amcl = Node(package='nav2_amcl',
                executable='amcl',
                name='amcl',
                output='screen',
                parameters=[amcl_params, {'use_sim_time': use_sim_time.conf}])

    lifecycle_nodes = ['map_server', 'amcl']
    lifecycle_manager_localization = Node(package='nav2_lifecycle_manager',
                                          executable='lifecycle_manager',
                                          name='lifecycle_manager_localization',
                                          output='screen',
                                          parameters=[{
                                              'use_sim_time': use_sim_time.conf,
                                              'autostart': True,
                                              'node_names': lifecycle_nodes}])

    return LaunchDescription([map.arg, use_sim_time.arg, map_server, amcl, lifecycle_manager_localization])
