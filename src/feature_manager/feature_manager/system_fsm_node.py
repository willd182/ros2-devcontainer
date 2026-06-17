import rclpy
from rclpy.node import Node
from std_msgs.msg import String  

from common_interfaces.msg import CruiseRequest
from feature_manager.CACC_StateMachine import StateMachineForCACC 


class SystemFSMNode(Node):
    def __init__(self):
        super().__init__('SystemFSMNode')

        # FSM
        self.fsm = StateMachineForCACC()

        # Subscriber
        self.create_subscription(
            CruiseRequest,
            '/cruise_request',
            self.cruise_callback,
            10
        )

        # Publisher (debug / state broadcast)
        self.state_pub = self.create_publisher(String, '/cacc_state', 10)

        # Fixed-rate timer (FSM tick)
        self.timer_period = 0.1  # 20 Hz
        self.timer = self.create_timer(self.timer_period, self.tick)

        self.get_logger().info("CACC Node initialized")

    def cruise_callback(self, msg: CruiseRequest):
        """ Convert ROS message to FSM events """
        self.fsm.update_fields_with_cruise_request(msg)

    def tick(self):
        """
        Fixed-rate execution:

        1. Step FSM
        2. Publish state
        3. Reset event consumption handled inside FSM
        """
        self.fsm.step()

        # Publish state for debugging / integration
        msg = String()
        msg.data = self.fsm.state.name
        self.state_pub.publish(msg)

        self.get_logger().debug(f"FSM State: {self.fsm.state.name}")


def main(args=None):
    rclpy.init(args=args)
    node = SystemFSMNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()