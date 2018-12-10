#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
import tf2_ros
import sys
from geometry_msgs.msg import Twist
from tf.transformations import *
import numpy as np


class ARFinder():

    def __init__(self, bot_frame, ar_frame, move_base):
        self.ar_frame = ar_frame
        self.bot_frame = bot_frame
        self.move_base = move_base
    

    def scanAR(self):
        print("I am scanning")
        timeStart = rospy.Time.now()
        timeNow = timeStart
        tfBuffer = tf2_ros.Buffer()
        tfListener = tf2_ros.TransformListener(tfBuffer)
        while(timeNow.to_sec() -timeStart.to_sec() < 5):
            canTrans = tfBuffer.can_transform(self.bot_frame, self.ar_frame, rospy.Time(0))
            if (canTrans):
                return True
            timeNow = rospy.Time.now()
        return False

    def spin(self):
        print("I am spinning")
        q_rot = quaternion_from_euler(0, 0, np.pi / 3)
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.orientation.x = q_rot[0]
        goal.target_pose.pose.orientation.y = q_rot[1]
        goal.target_pose.pose.orientation.z = q_rot[2]
        goal.target_pose.pose.orientation.w = q_rot[3]
        self.move_base.send_goal(goal)
        self.move_base.wait_for_result(rospy.Duration(60))

    def moveLeft(self):
        print("I am turning to the left")
        q_rot = quaternion_from_euler(0, 0, np.pi / 2)
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.orientation.x = q_rot[0]
        goal.target_pose.pose.orientation.y = q_rot[1]
        goal.target_pose.pose.orientation.z = q_rot[2]
        goal.target_pose.pose.orientation.w = q_rot[3]
        self.move_base.send_goal(goal)
        self.move_base.wait_for_result(rospy.Duration(60))
        print("I am moving 2 feet to the left")
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 1
        goal.target_pose.pose.orientation.w = 1.0 
        self.move_base.send_goal(goal)
        self.move_base.wait_for_result(rospy.Duration(60))

    def moveRight(self):
        print("I am turning back to the right")
        q_rot = quaternion_from_euler(0, 0, -np.pi)
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.orientation.x = q_rot[0]
        goal.target_pose.pose.orientation.y = q_rot[1]
        goal.target_pose.pose.orientation.z = q_rot[2]
        goal.target_pose.pose.orientation.w = q_rot[3]
        self.move_base.send_goal(goal)
        self.move_base.wait_for_result(rospy.Duration(60))
        # self.move_base.send_goal(goal)
        # self.move_base.wait_for_result(rospy.Duration(60))
        print("I am moving 2 feet to the right")
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 1
        goal.target_pose.pose.orientation.w = 1.0 
        self.move_base.send_goal(goal)
        self.move_base.wait_for_result(rospy.Duration(60))

    def requestInstruction(self):
        return False


    def findAR(self):
        print("I am finding")
        try:
            if (self.spinScan()):
                return True
            self.moveLeft()
            if (self.spinScan()):
                return True
            self.moveRight()
            if (self.spinScan()):
                return True
            self.requestInstruction()
            return False
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            print e
            pass

                
    def spinScan(self):
        count = 0
        while(count < 6):
            if(self.scanAR()):
                return True
            else:
                self.spin()
                count = count + 1
        return False