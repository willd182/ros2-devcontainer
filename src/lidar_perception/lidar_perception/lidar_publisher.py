import rclpy
from rclpy.node import Node

from std_msgs.msg import Header
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2


class PointCloudPublisher(Node):
    def __init__(self):
        super().__init__('pointcloud_publisher')

        self.pub = self.create_publisher(PointCloud2, '/points', 10)

        self.timer = self.create_timer(1.0, self.publish_cloud)

        self.get_logger().info("PointCloud2 publisher started")

    def publish_cloud(self):
        # -----------------------------
        # 1. Create valid ROS Header
        # -----------------------------
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = "map"

        # -----------------------------
        # 2. Create simple point cloud
        # -----------------------------
        points = [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
            (1.0, 0.5, 0.5),
        ]

        # -----------------------------
        # 3. Convert to PointCloud2
        # -----------------------------
        msg = pc2.create_cloud_xyz32(header, points)

        # -----------------------------
        # 4. Publish
        # -----------------------------
        self.pub.publish(msg)

        self.get_logger().info("Published PointCloud2")


def main(args=None):
    rclpy.init(args=args)

    node = PointCloudPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()