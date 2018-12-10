# FASTbot in the Real World

![FASTbot](https://1712507217.rsc.cdn77.org/wp-content/uploads/2016/08/medical-robot.jpg)

#### A First Aid Supply Transport Robot

There has been a lot of effort being invested into creating bots that relieve some stress imposed on search and rescue teams and triage nurses in field hospitals. More generally, there is always going to be a need to develop technology that allows for accessibility, portability and some level of autonomy in the healthcare or disaster management sector. FASTbot can help with such situations.

Consider this scenario, there is an emergency situation and the first responders are short-handed. In the field, they are running low on supplies and thus, have to return to the triage tent to replenish them. They ask FASTbot to go to the triage tent and get the supplies they need while they continue treating patients in the field. FASTbot allowed the first-responders to focus on treating patients rather than perform several trips back and forth to the triage tent for supplies. 

Since it was important for our team to get closer to solving a real-world problem, we decided on work on a carrier bot that would be able to navigate its way to a specified destination while avoiding static and dynamic obstacles. Our project allowed us to get a taste of the challenges and design decisions required to fulfill the goal of the carrier bot to deliver first aid kits in unpredictable and rough terrain. 

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

### rqt_graphs
![Active Nodes with no Instructions](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/Active%20Nodes%20when%20no%20instructions%20passed.jpeg)

![Active Nodes with Instructions](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/ActiveNodes%20when%20instruction%20passed.jpeg)

![ROS Graph with Instructions](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/RosGraph%20when%20instruction%20passed.jpeg)

![ROS Graph with no Instructions](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/RosGraph%20when%20no%20instruction%20passed.jpeg)

### System Diagram
![SystemDiagram](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/System%20Diagram.jpeg)

### Software Implementation

File | Type | Role
------------ | ------------- | -------------
run_kinect | launch | The file is responsible for ARTag Recognition. It takes in certain arguments such as the size and tolerance associated with the ARTags, the ROS topics that communicate the camera's information as well as the image's information with respect to the camera, in order to identify and track poses of ARTags that can be seen by the kinect on the FASTbot. The file utilizes ar_track_alvar package functionalities to help the FASTbot recognize the ARTag of interest. 
instructions | python | This file is the control file responsible for interacting with the user i.e asking the user for instructions and updating the user on what is happening with the FASTbot. The file also decodes user instructions and sends them to goToAR.py for implementation. If there is no instruction from the user, the file initializes it's own instructions for goToAR.py to make sure the FASTbot gets back home if it is not home already.  
goToAR | python | This file is responsible for implementing the path to go to an ARTag. It relies heavily on the tf2 ros package to look up transforms between the ARTag and the FASTbot (specifically, the base_link frame of the bot) to later on head towards the ARTag while avoiding static and dynamic obstacles. It uses findAR.py to first make sure that there exists a valid transform between the ARTag of interest and the FASTbot i.e. the ARTag can be seen by the kinect on the bot. The file extensively utilizes move_base package functionalities to send pose goals to the FASTbot to go to an ARTag while avoiding obstacles and receive feedback on the results. 
findAR | python | This file is responsible for confirming there exists a transform between the ARTag of interest and the FASTbot. If there exists one, it informs goTOAR.py, otherwise, it initializes a series of recursive steps to patrol a certain area in order to find the ARTag of interest. This file also extensively utilizes move_base package functionalities to send pose goals to the FASTbot to go to an ARTag while avoiding obstacles and receive feedback on the results.



## Results

Our bot achieved many goals successfully...

![Achieved Goals](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/Achieved%20Goals.jpeg)

![Visits multiple locations]()

![Patrols when AR tag is not visable]()

![Avoids static and dynamic obstacles]()

## Conclusion

## Team
