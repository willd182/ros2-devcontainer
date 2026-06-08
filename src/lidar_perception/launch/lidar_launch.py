from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    publisher_node = Node(
        package='lidar_perception',
        executable='lidar_publisher',
        name='pointcloud_publisher',
        output='screen'
    )

    subscriber_node = Node(
        package='lidar_perception',
        executable='lidar_listener',
        name='pointcloud_listener',
        output='screen'
    )

    return LaunchDescription([
        publisher_node,
        subscriber_node
    ])