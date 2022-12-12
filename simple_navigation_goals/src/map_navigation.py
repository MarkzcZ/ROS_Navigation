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



class map_navigation():
  def choose(self):
    choice='q'

    rospy.loginfo("|-------------------------------|")
    rospy.loginfo("|PRESSE A KEY:")
    rospy.loginfo("|'0': Cafe ")
    rospy.loginfo("|'1': Office 1 ")
    rospy.loginfo("|'2': Office 2 ")
    rospy.loginfo("|'3': Office 3 ")
    rospy.loginfo("|'q': Quit ")
    rospy.loginfo("|-------------------------------|")
    rospy.loginfo("|WHERE TO GO?")
    choice = input()
    return choice


  def __init__(self):
    # declare the coordinates of interest
    self.xCafe = -0.287
    self.yCafe = 0.8043
    self.xOffice1 = 2.6204
    self.yOffice1 = -2.2366
    self.xOffice2 = -3.28
    self.yOffice2 = -1.86
    self.xOffice3 = -0.5520
    self.yOffice3 = -4.9448

    self.parkpointx=1.835
    self.parkpointy=-1.866
    self.goalReached = False
    # initiliaze
    rospy.init_node('map_navigation', anonymous=False)
    
    choice = self.choose()

    if (choice == 0):
      self.goalReached = self.moveToGoal(self.xCafe, self.yCafe)

    elif (choice == 1):

      self.goalReached = self.moveToGoal(self.xOffice1, self.yOffice1)

    elif (choice == 2):

      self.goalReached = self.moveToGoal(self.xOffice2, self.yOffice2)

    elif (choice == 3):

      self.goalReached = self.moveToGoal(self.xOffice3, self.yOffice3)

    elif (choice==4):
      self.goalReached = self.moveToGoal(self.parkpointx, self.parkpointy)

      

    if (choice!='q'):

      if (self.goalReached):
        rospy.loginfo("Congratulations!")
        rospy.spin()
      else:
        rospy.loginfo("Hard Luck!")


    while choice != 'q':
      choice = self.choose()
      if (choice == 0):
        self.goalReached = self.moveToGoal(self.xCafe, self.yCafe)

      elif (choice == 1):
        self.goalReached = self.moveToGoal(self.xOffice1, self.yOffice1)

      elif (choice == 2):

        self.goalReached = self.moveToGoal(self.xOffice2, self.yOffice2)

      elif (choice == 3):

        self.goalReached = self.moveToGoal(self.xOffice3, self.yOffice3)

      elif (choice==4):
        # spin and scan
        self.goalReached = self.moveToGoal(self.parkpointx, self.parkpointy)
        aru_listener()


      if (choice!='q'):

        if (self.goalReached):
          rospy.loginfo("Congratulations!")
          rospy.spin()
          # rospy.spin()


        else:
          rospy.loginfo("Hard Luck!")
    


  def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Quit program")
        rospy.sleep()

  def moveToGoal(self,xGoal,yGoal):

      #define a client for to send goal requests to the move_base server through a SimpleActionClient
      ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

      #wait for the action server to come up
      while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
              rospy.loginfo("Waiting for the move_base action server to come up")
      goal = MoveBaseGoal()

      #set up the frame parameters
      goal.target_pose.header.frame_id = "map"
      goal.target_pose.header.stamp = rospy.Time.now()

      # moving towards the goal*/

      goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
      goal.target_pose.pose.orientation.x = 0.0
      goal.target_pose.pose.orientation.y = 0.0
      goal.target_pose.pose.orientation.z = 0.0
      goal.target_pose.pose.orientation.w = 1.0

      rospy.loginfo("Sending goal location ...")
      ac.send_goal(goal)

      ac.wait_for_result(rospy.Duration(60))

      if(ac.get_state() ==  GoalStatus.SUCCEEDED):
              rospy.loginfo("You have reached the destination")
              return True

      else:
              rospy.loginfo("The robot failed to reach the destination")
              return False


if __name__ == '__main__':
    try:
      rospy.loginfo("You have reached the destination")
      map_navigation()
      rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("map_navigation node terminated.")
