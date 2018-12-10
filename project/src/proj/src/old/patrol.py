import rospy
import numpy as np
from geometry_msgs.msg import Twist
from tf2_msgs.msg import TFMessage



# Pseudo code for overall patrolling movement:
# move left 2 feet (patrol_left)
# turn 30 degrees (patrol_spin)
# scan (figure out how to make it stop and scan/theshold)
# repeat 27 times (patrol_spin)
# if no tag found
# back to center (patrol_right)

# patrol_message = TFMessage()

# def patrol_callback(message):
#   patrol_message = message

# sub = rospy.Subscriber("/tf_static", TFMessage, callback)



# If no AR tagh visible, this function is called to move the turtlebot 
# negative x by 0.6096 (left by 2 feet). 
def patrol_left():
  command = Twist()
  command.linear.x = 0.6096
  command.linear.y = 0
  command.linear.z = 0
  command.angular.x = 0
  command.angular.y = 0
  command.angular.z = 8*np.pi
  return command

# If no AR tagh visible, this function is called to move the turtlebot 
# positive x by 0.6096 (right by 2 feet). 

def patrol_right():
  command = Twist()
  command.linear.x = 0.6096 
  command.linear.y = 0
  command.linear.z = 0
  command.angular.x = 0
  command.angular.y = 0
  command.angular.z = -np.pi/2
  return command

# If no AR tagh visible, this function is called to rotate the turtlebot by 30 degrees. 
# (When this function is called the expectation is that it will be called repeatedly 
# until the bot moves through 2 complete rotations)

def patrol_spin():
  command = Twist()
  #command.linear.x = 0 
  command.linear.x = 0.15
  command.linear.y = 0
  command.linear.z = 0
  command.angular.x = 0
  command.angular.y = 0
  #command.angular.z = np.pi/6
  command.angular.z = np.pi/2
  return command
