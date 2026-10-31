import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class Avoider(Node):
    def __init__(self):
        super().__init__('avoider')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_cb, 10)
        self.pose = None
        self.timer = self.create_timer(0.1, self.control_loop)

    def pose_cb(self, pose):
        self.pose = pose

    def control_loop(self):
        if self.pose is None:
            return
        p = self.pose
        msg = Twist()
        near_wall = p.x < 1.5 or p.x > 9.5 or p.y < 1.5 or p.y > 9.5
        if near_wall:
            # Haritanin merkezine (5.5, 5.5) bak
            hedef = math.atan2(5.5 - p.y, 5.5 - p.x)
            fark = math.atan2(math.sin(hedef - p.theta), math.cos(hedef - p.theta))
            msg.angular.z = 3.0 * fark
            msg.linear.x = 0.0 if abs(fark) > 0.5 else 1.0
            self.get_logger().info(f'Duvara yakin! x={p.x:.1f} y={p.y:.1f}, merkeze donuyorum')
        else:
            msg.linear.x = 2.0
            msg.angular.z = 0.0
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = Avoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
