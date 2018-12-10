#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the rospy package. For an import to work, it must be specified
#in both the package manifest AND the Python file in which it is used.
import rospy
import tf2_ros
import sys
import patrol
import instructions
from geometry_msgs.msg import Twist



# Performs the calculations needed to have the turtlebot approach the AR Tag if it is seen
# If there is no AR Tag, the turtlebot stops. 
# Inputs:
# - turtlebot_frame: the tf frame of the AR tag on your turtlebot
# - target_frame: the tf frame of the target AR tag
# - trans: instance of the lookup transform 

def control_twist(turtlebot_frame, goal_frame, trans):
    # P-Constants 
    K1 = 0.3
    K2 = 1
    # D-Constants 
    control_command = Twist()
    x = trans.transform.translation.x
    y = trans.transform.translation.y
    z = trans.transform.translation.z
    # 0.55 is when the 17.0 cm AR Tag is flush with the floor
    # NEED TO CHANGE once height determined
    if (x > 0.55):
        #print(x)
        next_x = K1*x
        next_theta = K2*y
        control_command.linear.x = next_x  
        control_command.linear.y = 0
        control_command.linear.z = 0
        control_command.angular.x = 0
        control_command.angular.y = 0
        control_command.angular.z = next_theta
    return control_command


#Method which contains the main functionality of the node.
def controller(turtlebot_frame, goal_frame):
  """
  Controls a turtlebot whose position is denoted by turtlebot_frame,
  to go to a position denoted by target_frame

  Inputs:
  - turtlebot_frame: the tf frame of the AR tag on your turtlebot
  - target_frame: the tf frame of the target AR tag
  """
  #Create a publisher and a tf buffer, which is primed with a tf listener
  pub = rospy.Publisher("/mobile_base/commands/velocity" , Twist, queue_size=10)
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)
  

  hasCheckedLeft = False
  hasCheckedRight = False
  hasRotated = 0

  # Create a timer object that will sleep long enough to result in
  # a 10Hz publishing rate
  r = rospy.Rate(20) # 10hz
  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():

    canTrans = tfBuffer.can_transform(turtlebot_frame, goal_frame, rospy.Time.now(), rospy.Duration(0.4))
    print(canTrans)
    control_command = Twist()
    if(canTrans == 1):
      try:
        trans = tfBuffer.lookup_transform(turtlebot_frame, goal_frame, rospy.Time.now(), rospy.Duration(0.4))
        control_command = control_twist(turtlebot_frame, goal_frame, trans)
        # Process trans to get your state error
        # Generate a control command to send to the robot
      except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
        print e
        pass
    else:
      if(hasCheckedLeft == False):
        control_command = patrol.patrol_left()
        pub.publish(control_command)
        hasCheckedLeft = True

      if (hasRotated == 2 & hasCheckedLeft):
        control_command = patrol.patrol_right()
        pub.publish(control_command)
        control_command = patrol.patrol_right()
        pub.publish(control_command)
        hasCheckedRight = True
        hasRotated = 0

      if(hasRotated != 2):
        control_command = patrol.patrol_spin()
        hasRotated = hasRotated + 1
        pub.publish(control_command)

      if(hasCheckedRight & hasCheckedLeft & hasRotated == 2):
        control_command = patrol.patrol_left()
        pub.publish(control_command)
        #requestNew()


          
    # Use our rate object to sleep until it is time to publish again
    pub.publish(control_command)
    r.sleep()

      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  #Run this program as a new node in the ROS computation graph 
  #called /turtlebot_controller.
  rospy.init_node('turtlebot_controller', anonymous=True)
  try:
    controller(sys.argv[1], sys.argv[2])
  except rospy.ROSInterruptException:
    pass
