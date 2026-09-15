#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class laser_Scan(Node):

	def __init__(self):
		super().__init__('ls')
		self.subscriber= self.create_subscriber('sensor_msgs/msg/LaserScan', LaserScan, callback)

		
			
	def callback(self):
		msg = Laser_Scan()		
		self.subscriber_.subscriber(msg)
		self.get_logger().info('Scan_data: "%s"' % msg)
			
			
def main(arg=None):
	rclpy.init(args=args)
	ls = laser_Scan()
	rclpy.spin(ls)

if __name__ == '__main__':
	main()
