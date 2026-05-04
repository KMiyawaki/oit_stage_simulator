#!/usr/bin/env python3
import math
import os

import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.node import Node
from tf_transformations import euler_from_quaternion


class AmclPoseSub(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self.pose_callback, 10)

        self.get_logger().info('AMCL Pose Subscriber has been started.')

    def pose_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion((q.x, q.y, q.z, q.w))
        degree = math.degrees(yaw)

        self.get_logger().info(
            f'Pose: x={x:.3f}, y={y:.3f}, theta={yaw:.3f} rad ({degree:.1f} deg)')


def main(args=None):
    rclpy.init(args=args)
    script_name = os.path.basename(__file__)
    node_name = os.path.splitext(script_name)[0]
    node = AmclPoseSub(node_name)
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
