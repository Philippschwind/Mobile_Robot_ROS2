
import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class TurtleSquare(Node):

    def __init__(self):
        super().__init__('turtle_square')

        self.publisher = self.create_publisher(
                Twist, '/turtle1/cmd_vel', 10
            )

        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose',
            self.pose_callback, 10
        )

        self.timer = self.create_timer(
            0.05, self.control_loop
        )

        self.pose = None

        self.state = 'MOVE'
        self.start_position = None
        self.target_angle = None
        self.completed_sides = 0

        self.side_length = 2.0
        self.linear_speed = 1.0
        self.angular_speed = 1.0

    def pose_callback(self, msg):
        self.pose = msg

    def control_loop(self):
        if self.pose is None:
            return

        cmd = Twist()

        if self.state == 'MOVE':
            if self.start_position is None:
                self.start_position = (
                    self.pose.x, self.pose.y
                )

            dx = self.pose.x - self.start_position[0]
            dy = self.pose.y - self.start_position[1]
            distance = math.hypot(dx, dy)

            if distance < self.side_length:
                cmd.linear.x = self.linear_speed
            else:
                cmd.linear.x = 0.0
                self.state = 'TURN'
                self.target_angle = self.pose.theta + math.pi / 2
                if self.target_angle > math.pi:
                    self.target_angle -= 2 * math.pi

        elif self.state == 'TURN':
            error = math.atan2(
                math.sin(self.target_angle - self.pose.theta),
                math.cos(self.target_angle - self.pose.theta)
            )

            if abs(error) > 0.02:
                cmd.angular.z = (
                    self.angular_speed if error > 0
                    else -self.angular_speed
                )
            else:
                self.completed_sides += 1
                self.start_position = None

                if self.completed_sides >= 4:
                    self.state = 'DONE'
                    self.get_logger().info(
                        'Square completed!'
                    )
                else:
                    self.state = 'MOVE'

        self.publisher.publish(cmd)

    def destroy_node(self):
        self.publisher.publish(Twist())
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSquare()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()