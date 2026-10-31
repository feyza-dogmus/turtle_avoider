import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

MAP_SIZE = 11.0  # turtlesim haritasi yaklasik 11x11 birim


def aci_farki(hedef, mevcut):
    """Iki aci arasindaki farki -pi..pi araligina normalize eder."""
    return math.atan2(math.sin(hedef - mevcut), math.cos(hedef - mevcut))


class Avoider(Node):
    def __init__(self):
        super().__init__('avoider')

        # Parametreler: ros2 param set ile calisirken degistirilebilir
        self.declare_parameter('wall_margin', 1.5)        # duvara bu kadar yaklasinca kac
        self.declare_parameter('obstacle_distance', 2.0)  # diger kaplumbagaya bu kadar yaklasinca kac
        self.declare_parameter('cruise_speed', 2.0)       # duz giderken ileri hiz
        self.declare_parameter('turn_gain', 3.0)          # P kontrol kazanci
        self.declare_parameter('center_x', 5.5)           # duvardan sonra donulecek nokta
        self.declare_parameter('center_y', 5.5)

        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_cb, 10)
        # Engel: ikinci kaplumbaganin konumu
        self.obs_sub = self.create_subscription(Pose, '/turtle2/pose', self.obstacle_cb, 10)
        self.pose = None
        self.obstacle = None
        self.timer = self.create_timer(0.1, self.control_loop)

    def pose_cb(self, pose):
        self.pose = pose

    def obstacle_cb(self, pose):
        self.obstacle = pose

    def control_loop(self):
        if self.pose is None:
            return

        # Parametreleri her dongude okuyoruz, boylece anlik degisiklik etki eder
        margin = self.get_parameter('wall_margin').value
        obs_dist = self.get_parameter('obstacle_distance').value
        speed = self.get_parameter('cruise_speed').value
        gain = self.get_parameter('turn_gain').value
        cx = self.get_parameter('center_x').value
        cy = self.get_parameter('center_y').value

        p = self.pose
        msg = Twist()

        near_wall = (p.x < margin or p.x > MAP_SIZE - margin
                     or p.y < margin or p.y > MAP_SIZE - margin)

        near_obstacle = False
        if self.obstacle is not None:
            dx = p.x - self.obstacle.x
            dy = p.y - self.obstacle.y
            near_obstacle = math.hypot(dx, dy) < obs_dist

        # Oncelik sirasi: 1) duvar  2) diger kaplumbaga  3) duz ilerle
        if near_wall:
            hedef = math.atan2(cy - p.y, cx - p.x)
            fark = aci_farki(hedef, p.theta)
            msg.angular.z = gain * fark
            msg.linear.x = 0.0 if abs(fark) > 0.5 else 1.0
            self.get_logger().info(
                f'Duvara yakin! x={p.x:.1f} y={p.y:.1f}, merkeze donuyorum',
                throttle_duration_sec=1.0)
        elif near_obstacle:
            # Engelden uzaga bak: engele dogru olan dogrultunun tersi
            hedef = math.atan2(dy, dx)
            fark = aci_farki(hedef, p.theta)
            msg.angular.z = gain * fark
            msg.linear.x = 0.0 if abs(fark) > 0.5 else 1.0
            self.get_logger().info(
                f'Engel yakin! mesafe={math.hypot(dx, dy):.1f}, uzaklasiyorum',
                throttle_duration_sec=1.0)
        else:
            msg.linear.x = speed
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
