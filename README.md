# FASTbot in the Real World

![FASTbot](https://1712507217.rsc.cdn77.org/wp-content/uploads/2016/08/medical-robot.jpg)

#### A First Aid Supply Transport Robot

It was important to our team to solve for a real world problem.  In emergency and disaster situations, first responders are always short-handed.  Doctors and Paramedics in the field will run low on supplies and have to return to the triage tent to replenish them.  FASTbot can help with that.

## Objectives and Goals

We wanted to design a bot that would receive requests from a dispatcher to autonomously pick up and deliver supplies to specific spots over unpredictable, rough terrain by using simultaneous localization and mapping.  AR Markers were meant to represent pick up and drop off locations, to later be replaced with color block recognition for locating pick ups at the Red Cross tent and facial recognition to locate particular people in the field for delivery.  In this type of emergency environment, we expected the bot to be able to identify and navigate to a specified destination while dynamically avoiding static or dynamic obstacles and maneuver rocky ground. 

## Design

#### Measurable Goals
- Command Based Autonomous Navigation: a dispatcher should be able to feed locations to the bot for pickup and drop off without any additional interaction.
- AR Tag Recognition: AR tags will be used for identifying pickup and drop off locations.
- Obstacle Avoidance: the bot should avoid both static and dynamic obstacles in its path.

#### Stretch Goals
- First Aid Box Loop: a dispatcher should be able to assign any number of pickups and drop offs to the bot without the need to return to home base between each.
- Color Block Recognition: the bot should be able to identify the Red Cross tent using color blocking to see the red cross.
- Facial Recognition: the bot should use facial recognition to identify a particular person in the field for delivery.
- Port Code to a Raspberry Pi Rover: the custom designed rover should be able to travel quickly across rugged terrain.

### Choices, Trade-Offs, Compromises
Because Turtlebots are already well integrated with ROS and rviz, we decided to write the code for a turtlebot, refine our algorithms, and then port the code to the custom hardware where we will face many small challenges such as marking the velocity of the wheels with encoders and using a CAD drawing to map our rover in rviz.

### Challenges 

#### Locating the AR Tag: 
- Creating the launch file to leverage the Kinect camera was difficult.  It required finding the correct topics to use for the camera and adding/adjusting all the correct parameters to the file.
- Maintaining visual contact and keeping the tag in range was hard to do as the bot moved around the space.  We needed to find a way to store and reference the location of the AR tag upon initial visualization so once the AR tag was seen, we sent the pose as a goal to move_base.

#### Moving to AR Tag and Stop
- Getting the bot to stop at a specific distance from the AR tag.
- Producing the twist to rotate.

#### Localizing the bot in global frame
- Getting a clean map of the lab
- Ensuring the bot recognizes the accurate location and orientation

#### Generating the local obstacle costmap
- Physically moving hte bot confused it and placed obstacles where there were none

#### Finding the right height of an obstacle
- Sometimes the object would not be high enough for the bot to be certain it was an obstacle.  It recognized it needed to move around something but the edges were a little fuzzy and it didn't navigate it well.
![FASTbot taps edges of block box video]()

#### Patrolling an area
- Waiting for new request at home vs destination
- Recognizing bot is not at home if it can't find the AR tag

#### Following instructions
- Producing the quaternion to have the bot move right and left
- Inexact rotation/distance for patrol due to 80 degree spinScan


## Implementation
Meet the real FASTbot and his sidekicks, the AR tags.

![FASTbot](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/FASTbot%20and%20friends.jpg)

Our FASTbot prototype uses the Kobuki model of the TurtleBot 2 open robotics platform with a Microsoft Kinect sensor designed for the Xbox 360 gaming console. The Kobuki is a mobile base with sensors, motors and power sources that allow it to have highly accurate odometry. The project incorporated the Kinect sensor with the use of both the RGB camera and depth sensitivity functions of the device to identify ARTags and avoid obstacles, respectively.  Laser cut stands and ¼-inch dowel rods were used as stands for laminated ARTags to mark home, pick-up, and drop-off locations for testing and demonstrative purposes. 

#### rqt_graphs
![Active Nodes with no Instructions](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/Active%20Nodes%20when%20no%20instructions%20passed.jpeg)

![Active Nodes with Instructions](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/ActiveNodes%20when%20instruction%20passed.jpeg)

![ROS Graph with Instructions](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/RosGraph%20when%20instruction%20passed.jpeg)

![ROS Graph with no Instructions](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/RosGraph%20when%20no%20instruction%20passed.jpeg)

#### System Diagram
![SystemDiagram](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/System%20Diagram.jpeg)

#### Software Implementation

File | Type | Role
------------ | ------------- | -------------
run_kinect | launch | The file is responsible for how the Kinect’s camera interprets the AR . It takes in the expected dimensions of the AR Tags, tolerances as well as frames with respect to whom the AR Tag transforms should be calculated. In addition it takes in node names and resolution information. It utilizes ar_track_alvar package functionalities to help the FASTbot recognize the tag of interest. 
instructions | python | This file is the file responsible for interacting with the user, processing and decoding the instructions.  It communicates with the rest of the python files to ensure the user’s input goal is achieved. If there is no instruction fed in, it will wait for 20 seconds after which it will send a goal to the FASTbot to go home.
goToAR | python | This file is responsible for implementing the path to go to an AR tag. It relies heavily on tf2 ros package to look up transforms between the tag and it’s base_link to later on head towards the AR tag. It uses findAR to first make sure that the AR Tag of interest can be seen. 
findAR | python | This file is responsible for wai



## Results

Our bot achieved many goals successfully...

![Achieved Goals](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/Achieved%20Goals.jpeg)

![Visits multiple locations]()

![Patrols when AR tag is not visable]()

![Avoids static and dynamic obstacles]()

## Conclusion

## Team
