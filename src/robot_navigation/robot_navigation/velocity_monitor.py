
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityMonitor(Node):

    def __init__(self):
        super().__init__('velocity_monitor')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.velocity_callback,
            10
        )

        self.get_logger().info('Velocity Monitor started')

    def velocity_callback(self, msg):
        self.get_logger().info(
            f'Linear X: {msg.linear.x:.2f} m/s | '
            f'Angular Z: {msg.angular.z:.2f} rad/s'
        )


def main(args=None):
    rclpy.init(args=args)

    node = VelocityMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
