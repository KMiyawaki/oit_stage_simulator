import os
from types import SimpleNamespace

from ament_index_python.packages import get_package_share_directory

from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


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
