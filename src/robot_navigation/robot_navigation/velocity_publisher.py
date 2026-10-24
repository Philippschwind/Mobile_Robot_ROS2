
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityPublisher(Node):

    def __init__(self):
        super().__init__('velocity_publisher')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.5,
            self.publish_velocity
        )

        self.get_logger().info('Velocity Publisher started')

    def publish_velocity(self):
        msg = Twist()

        # Forward movement: 0.2 m/s
        msg.linear.x = 0.2

        # No rotation
        msg.angular.z = 0.0

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Publishing velocity: {msg.linear.x} m/s'
        )


def main(args=None):
    rclpy.init(args=args)

    node = VelocityPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
