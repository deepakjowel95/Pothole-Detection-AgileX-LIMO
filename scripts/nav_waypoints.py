from geometry_msgs.msg import Pose, PoseStamped, Quaternion
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.duration import Duration
from tf_transformations import quaternion_from_euler

"""
Basic navigation demo to go to pose.
"""

def pose_from_xytheta(x, y, theta):
    # negative theta: turn clockwise
    pose = Pose()
    pose.position.x = x
    pose.position.y = y
    q = quaternion_from_euler(0, 0, theta)
    pose.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])
    return pose
    
def main():
    rclpy.init()

    navigator = BasicNavigator()

    '''# Set our demo's initial pose (0,0,0)
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose = pose_from_xytheta(0.0, 0.0, 0.0)
    navigator.setInitialPose(initial_pose)'''

    # Wait for navigation to fully activate, since autostarting nav2
    navigator.waitUntilNav2Active()
    
    goal_poses=[]

    # Go to our demos first goal pose_A
    goal_pose_A= PoseStamped()
    goal_pose_A.header.frame_id = 'map'
    goal_pose_A.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_A.pose = pose_from_xytheta(1.50 0.0, 0.0)
    goal_poses.append(goal_pose_A)
    
    '''# Go to our demos goal_pose_AB
    goal_pose_AB = PoseStamped()
    goal_pose_AB.header.frame_id = 'map'
    goal_pose_AB.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_AB.pose = pose_from_xytheta(1.09, -0.45, 0.0)
    goal_poses.append(goal_pose_AB)'''
    
    
    # Go to our demos first goal pose_B
    goal_pose_B = PoseStamped()
    goal_pose_B.header.frame_id = 'map'
    goal_pose_B.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_B.pose = pose_from_xytheta(0.915, -0.77, 0.0)
    goal_poses.append(goal_pose_B)
    
    '''# Go to our demos first goal pose_BC
    goal_pose_BC = PoseStamped()
    goal_pose_BC.header.frame_id = 'map'
    goal_pose_BC.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_BC.pose = pose_from_xytheta(0.55, -0.77, 0.0)
    goal_poses.append(goal_pose_BC)'''
    
    
    # Go to our demos first goal pose_C
    goal_pose_C = PoseStamped()
    goal_pose_C.header.frame_id = 'map'
    goal_pose_C.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_C.pose = pose_from_xytheta(-0.18, -0.9, 0.0)
    goal_poses.append(goal_pose_C)
    
    # Go to our demos first goal pose_D
    goal_pose_D = PoseStamped()
    goal_pose_D.header.frame_id = 'map'
    goal_pose_D.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_D.pose = pose_from_xytheta(-0.3, -0.2, 0.0)
    goal_poses.append(goal_pose_D)
    
    # Go to our demos first goal pose_E
    goal_pose_E = PoseStamped()
    goal_pose_E.header.frame_id = 'map'
    goal_pose_E.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_E.pose = pose_from_xytheta(-0.9, -0.03, 0.0)
    goal_poses.append(goal_pose_E)
    
    # Go to our demos first goal pose_F
    goal_pose_F = PoseStamped()
    goal_pose_F.header.frame_id = 'map'
    goal_pose_F.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_F.pose = pose_from_xytheta(-0.9, -0.9, 0.0)
    goal_poses.append(goal_pose_F)
    
    # Go to our demos first goal pose_G
    goal_pose_G = PoseStamped()
    goal_pose_G.header.frame_id = 'map'
    goal_pose_G.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_G.pose = pose_from_xytheta(-0.1, -0.2, 0.0)
    goal_poses.append(goal_pose_G)
    
    ''''# Go to our demos first goal pose_Initial
    goal_pose_Home = PoseStamped()
    goal_pose_Home.header.frame_id = 'map'
    goal_pose_Home.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose_Home.pose = spin(spin_dist=1.57,time_allowance=10)
    goal_poses.append(goal_pose_Home)'''''

    

    
    