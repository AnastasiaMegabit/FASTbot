# FASTbot in the Real World

![FASTbot](https://1712507217.rsc.cdn77.org/wp-content/uploads/2016/08/medical-robot.jpg)

#### A First Aid Supply Transport Robot

It was important to our team to solve for a real world problem.  In emergency and disaster situations, first responders are always short-handed.  Doctors and Paramedics in the field will run low on supplies and have to return to the triage tent to replenish them.  FASTbot can help with that.


## Objectives and Goals

We wanted to design a bot that would receive requests from a dispatcher to autonomously pick up and deliver supplies to specific spots over unpredictable, rough terrain by using simultaneous localization and mapping.  AR Markers were meant to represent pick up and drop off locations, to later be replaced with color block recognition for locating pick ups at the Red Cross tent and facial recognition to locate particular people in the field for delivery.  In this type of emergency environment, we expected the bot to be able to identify and navigate to a specified destination while dynamically avoiding static or dynamic obstacles and maneuver rocky ground. 

#### Measurable Goals
- Command Based Autonomous Navigation: a dispatcher should be able to feed locations to the bot for pickup and drop off without any additional interaction.
- AR Tag Recognition: AR tags will be used for identifying pickup and drop off locations.
- Obstacle Avoidance: the bot should avoid both static and dynamic obstacles in its path.

#### Stretch Goals
- First Aid Box Loop: a dispatcher should be able to assign any number of pickups and drop offs to the bot without the need to return to home base between each.
- Color Block Recognition: the bot should be able to identify the Red Cross tent using color blocking to see the red cross.
- Facial Recognition: the bot should use facial recognition to identify a particular person in the field for delivery.
- Port Code to a Raspberry Pi Rover: the custom designed rover should be able to travel quickly across rugged terrain.

## Design

### Choices, Trade-Offs, Compromises
Because Turtlebots are already well integrated with ROS and rviz, we decided to write the code for a turtlebot, refine our algorithms, and then port the code to the custom hardware where we will face many small challenges such as marking the velocity of the wheels with encoders and using a CAD drawing to map our rover in rviz.

### Challenges 

#### Locating the AR Tag: 
- Creating the launch file to leverage the Kinect camera was difficult.  It required finding the correct topics to use for the camera and adding/adjusting all the correct parameters to the file.
- Maintaining visual contact and keeping the tag in range was hard to do as the bot moved around the space.  We needed to find a way to store and reference the location of the AR tag upon initial visualization so once the AR tag was seen, we sent the pose as a goal to move_base.

#### Moving to AR Tag and Stop
- Getting the bot to stop at a specific distance from the AR tag took some thought.  The bot uses the pose of the AR tag as a move_base goal.  It continues to move towards the goal until it is in that spot so we had to tell the bot that its actual goal was a delta distance from the AR tag pose.
- Producing the twist to rotate was a task.  Understanding how to use the linear and angular variables to move the bot in 3D space took us a great deal of time to figure out.  The linear x is a negative value for moving forward and rotations required the right angular velocity in conjunction with the right linear x as well.

#### Localizing the bot in global frame
- Ensuring the bot recognizes the accurate location and orientation were important for the bot to navigate to the correct goal pose of the AR tag.  If the bot did not start at the right place on the global map and then tried to navigate to the AR tag, the bot could move to the wrong spot but think it is where its supposed to go.

#### Generating the local obstacle costmap
- Getting a clean map of the lab was critical for the bot to correctly predict where the obstacles were in the local costmap. It took awhile for us to identify this as the issue but once we did, we were able to clear the small marks on the map away and give the bot clean white space on the floor.  At that point, it was able to update the local costmap easily any time it moved around.
- Physically lifting and moving bot confused it and placed obstacles where there were none.  We eventually found that if we used the 2D pose estimate and 2D nav goal features in the rviz visualization tool, the bot had no trouble keeping a current obstacle map.

#### Finding the right height of an obstacle
- Sometimes the object would not be high enough for the bot to be certain it was an obstacle.  It recognized it needed to move around something but the edges were a little fuzzy and it didn't navigate it well.
[![FASTbot taps edges of block box video](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot_Blooper.png)](https://youtu.be/XcfFtEHvWSk "FASTbot taps edges of block box video")

#### Patrolling an area
- Waiting for new request at home vs destination
- Recognizing bot is not at home if it can't find the AR tag

#### Following instructions
- Producing the quaternion to have the bot move right and left
- Inexact rotation/distance for patrol due to 80 degree spinScan


## Implementation
Meet the real FASTbot and his sidekicks, the AR tags.

![FASTbot](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot%20and%20friends.jpg)

Our FASTbot prototype uses the Kobuki model of the TurtleBot 2 open robotics platform with a Microsoft Kinect sensor designed for the Xbox 360 gaming console. The Kobuki is a mobile base with sensors, motors and power sources that allow it to have highly accurate odometry. The project incorporated the Kinect sensor with the use of both the RGB camera and depth sensitivity functions of the device to identify ARTags and avoid obstacles, respectively.  Laser cut stands and ¼-inch dowel rods were used as stands for laminated ARTags to mark home, pick-up, and drop-off locations for testing and demonstrative purposes. 

### System Diagram
![SystemDiagram](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/System%20Diagram.jpeg)

Imagine FASTbot being used in the real world for a moment...

A dispatcher would come in each morning and turn on the bots.  They would sit at home and wait to be dispatched.  Our code accounts for this.  When instructions.py is started, the bot recognizes it is at home and waits for the first instruction of the day to be given.

When needed, a dispatcher can feed pickup or drop off commands to the bot simply by entering [pickup/dropoff #]* any number of times.  The bot will recieve and parse the commands its been given, executing them one set at a time.  It calls pickup or dropoff depending on the command and uses the number entered to assign the destination AR marker.

Once parsed, it then calls goToAR which leverages move_base.  goToAR calls findAR which uses spinScan, spin, scanAR, and patrol functions to move right and left to come up with a goal based on the location of the AR tag or calls requests a new instruction, if no AR tag can be found.  The goal is then sent back to goToAR and passes the goal into move_base.

From there, the bot navigates to its destination.  If there are further instructions, the bot cycles through them all until there are no more.  Once completeed, the bot requests a new instruction.  If no instructions are given for a designated timeout threshold of 20 seconds, it will search for and return to the AR tag designated as home.  Once home, it sits and waits indefinitely for instructions and at the end of the day, the dispatcher will shut them down again.

### Software Implementation

File | Type | Role
------------ | ------------- | -------------
run_kinect | launch | The file is responsible for ARTag Recognition. It takes in certain arguments such as the size and tolerance associated with the ARTags, the ROS topics that communicate the camera's information as well as the image's information with respect to the camera, in order to identify and track poses of ARTags that can be seen by the kinect on the FASTbot. The file utilizes ar_track_alvar package functionalities to help the FASTbot recognize the ARTag of interest. 
instructions | python | This file is the control file responsible for interacting with the user i.e asking the user for instructions and updating the user on what is happening with the FASTbot. The file also decodes user instructions and sends them to goToAR.py for implementation. If there is no instruction from the user, the file initializes it's own instructions for goToAR.py to make sure the FASTbot gets back home if it is not home already.  
goToAR | python | This file is responsible for implementing the path to go to an ARTag. It relies heavily on the tf2 ros package to look up transforms between the ARTag and the FASTbot (specifically, the base_link frame of the bot) to later on head towards the ARTag while avoiding static and dynamic obstacles. It uses findAR.py to first make sure that there exists a valid transform between the ARTag of interest and the FASTbot i.e. the ARTag can be seen by the kinect on the bot. The file extensively utilizes move_base package functionalities to send pose goals to the FASTbot to go to an ARTag while avoiding obstacles and receive feedback on the results. 
findAR | python | This file is responsible for confirming there exists a transform between the ARTag of interest and the FASTbot. If there exists one, it informs goTOAR.py, otherwise, it initializes a series of recursive steps to patrol a certain area in order to find the ARTag of interest. This file also extensively utilizes move_base package functionalities to send pose goals to the FASTbot to go to an ARTag while avoiding obstacles and receive feedback on the results.


## Results

Our bot achieved many goals successfully...

![Achieved Goals](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/Achieved%20Goals.jpeg)

![Visits multiple locations]()

![Patrols when AR tag is not visable]()

![Avoids static and dynamic obstacles]()

[![FASTbot Full Demo](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot%20Full%20Feature%20Demo%20YouTube%20ScreenShot.png)](https://www.youtube.com/embed/YjjWvV42Nm4 "FASTbot Full Demo")


## Conclusion

## Team

## Appendix

### rqt_graphs
![Active Nodes with no Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/Active%20Nodes%20when%20no%20instructions%20passed.jpeg)

![Active Nodes with Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/ActiveNodes%20when%20instruction%20passed.jpeg)

![ROS Graph with Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/RosGraph%20when%20instruction%20passed.jpeg)

![ROS Graph with no Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/RosGraph%20when%20no%20instruction%20passed.jpeg)
