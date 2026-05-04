#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import time

from oit_stage_simulator.launch_utils import PackagePath


def main(launch):
    pkg_path = PackagePath()
    search_target = pkg_path.maps + '/**/*.yaml'
    map_data = glob.glob(search_target, recursive=True)
    if not map_data:
        wait = 3
        print('マップがありません。%d秒後に画面を閉じます。' % wait)
        time.sleep(wait)
        return
    for i, m in enumerate(map_data):
        map_data[i] = m.replace(pkg_path.maps + '/', '').replace('.yaml', '')
    map_data.sort(reverse=True)
    for i, m in enumerate(map_data):
        print("[%2d] %s" % (i, m))
    idx = 0
    if len(map_data) > 1:
        print('マップ番号を 0 -- %d で入力してください。それ以外の番号でキャンセルします' %
              (len(map_data) - 1))
        idx = int(input('番号？ > '))
        if idx < 0 or len(map_data) <= idx:
            return
    command = 'ros2 launch %s %s map:=%s' % (
        pkg_path.package_name, launch, map_data[idx])
    os.system(command)


if __name__ == '__main__':
    main('stage_navigation.launch.py')
