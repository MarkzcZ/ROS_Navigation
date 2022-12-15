# ROS_Navigation
SUSTECH EE347 group#7 zhanchenzhi#12012505 zhangyuxuan#12012508
## Git Clone
cd ~/catkin_ws/src

git clone git@github.com:MarkzcZ/ROS_Navigation.git

Put the classroom.yaml and classroom.pgm at HOME/.

## Part 1
To navigate the turtlebot3 from point1 to point4 you need to turn up four terminal

roscore

ssh & bringup

roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=￥HOME/classroom.yaml

python map_navigation.py

Then you can input 0/1/2/3 to navigate the turtlebot to the point.

## Part 2
To find the parking place, we set a fourth position near the aruko marker and the robot can trip to the position by entering 4. Robot also will search for the aruco maker. Then method aru_listener() is running to subscribe to "aruco_single/pose" and make the parking decision. Just running belowed command.

roslaunch line_follower_turtlebot aruco_marker_finder.launch

python map_navigation.py

python te_aru.py
