#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import cv2


def add_border_to_image(input_file_path, border_size=5, border_color=(0, 0, 0)):
    if not os.path.exists(input_file_path):
        print("Error: Input file not found - %s" % input_file_path)
        return None

    try:
        img = cv2.imread(input_file_path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(
                "Could not read image. File might be corrupted or unsupported format.")
    except Exception as e:
        print("Error: An issue occurred while reading the image - %s" % e)
        return None

    bordered_img = cv2.copyMakeBorder(
        img,
        border_size,
        border_size,
        border_size,
        border_size,
        cv2.BORDER_CONSTANT,
        value=border_color
    )

    base_name = os.path.splitext(input_file_path)[0]
    output_file_path = "%s_border.png" % base_name

    try:
        cv2.imwrite(output_file_path, bordered_img)
        print("Bordered image saved: %s" % output_file_path)
        return output_file_path
    except Exception as e:
        print("Error: An issue occurred while saving the image - %s" % e)
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python %s <input_file_path>" % sys.argv[0])
        print("Example: python %s input.jpg" % sys.argv[0])
        sys.exit(1)

    input_file = sys.argv[1]

    border_thickness = 5
    black_color = (0, 0, 0)

    add_border_to_image(input_file, border_thickness, black_color)


if __name__ == "__main__":
    main()
