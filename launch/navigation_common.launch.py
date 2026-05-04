
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from oit_stage_simulator.launch_utils import (PackagePath, amcl_nodes,
                                              declare_arg, navigation_nodes)


def generate_launch_description():
    path = PackagePath()
    map = declare_arg('map', 'HRC', 'map file name, without .yaml')
    map_path = LaunchConfiguration(
        map.arg.name + '_path', default=[path.maps, '/', map.conf, '.yaml'])
    use_sim_time = declare_arg(
        'use_sim_time', 'false', '', choices=['true', 'false'])

    map_server, amcl = amcl_nodes(map_path, use_sim_time.conf)
    controller_server, smoother_server, planner_server, behavior_server, bt_navigator, waypoint_follower, velocity_smoother = navigation_nodes(
        use_sim_time.conf)

    lifecycle_nodes = [map_server.name, amcl.name, controller_server.name,
                       smoother_server.name, planner_server.name, behavior_server.name, bt_navigator.name,
                       waypoint_follower.name, velocity_smoother.name]

    lifecycle_manager = Node(package='nav2_lifecycle_manager',
                             executable='lifecycle_manager',
                             name='lifecycle_manager_navigation',
                             output='screen',
                             parameters=[{'use_sim_time': use_sim_time.conf},
                                         {'autostart': True},
                                         {'node_names': lifecycle_nodes}])

    return LaunchDescription([use_sim_time.arg,
                              map_server.node, amcl.node,
                              controller_server.node, smoother_server.node, planner_server.node,
                              behavior_server.node, bt_navigator.node, waypoint_follower.node, velocity_smoother.node,
                              lifecycle_manager])
