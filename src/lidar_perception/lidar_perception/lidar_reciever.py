#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2

from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class PointCloudListener(Node):
	def __init__(self):
		super().__init__("lidar_receiver")

		qos = QoSProfile(
			reliability=QoSReliabilityPolicy.RELIABLE,
			history=QoSHistoryPolicy.KEEP_LAST,
			depth=1
		)

		self.subscription = self.create_subscription(
			PointCloud2,
			'/points',
			self.pointcloud_callback,
			qos
			)
		
		self.get_logger().info("Starting lidar reciever node!")
	
	def pointcloud_callback(self, msg: PointCloud2):
		points = pc2.read_points(msg, field_names=("x","y","z"), skip_nans=True)
		
		count = 0

		for p in points:
			count += 1

		ts = msg.header.stamp.sec
		self.get_logger().info(f"Received point cloud with {count} points at t={ts}")

def main(args=None):
	rclpy.init(args=args)
	node = PointCloudListener()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()