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
from geometry_msgs.msg import Twist

#Define the method which contains the main functionality of the node.
def controller(bot_frame, ar_frame):
  """
  Controls a turtlebot whose position is denoted by turtlebot_frame,
  to go to a position denoted by target_frame

  Inputs:
  - turtlebot_frame: the tf frame of the AR tag on your turtlebot
  - target_frame: the tf frame of the target AR tag
  """

  ################################### YOUR CODE HERE ##############

  #Create a publisher and a tf buffer, which is primed with a tf listener
  pub = rospy.Publisher("/mobile_base/commands/velocity" , Twist, queue_size=10)
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)
  
  # Create a timer object that will sleep long enough to result in
  # a 10Hz publishing rate
  r = rospy.Rate(10) # 10hz
  
  # Controller Constants
  K1 = 0.3
  K2 = 1

  world_frame = "odom"
  transWorldAR = tfBuffer.lookup_transform(world_frame, ar_frame, rospy.Time(0), rospy.Duration(4.0))
  WAr_X = transWorldAR.transform.translation.x
  WAr_Y = transWorldAR.transform.translation.y
  WAr_Z = transWorldAR.transform.translation.z

  isObstacle = False
  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():
    try:
      #canTrans = tfBuffer.can_transform(bot_frame, goal_frame, rospy.Time(0), rospy.Duration(4.0))
      transBotAR = tfBuffer.lookup_transform(bot_frame, ar_frame, rospy.Time(0), rospy.Duration(4.0))
      BAr_X = transBotAR.transform.translation.x
      BAr_Y = transBotAR.transform.translation.y
      BAr_Z = transBotAR.transform.translation.z

      control_command = Twist()


      #if (canTrans == True)
      # Check if there is an obstacle in your straight path to the AR Tag (Can use laser scan ideas from labs)
      #if (isObstacle == True):

        # Want to avoid the obstacle by using laser scan data
        # AR Tag's location with respect to the odom has been saved earlier

        #Find dimension of the obstacle 
          #Options
            # When an obstacle is in front of the bot
              #1. Create a temp map of the immediate area?
              #2. Detect edges of the obstacle and pick the farthest obstacle-free point dynamically 



        # Pre plan a set of steps to avoid it 

      # If there is no obstacle, go to AR
      if (isObstacle == False):
        if (BAr_X > 0.55):
          print("Heading to AR Tag:")
          next_x = K1*BAr_X
          next_theta = K2*BAr_Y

          control_command.linear.x = next_x  
          control_command.linear.y = 0
          control_command.linear.z = 0
          control_command.angular.x = 0
          control_command.angular.y = 0
          control_command.angular.z = next_theta
          pub.publish(control_command)



        
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
      print e
      pass
    # Use our rate object to sleep until it is time to publish again
    r.sleep()

      
# # This is Python's sytax for a main() method, which is run by default
# # when exectued in the shell
# if __name__ == '__main__':
#   # Check if the node has received a signal to shut down
#   # If not, run the talker method

#   #Run this program as a new node in the ROS computation graph 
#   #called /turtlebot_controller.
#   rospy.init_node('turtlebot_controller', anonymous=True)

#   try:
#     controller(sys.argv[1], sys.argv[2])
#   except rospy.ROSInterruptException:
#     pass
