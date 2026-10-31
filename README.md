# turtle_avoider

ROS 2 Humble ile yazılmış, turtlesim üzerinde çalışan basit bir duvardan kaçınma node'u.

Kaplumbağa düz ilerler. Duvara yaklaştığında (kenarlara 1.5 birimden az) yerinde haritanın merkezine (5.5, 5.5) döner, yön tutunca ilerler.

## Node mimarisi

![rqt_graph](docs/rqt_graph.png)

| Node | Abone olduğu topic | Yayınladığı topic |
|---|---|---|
| /avoider | /turtle1/pose (turtlesim/msg/Pose) | /turtle1/cmd_vel (geometry_msgs/msg/Twist) |

Kontrol 10 Hz'lik bir zamanlayıcı döngüsünde çalışır: konum okunur, karar verilir, hız komutu yayınlanır. Yön hatası oransal (P) kontrolle düzeltilir.

## Kurulum ve çalıştırma

Ubuntu 22.04 + ROS 2 Humble gerekir.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/feyza-dogmus/turtle_avoider.git turtle_avoider
cd ~/ros2_ws
colcon build --packages-select turtle_avoider
source install/setup.bash
```

İki ayrı terminalde:

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtle_avoider avoider
```

## Geliştirme notları

- İlk sürümde komut yalnızca pose mesajı gelince üretiliyordu. Kaplumbağa durduğu için pose gelmiyor, komut da çıkmıyordu. Kontrol, zamanlayıcıya bağlı bir döngüye taşınarak çözüldü.
- İlk kaçınma mantığı duvar bölgesinde dönerken ileri gittiği için dar ilmeklerde sıkışıyordu. Şimdi önce merkeze dönüyor, yön tutunca ilerliyor.
- Aynı node iki kez çalıştırılınca iki kaynak aynı topic'e yayın yaptı. `ros2 node list` ile tespit edildi.

## Yol haritası

- ROS parametreleri (duvar mesafesi, hız, kazanç)
- Launch dosyası
- TurtleBot3 + Gazebo + LiDAR ile engelden kaçınma

## Not

Kod yazımında yapay zekâdan yardım aldım. Kodu çalıştırıp hataları (pose gelmeyince komutun çıkmaması, iki node çakışması) kendim tespit ettim ve düzelttim.

Yazar: Feyza Doğmuş
