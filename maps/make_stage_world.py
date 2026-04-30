#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import cv2
import yaml


def load_map_yaml_data(map_yaml_path):
    try:
        with open(map_yaml_path, 'r') as f:
            map_data = yaml.safe_load(f)

        origin = map_data.get('origin')
        if origin is None:
            print('Error: "origin" key not found in map YAML file - %s' %
                  map_yaml_path)
            sys.exit(1)
        if not isinstance(origin, list) or len(origin) != 3:
            print('Error: "origin" in map YAML is not a list of 3 values - %s' % origin)
            sys.exit(1)

        resolution = map_data.get('resolution')
        if resolution is None:
            print('Error: "resolution" key not found in map YAML file - %s' %
                  map_yaml_path)
            sys.exit(1)
        if not isinstance(resolution, (int, float)):
            print('Error: "resolution" in map YAML is not a number - %s' %
                  resolution)
            sys.exit(1)

        return {
            'origin': tuple(map(float, origin)),
            'resolution': float(resolution)
        }

    except FileNotFoundError:
        print('Error: Map YAML file not found - %s' % map_yaml_path)
        sys.exit(1)
    except yaml.YAMLError as e:
        print('Error: Failed to parse map YAML file - %s' % e)
        sys.exit(1)
    except Exception as e:
        print('Error: An issue occurred while loading map YAML data - %s' % e)
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print('Usage: python %s <map_yaml_path>' % sys.argv[0])
        print('Example: python %s map.yaml' % sys.argv[0])
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_map_yaml_path = sys.argv[1]
    map_dir = os.path.dirname(os.path.abspath(input_map_yaml_path))
    map_basename = os.path.basename(input_map_yaml_path)

    MAP_NAME = os.path.splitext(map_basename)[0]
    MAP_YAML = os.path.join(map_dir, map_basename)
    MAP_PNG = os.path.join(map_dir, "%s_border.png" % MAP_NAME)
    MAP_RELATIVE = "%s_border.png" % MAP_NAME
    SIMULATION_WORLD = os.path.join(map_dir, "%s.world" % MAP_NAME)
    TEMPLATE_FILE = os.path.join(script_dir, 'world.template')

    if not os.path.exists(MAP_PNG):
        print(
            'Error: Bordered image %s not found. Please run add_border.py first.' % MAP_PNG)
        sys.exit(1)
    print('Using bordered image: %s' % MAP_PNG)

    try:
        img = cv2.imread(MAP_PNG)
        if img is None:
            raise ValueError(
                'Could not read bordered PNG image for dimensions. Check if the file is valid and exists.')
        IMG_HEIGHT, IMG_WIDTH = img.shape[:2]
    except Exception as e:
        print('Error: Failed to get image dimensions from %s - %s' % (MAP_PNG, e))
        sys.exit(1)

    map_data = load_map_yaml_data(MAP_YAML)

    MAP_RESOLUTION = map_data['resolution']
    MAP_WIDTH = IMG_WIDTH * MAP_RESOLUTION
    MAP_HEIGHT = IMG_HEIGHT * MAP_RESOLUTION

    ORIGIN_XYZ = map_data['origin']
    OX = ORIGIN_XYZ[0]
    OY = ORIGIN_XYZ[1]
    OZ = ORIGIN_XYZ[2]

    CX = MAP_WIDTH / 2 + OX
    CY = MAP_HEIGHT / 2 + OY

    CX_formatted = '%.2f' % CX
    CY_formatted = '%.2f' % CY

    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template_content = f.read()

        world_content = template_content.format(
            MAP_PNG=MAP_RELATIVE,
            MAP_WIDTH=MAP_WIDTH,
            MAP_HEIGHT=MAP_HEIGHT,
            CX=CX_formatted,
            CY=CY_formatted
        )

        with open(SIMULATION_WORLD, 'w') as f:
            f.write(world_content)
        print('Generated simulation world file: %s' % SIMULATION_WORLD)

    except FileNotFoundError:
        print('Error: Template file %s not found.' % TEMPLATE_FILE)
        sys.exit(1)
    except Exception as e:
        print('Error: Failed to generate simulation world file - %s' % e)
        sys.exit(1)


if __name__ == '__main__':
    main()
