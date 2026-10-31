from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Simulasyon penceresi
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen',
        ),
        # Hareketli engel: turtle2'yi olusturur ve dondurur
        Node(
            package='turtle_avoider',
            executable='wanderer',
            name='wanderer',
            output='screen',
        ),
        # Kacinan node: parametreler buradan verilir
        Node(
            package='turtle_avoider',
            executable='avoider',
            name='avoider',
            output='screen',
            parameters=[{
                'wall_margin': 1.5,
                'obstacle_distance': 2.0,
                'cruise_speed': 2.0,
                'turn_gain': 3.0,
            }],
        ),
    ])
