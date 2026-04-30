import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import RewrittenYaml

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration

pack_dir = get_package_share_directory('oit_stage_simulator')


def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='false')
    use_sim_time = LaunchConfiguration(use_sim_time_arg.name)
    params = {'behavior_server.yaml': None,
              'bt_navigator.yaml': None,
              'controller_server.yaml': None,
              'planner_server.yaml': None,
              'smoother_server.yaml': None,
              'velocity_smoother.yaml': None,
              'waypoint_follower.yaml': None}
    for k in params.keys():
        yaml = os.path.join(pack_dir, 'config', 'nav2', k)
        params[k] = [ParameterFile(
            RewrittenYaml(
                source_file=yaml,
                root_key=None,
                param_rewrites={'use_sim_time': use_sim_time},
                convert_types=True),
            allow_substs=True)]

    lifecycle_nodes = ['controller_server',
                       'smoother_server',
                       'planner_server',
                       'behavior_server',
                       'bt_navigator',
                       'waypoint_follower',
                       'velocity_smoother']
    navigation_nodes = GroupAction(
        actions=[
            Node(package='nav2_controller',
                 executable='controller_server',
                 name='controller_server',
                 output='screen',
                 respawn=True,
                 respawn_delay=2.0,
                 parameters=params['controller_server.yaml'],
                 remappings=[('cmd_vel', 'cmd_vel_nav')]),
            Node(package='nav2_smoother',
                 executable='smoother_server',
                 name='smoother_server',
                 output='screen',
                 respawn=True,
                 respawn_delay=2.0,
                 parameters=params['smoother_server.yaml']),
            Node(package='nav2_planner',
                 executable='planner_server',
                 name='planner_server',
                 output='screen',
                 respawn=True,
                 respawn_delay=2.0,
                 parameters=params['planner_server.yaml']),
            Node(package='nav2_behaviors',
                 executable='behavior_server',
                 name='behavior_server',
                 output='screen',
                 respawn=True,
                 respawn_delay=2.0,
                 parameters=params['behavior_server.yaml']),
            Node(package='nav2_bt_navigator',
                 executable='bt_navigator',
                 name='bt_navigator',
                 output='screen',
                 respawn=True,
                 respawn_delay=2.0,
                 parameters=params['bt_navigator.yaml']),
            Node(package='nav2_waypoint_follower',
                 executable='waypoint_follower',
                 name='waypoint_follower',
                 output='screen',
                 respawn=True,
                 respawn_delay=2.0,
                 parameters=params['waypoint_follower.yaml']),
            Node(package='nav2_velocity_smoother',
                 executable='velocity_smoother',
                 name='velocity_smoother',
                 output='screen',
                 respawn=True,
                 respawn_delay=2.0,
                 parameters=params['velocity_smoother.yaml'],
                 remappings=[('cmd_vel', 'cmd_vel_nav'),
                             ('cmd_vel_smoothed', 'cmd_vel')]),
            Node(package='nav2_lifecycle_manager',
                 executable='lifecycle_manager',
                 name='lifecycle_manager_navigation',
                 output='screen',
                 parameters=[use_sim_time,
                             {'autostart': True},
                             {'node_names': lifecycle_nodes}]),
        ]
    )

    return LaunchDescription([use_sim_time_arg, navigation_nodes])
