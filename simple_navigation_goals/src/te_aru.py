import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point,Twist
import message_filters
from geometry_msgs.msg import PoseStamped



def aru_listener():
  rospy.init_node('listenner',anonymous=False)
  # sub_info_aru=rospy.Subscriber("/aruco_single/pose",)
  rospy.Subscriber("aruco_single/pose",PoseStamped,aru_callback)
  # aru_listener=message_filters.TimeSynchronizer(sub_info_aru,10)
  # aru_listener.registerCallback(aru_callback)
  rospy.loginfo("Pose has been received")

def aru_callback(data_array):
    velocity=Twist()
    rospy.loginfo("Aru has been received")
    x_distance=data_array.pose.position.x
    z_distance=data_array.pose.position.z

    #define a client for to send goal requests to the move_base server through a SimpleActionClient
    # ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

    # #wait for the action server to come up
    # while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
    #   rospy.loginfo("Waiting for the move_base action server to come up")
    goal = MoveBaseGoal()

    #set up the frame parameters
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    if x_distance>0.1:
      velocity.linear.x = 0.04
      velocity.angular.z = -0.3
    elif x_distance<-0.1:
      velocity.linear.x = 0.04
      velocity.angular.z = 0.3
    elif z_distance>0.5:
      velocity.linear.x = 0.04
      velocity.angular.z = 0
    elif z_distance<=0.2 and z_distance>0.05:
      velocity.linear.x = 0
      velocity.angular.z = 0
    else:
      velocity.linear.x = 0
      velocity.angular.z = 0

if __name__ == '__main__':
  aru_listener()
  rospy.spin()