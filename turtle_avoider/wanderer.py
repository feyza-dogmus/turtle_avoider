import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn


class Wanderer(Node):
    """Ikinci kaplumbagayi (turtle2) olusturur ve surekli daire cizdirir.

    Avoider icin hareketli bir engel gorevi gorur.
    """

    def __init__(self):
        super().__init__('wanderer')
        self.declare_parameter('linear_speed', 1.5)
        self.declare_parameter('angular_speed', 0.8)

        self.pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.ready = False

        # Turtlesim servisi hazir olana kadar bekle (bloklamadan)
        self.spawn_timer = self.create_timer(0.5, self.try_spawn)
        self.move_timer = self.create_timer(0.1, self.move)

    def try_spawn(self):
        if not self.spawn_client.service_is_ready():
            self.get_logger().info('/spawn servisi bekleniyor...', throttle_duration_sec=2.0)
            return
        self.spawn_timer.cancel()
        req = Spawn.Request()
        req.x = 8.0
        req.y = 3.0
        req.theta = 0.0
        req.name = 'turtle2'
        future = self.spawn_client.call_async(req)
        future.add_done_callback(self.spawn_done)

    def spawn_done(self, future):
        try:
            result = future.result()
            self.get_logger().info(f'{result.name} olusturuldu')
        except Exception as e:
            # turtle2 zaten varsa (turtlesim yeniden baslatilmadiysa) devam et
            self.get_logger().warn(f'Spawn basarisiz, mevcut turtle2 kullanilacak: {e}')
        self.ready = True

    def move(self):
        if not self.ready:
            return
        msg = Twist()
        msg.linear.x = self.get_parameter('linear_speed').value
        msg.angular.z = self.get_parameter('angular_speed').value
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = Wanderer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
