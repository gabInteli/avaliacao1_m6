import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose as TPose
from Queue import Queue
from collections import deque
import time
import math

#Definição da variável que possui todos os pontos pelos quais a tartaruga deve passar 
points = [0.0, 0.5],[0.5, 0.0],[0.0, 0.5],[0.5, 0.0],[0.0, 1.0],[1.0, 0.0]
MAX_DIFF = 0.1

class Pose(TPose):
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        super().__init__(x=x, y=y, theta=theta)
        
    def __repr__(self):
        return f"(x={self.x:.2f}, theta={self.y:.2f})"
    
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __eq__(self, other):
        return abs(self.x - other.x) < MAX_DIFF \
        and abs(self.y - other.y) < MAX_DIFF \

class MissionControl(deque):
    def __init__(self, points):
        super().__init__()
        for i in range(0,5):
            new_pose = Pose()
            new_pose.x, new_pose.y = points[i]
            self.enqueue(new_pose)

    def enqueue(self, x):
        super().append(x)
    
    def dequeue(self):
        return super().popleft()

class TurtleController(Node):
    def __init__(self, mission_control, control_period=0.02):
        super().__init__('turtle_controller')
        self.pose = Pose(x=-40.0)
        self.setpoint = Pose(x=-40.0)
        self.mission_control = mission_control
        self.publisher = self.create_publisher(
            msg_type=Twist,
            topic="/turtle1/cmd_vel",
            qos_profile=10
        )
        self.subscription = self.create_subscription(
            msg_type=Pose,
            topic="/turtle1/pose",
            callback=self.pose_callback,
            qos_profile=10
        )
        self.control_timer = self.create_timer(
                timer_period_sec=control_period,
                callback=self.control_callback
        )

    def control_callback(self):
        if self.pose.x == -40.0:
            self.get_logger().info("Aguardando primeira pose...")
            return
        msg = Twist()
        x_diff = self.setpoint.x - self.pose.x
        y_diff = self.setpoint.y - self.pose.y
        if self.pose == self.setpoint:
            msg.linear.x, msg.linear.y = 0.0, 0.0
            self.update_setpoint()
        if abs(y_diff) > MAX_DIFF:
            msg.linear.y = 0.5 if y_diff > 0 else -0.5
        else:
            msg.linear.y = 0.0
        if abs(x_diff) > MAX_DIFF:
            msg.linear.x = 0.5 if x_diff > 0 else -0.5
        else:
            msg.linear.x = 0.0
        self.publisher.publish(msg)
        
    def update_setpoint(self):
        try:
            self.setpoint = self.pose + self.mission_control.dequeue()
            self.get_logger().info(f"A tartaruga chegou em {self.pose}, \
                                   andando para {self.setpoint}")
        except IndexError:
            self.get_logger().info(f"Fim da jornada!")
            exit()

    def pose_callback(self, msg):
        self.pose = Pose(x=msg.x, y=msg.y, theta=msg.theta)
        if self.setpoint.x == -40.0:
            self.update_setpoint()


def main(args=None):
    rclpy.init(args=args)
    mc = MissionControl(points)
    tc = TurtleController(mc)
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()