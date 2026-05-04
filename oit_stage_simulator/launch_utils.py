import os
from types import SimpleNamespace

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import RewrittenYaml

from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression

'''
$ ros2 lifecycle nodes
/amcl
/behavior_server
/bt_navigator
/controller_server
/global_costmap/global_costmap
/local_costmap/local_costmap
/map_server
/planner_server
/smoother_server
/velocity_smoother
/waypoint_follower
'''


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


class PackagePath:
    def __init__(self, package_name=None):
        if package_name is None:
            self._pkg_name = os.path.basename(os.path.dirname(__file__))
        else:
            self._pkg_name = package_name
        self._share_dir = None

    @property
    def package_name(self):
        return self._pkg_name

    @property
    def share(self):
        if self._share_dir is None:
            self._share_dir = get_package_share_directory(self._pkg_name)
        return self._share_dir

    def join(self, *args):
        return os.path.join(self.share, *args)

    @property
    def maps(self): return self.join('maps')

    @property
    def config(self): return self.join('config')

    @property
    def config_nav2(self): return self.join('config', 'nav2')

    @property
    def rviz(self): return self.join('rviz')

    @property
    def launch(self): return self.join('launch')


def amcl_nodes(map_path_conf, use_sim_time_conf):
    path = PackagePath()
    amcl_params = os.path.join(path.config, 'amcl.yaml')

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        respawn=True,
        respawn_delay=2.0,
        parameters=[{'yaml_filename': map_path_conf, 'use_sim_time': use_sim_time_conf}])

    amcl = Node(package='nav2_amcl',
                executable='amcl',
                name='amcl',
                output='screen',
                parameters=[amcl_params, {'use_sim_time': use_sim_time_conf}])

    return SimpleNamespace(node=map_server, name='map_server'), SimpleNamespace(node=amcl, name='amcl')


def navigation_nodes(use_sim_time_conf):
    path = PackagePath()
    params = {'behavior_server.yaml': None,
              'bt_navigator.yaml': None,
              'controller_server.yaml': None,
              'planner_server.yaml': None,
              'smoother_server.yaml': None,
              'velocity_smoother.yaml': None,
              'waypoint_follower.yaml': None}
    for k in params.keys():
        yaml = os.path.join(path.config_nav2, k)
        params[k] = [ParameterFile(
            RewrittenYaml(
                source_file=yaml,
                root_key=None,
                param_rewrites={'use_sim_time': use_sim_time_conf},
                convert_types=True),
            allow_substs=True)]

    n = Node(package='nav2_controller',
             executable='controller_server',
             name='controller_server',
             output='screen',
             respawn=True,
             respawn_delay=2.0,
             parameters=params['controller_server.yaml'],
             remappings=[('cmd_vel', 'cmd_vel_nav')])
    controller_server = SimpleNamespace(node=n, name='controller_server')

    n = Node(package='nav2_smoother',
             executable='smoother_server',
             name='smoother_server',
             output='screen',
             respawn=True,
             respawn_delay=2.0,
             parameters=params['smoother_server.yaml'])
    smoother_server = SimpleNamespace(node=n, name='smoother_server')

    n = Node(package='nav2_planner',
             executable='planner_server',
             name='planner_server',
             output='screen',
             respawn=True,
             respawn_delay=2.0,
             parameters=params['planner_server.yaml'])
    planner_server = SimpleNamespace(node=n, name='planner_server')

    n = Node(package='nav2_behaviors',
             executable='behavior_server',
             name='behavior_server',
             output='screen',
             respawn=True,
             respawn_delay=2.0,
             parameters=params['behavior_server.yaml'])
    behavior_server = SimpleNamespace(node=n, name='behavior_server')

    n = Node(package='nav2_bt_navigator',
             executable='bt_navigator',
             name='bt_navigator',
             output='screen',
             respawn=True,
             respawn_delay=2.0,
             parameters=params['bt_navigator.yaml'])
    bt_navigator = SimpleNamespace(node=n, name='bt_navigator')

    n = Node(package='nav2_waypoint_follower',
             executable='waypoint_follower',
             name='waypoint_follower',
             output='screen',
             respawn=True,
             respawn_delay=2.0,
             parameters=params['waypoint_follower.yaml'])
    waypoint_follower = SimpleNamespace(node=n, name='waypoint_follower')

    n = Node(package='nav2_velocity_smoother',
             executable='velocity_smoother',
             name='velocity_smoother',
             output='screen',
             respawn=True,
             respawn_delay=2.0,
             parameters=params['velocity_smoother.yaml'],
             remappings=[('cmd_vel', 'cmd_vel_nav'),
                         ('cmd_vel_smoothed', 'cmd_vel')])
    velocity_smoother = SimpleNamespace(node=n, name='velocity_smoother')

    return controller_server, smoother_server, planner_server, behavior_server, bt_navigator, waypoint_follower, velocity_smoother
