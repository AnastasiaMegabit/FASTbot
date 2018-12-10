#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

#Code is inspired by http://wiki.ros.org/navigation/Tutorials/SendingSimpleGoals (written in C++).
#TurtleBot must have minimal.launch & amcl_demo.launch running prior to starting this script.

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
import tf2_ros
import sys
from geometry_msgs.msg import Twist
import findAR



class GoForwardAvoid():
    # Init method sets the ar frame and bot frame with respect to whom the bot will plan it's path
    def __init__(self, bot_frame, ar_frame):
        #rospy.init_node('nav_test', anonymous=False)
        self.ar_frame = ar_frame
        self.bot_frame = bot_frame
        self.condition = False

	#What to do if shut down (e.g. ctrl + C or failure)
	rospy.on_shutdown(self.shutdown)

	
	#tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("\nWait for the action server to come up")

	#allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

	self.ar_finder = findAR.ARFinder(self.bot_frame, self.ar_frame, self.move_base)

	if (self.ar_finder.findAR()):
		# Based on the ar_frame and bot_frame, 
		print("I am going to find an AR")
		goal = self.getGoal()
		print(goal)
		#start moving
	    	self.move_base.send_goal(goal)

		#allow TurtleBot up to 60 seconds to complete task
		success = self.move_base.wait_for_result(rospy.Duration(60)) 

		if not success:
	                self.move_base.cancel_goal()
	                rospy.loginfo("\nDestination canceled, I don't know why I failed")
	    	else:
			# We made it!
			state = self.move_base.get_state()
			if state == GoalStatus.SUCCEEDED:
			    rospy.loginfo("\nI have reached my destination")
			self.condition = True



    def getGoal(self):
	try:
		tfBuffer = tf2_ros.Buffer()
		tfListener = tf2_ros.TransformListener(tfBuffer)
		

		transBotAR = tfBuffer.lookup_transform(self.bot_frame, self.ar_frame, rospy.Time(0), rospy.Duration(4.0))
		BAr_X = transBotAR.transform.translation.x
		BAr_Y = transBotAR.transform.translation.y
		
		#we'll send a goal to the robot to move 3 meters forward
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = 'base_link'
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose.position.x = BAr_X - 0.4
		goal.target_pose.pose.position.y = BAr_Y
		goal.target_pose.pose.orientation.w = 1.0 #go forward
		return goal
	except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
		print e
		pass


    def shutdown(self):
        rospy.loginfo("Stop")

# if __name__ == '__main__':
#     try:
#         GoForwardAvoid(sys.argv[1], sys.argv[2])
#     except rospy.ROSInterruptException:
#         rospy.loginfo("Exception thrown")