# FASTbot in the Real World

![FASTbot](https://1712507217.rsc.cdn77.org/wp-content/uploads/2016/08/medical-robot.jpg)

#### A First Aid Supply Transport Robot

It was important to our team to solve for a real world problem.  In emergency and disaster situations, first responders are always short-handed.  Doctors and Paramedics in the field will run low on supplies and have to return to the triage tent to replenish them.  FASTbot can help with that.


## Objectives and Goals

We wanted to design a bot that would receive requests from a dispatcher to autonomously pick up and deliver supplies to specific spots over unpredictable, rough terrain by using simultaneous localization and mapping.  AR Markers were meant to represent pick up and drop off locations, to later be replaced with color block recognition for locating pick ups at the Red Cross tent and facial recognition to locate particular people in the field for delivery.  In this type of emergency environment, we expected the bot to be able to identify and navigate to a specified destination while dynamically avoiding static and dynamic obstacles and maneuver over rocky areas. 

#### Measurable Goals
- Command Based Autonomous Navigation: A dispatcher should be able to feed locations to the bot for pickup and drop off without any additional interaction.
- ARTag Recognition: ARTags will be used for identifying pickup and drop off locations.
- Obstacle Avoidance: The bot should avoid both static and dynamic obstacles in its path.

#### Stretch Goals
- First Aid Box Loop: A dispatcher should be able to assign any number of pickups and drop offs to the bot without the need to return to home base between each.
- Color Block Recognition: The bot should be able to identify the Red Cross tent using color blocking to see the red cross.
- Facial Recognition: The bot should use facial recognition to identify a particular person in the field for delivery.
- Port Code to a Raspberry Pi Rover: The custom designed rover should be able to travel quickly across rugged terrain.

## Design

### Choices
The main design choice we had to deal with in the beginning of our planning phase was the bot we wished to use. We initially planned on working on a raspberry pi rover. This is mainly because 
- we had inventoried all the materials we would need including the sensors, main frame, chassises and tires for the rover
- we had begun assembling the body of the rover 
- we believed it would be suitable for the rough, unpredictable terrain we expected for a carrier bot, 

but later on, we decided to choose the turtlebot 2i, mainly because, it was already well integrated with ROS and rviz which in turn, would allow us to focus on the actual implementation of the algorithm for a carrier robot, refine it and then port the code to the custom hardware for a raspberry pi rover where we would inevitably have to work through many other challenges such as installing encoders to control the trajectory and velocity of the bot given the huge tires and create a custom URDF file for our rover in rviz. 


### Challenges 

#### Locating an ARTag
- Creating the launch file to leverage the Kinect camera was difficult. It required finding the correct topics to use for the camera and adding/adjusting the correct parameters to the file such as the ROS topic for the camera's information versus the ROS topic for the image's information with respect to the camera.
- Ensuring that the ARTag was always in sight to be able to determine it's pose was challenging because the bot also had to avoid obstacles while heading to the ARTag. We needed to find a way to store the location of the ARTag with respect to a fixed frame, the global frame upon it's initial visualization so that we could leverage this pose as a goal for move_base.

#### Moving to the ARTag and Stopping
- Getting the bot to stop at a specific distance from the AR tag took some thought. The bot used  the pose of the AR tag as a move_base goal and thus, would get confused since the ARTag itself was also an obstacle. We had to make sure we accounted for delta distance from the ARTag pose in the move_base goal. This delta distance also was a culmination of sveeral trial and errors. 
- Producing the twist to rotate the bot to a desirable position took some effort too. We realised that the linear x position is a negative value for moving forward and rotations required the right angular velocity in conjunction with a small linear x value to ensure smoother rotations.

#### Localizing the bot in the Global Frame
- Ensuring the bot recognized it's own position and orientation on the the global map of the lab was important for navigating to an AR Tag while using move_base.  If the bot could not localize itself appropriately, it would mis calculate the pose of the ARTag of interest and go to a place that did not have the actual ARTag. This required us to launch rviz everytime we launched other important files to ensure we could set the 2D Pose of the bot manually. 

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

 <span style="display:block;text-align:center">![FASTbot](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot%20and%20friends.jpg)</span>

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
#### Visits Multiple Locations
[![Visits multiple locations](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/Multiple_Loc.png)]( https://youtu.be/yvhe6k0q9xY "Visits multiple locations")
#### Patrols when AR tag is not visible
[![Patrols when AR tag is not visible](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot_patrol.png)](https://youtu.be/v3bBYx6qFfA "Patrols when AR tag is not visible")
#### Avoids static and dynamic obstacles
[![Avoids static and dynamic obstacles](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/Static_Dynamic_Obs_Avoid_Screenshot.png)](https://www.youtube.com/watch?v=7iK36OHjpcs "Avoids static and dynamic obstacles")
#### FASTbot Full Demo
[![FASTbot Full Demo](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot%20Full%20Feature%20Demo%20YouTube%20ScreenShot.png)](https://www.youtube.com/embed/YjjWvV42Nm4 "FASTbot Full Demo")


## Conclusion

## Team

## Appendix

### rqt_graphs
![Active Nodes with no Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/Active%20Nodes%20when%20no%20instructions%20passed.jpeg)

![Active Nodes with Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/ActiveNodes%20when%20instruction%20passed.jpeg)

![ROS Graph with Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/RosGraph%20when%20instruction%20passed.jpeg)

![ROS Graph with no Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/RosGraph%20when%20no%20instruction%20passed.jpeg)
