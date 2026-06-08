#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2

class PointCloudListener(Node):
	def __init__(self):
		super().__init__("lidar_receiver")

		self.subscription = self.create_subscription(
			PointCloud2,
			'/points',
			self.pointcloud_callback,
			10
			)
		
		self.get_logger().info("Starting lidar reciever node!")
	
	def pointcloud_callback(self, msg: PointCloud2):
		points = pc2.read_points(msg, field_names=("x","y","z"), skip_nans=True)
		
		count = 0
		for p in points:
			count += 1
		
		self.get_logger().info(f"Received point cloud with {count} points")

def main(args=None):
	rclpy.init(args=args)
	node = PointCloudListener()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()