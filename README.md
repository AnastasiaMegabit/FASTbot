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
The main design choice we had to deal with in the beginning of our planning phase was the bot we wished to use. Initially, we planned on working on a raspberry pi rover. We chose this mainly because of the following reasons:
- We had inventoried all the materials we would need including the sensors, main frame, chassis and tires for the rover.
- We had begun assembling the body of the rover,
- We believed it would be suitable for the rough, unpredictable terrain we expected for a carrier bot.

Shortly thereafter, we decided to use a Turtlebot 2 instead because, unlike the rover, it was well integrated with ROS and rviz and was fully functional. This would allow us to focus on the actual implementation of the algorithm for a carrier bot, run the algorithm several times and refine it.  Then we planned to port it to the custom hardware for the raspberry pi rover where we would inevitably have to work through many other challenges such as installing encoders to control the trajectory and velocity of the bot given the huge tires and create a custom URDF file for our rover in rviz. 


### Challenges 

#### Locating an ARTag
- Creating the launch file to leverage the Kinect camera was difficult. It required finding the correct topics to use for the camera and adding/adjusting the correct parameters to the file such as the ROS topic for the camera's information versus the ROS topic for the image's information with respect to the camera.
- Ensuring that the ARTag was always in sight to be able to determine it's pose was challenging because the bot also had to avoid obstacles while heading to the ARTag. We needed to find a way to store the location of the ARTag with respect to a fixed frame, the global frame, upon it's initial visualization so that we could leverage this pose as a goal for move_base.

#### Moving to the ARTag and Stopping
- Getting the bot to stop at a specific distance from the AR tag took some thought. The bot used  the pose of the AR tag as a move_base goal and thus, would get confused since the ARTag itself was also an obstacle. We had to make sure we accounted for a delta distance from the ARTag pose in the move_base goal. This final delta distance was a culmination of several trial and error runs. 
- Producing the twist to rotate the bot to a desirable position took some effort too. We realized that the linear x position is a negative value for moving forward and rotations required the right angular velocity in conjunction with a small linear x value to ensure smooth rotations.

#### Localizing the bot in the Global Frame
- Ensuring the bot recognized its own position and orientation on the the global map of the lab was important for navigating to an AR Tag while using move_base.  If the bot could not localize itself appropriately, it would mis calculate the pose of the ARTag of interest and go to a place that did not have the actual ARTag. This required us to launch rviz everytime we launched other important files to ensure we could set the 2D Pose of the bot manually. 

#### Generating the local obstacle costmap
- Getting a clean map of the lab was critical for the bot to correctly predict where the obstacles were in the local costmap. It took awhile for us to identify this as the issue but once we did, we were able to clear the small marks on the map away and give the bot clean white space on the floor.  At that point, it was able to update the local costmap easily any time it moved around.
![Setting a 2D pose](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/NavigationLaunchers.jpeg?raw=true)
- Physically lifting and moving bot confused it and placed obstacles where there were none.  We eventually found that if we used the 2D pose estimate and 2D nav goal features in the rviz visualization tool, the bot had no trouble keeping a current obstacle map.

#### Obstacle Avoidance
- When we first began thinking of the best way to avoid obstacles, ..... (Need to talk about Mark Silliman here too)
- While experimenting with move_base to determine limitations of obstacle avoidance for the bot, we realized that the obstacle had to be of a certain height before the bot could fully estimate it's dimensions. While the bot could easily acknowledge the presence of an obstacle for any size, the edges of a shorter obstacle seemed a little fuzzy in the bot's local costmap and therefore, it was not able to navigate them well. Thus, had to ensure obstacles were approximately above the kinect's height on the bot for clear edge detection in the local costmap.
[![FASTbot taps edges of block box video](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot_Blooper.png)](https://youtu.be/XcfFtEHvWSk "FASTbot taps edges of block box video")

#### Patrolling an Area
- Producing the quaternion to have the bot move right and left was a new experience for our team and not as intuitive as we had hoped.  It turns out it is hard for a human to think about what a quaternion looks like but much easier to think in terms of Euler's.  So, we chose to use a conversion function which takes in an Euler's angle and returns a quaternion rather than tinker with the quaternion directly.
- We found that we experienced an inexact rotation/distance for patrol due to our decision to use an 80 degree spinScan.  The choice to use this odd degree was because we wanted to make sure the tag would, at some point, be within the scope of the Kinect camera during its full spin but at the same time minimize the number of scans the bot would have to stop to make.  This meant that when the bot "turned to the left/right", it would be an offset from its starting position and the bot would not move exactly left or exactly right.  We decided this was acceptable considering the bot was simply patrolling a general area and not specifically required to go exactly left or right.

#### Following instructions
- Our bot was designed to request a new instruction from dispatch using the raw_input command.  This works beautifully when the dispatcher turns the bots in the morning and they sit at home waiting for instructions but it is problematic if the bot is in the field after its last pickup or dropoff.  The request was going to function the same but if the bot was in the field, it should only wait for a short time before returning home to get out of the way.  raw_input does not have a built in time out feature so we had to get creative. We found a creative use of an AlarmException and the signal class which we could tweak and leverage to call goHome after it waited for 20 seconds and which would then send an empty char to raw_input.
- Recognizing whether or not the bot is at home when it can't find the ARTag was a complication as well.  We found that if the bot patrolled and area but did not find a the AR tag for which it was looking, it would assume it was home and return to waiting for a new instruction.  We used a simple boolean value to account for this occasion.  If the bot left home initially, it recognized it was not home and would not again assume it was home unless goHome was called.



## Implementation
Meet the real FASTbot and his sidekicks, the AR tags.

 <span style="display:block;text-align:center">![FASTbot](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot%20and%20friends.jpg)</span>

Our FASTbot prototype uses the Kobuki model of the TurtleBot 2 open robotics platform with a Microsoft Kinect sensor designed for the Xbox 360 gaming console. The Kobuki is a mobile base with sensors, motors and power sources that allow it to have highly accurate odometry. The project incorporated the Kinect sensor with the use of both the RGB camera and depth sensitivity functions of the device to identify ARTags and avoid obstacles, respectively.  Laser cut stands and ¼-inch dowel rods were used as stands for laminated ARTags to mark home, pick-up, and drop-off locations for testing and demonstrative purposes. 

### System Diagram
![SystemDiagram](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/System%20Diagram.jpeg)

To understand what FASTbot's day might look like in use at a field site, we offer the following walkthrough...

A dispatcher would come in, each morning and turn on the bots.  They would then sit at home and wait to be dispatched.  Our code accounts for this.  When instructions.py is started, the bot recognizes it is at home and waits for the first instruction of the day to be given.

When needed, a dispatcher can feed pickup or drop off commands to the bot simply by entering [pickup/dropoff #]* any number of times.  The bot will receive and parse the commands its been given, executing them one set at a time.  It calls pickup or dropoff depending on the command and uses the number entered to assign the destination ARTag.

Once parsed, it then calls goToAR.py which leverages move_base.  goToAR.py calls findAR.py (which uses methods such as spinScan, spin, scanAR, and patrol) to confirm the presence of the ARTag requested in the bot's vicinity. If findAR.py cannot find the ARTag of interest, goToAR.py requests a new instruction from the dispatcher. If findAR.py can find the ARTag requested, goToAR.py comes up with a move_base goal based on the position and orientation of the ARTag.

From there, the bot navigates to the provided move_base goal.  If there are further instructions, the bot cycles through all of them until there are no more.  Once completed, the bot requests a new instruction.  If no instructions are given for a designated timeout threshold of 20 seconds, it will search for and return to the ARTag designated as home.  Once home, it sits and waits indefinitely for instructions and at the end of the day, the dispatcher will shut them down again.


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
#### FASTbot can be sent to multiple locations without having to return home between each dispatch.
[![Visits multiple locations](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/Multiple_Loc.png)]( https://youtu.be/yvhe6k0q9xY "Visits multiple locations")
#### When FASTbot cannot find the AR tag requested, it will patrol in search of one.
[![Patrols when AR tag is not visible](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot_patrol.png)](https://youtu.be/v3bBYx6qFfA "Patrols when AR tag is not visible")
#### FASTbot effectively avoids both static and dynamic obstacles in its path.
[![Avoids static and dynamic obstacles](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/Static_Dynamic_Obs_Avoid_Screenshot.png)](https://www.youtube.com/watch?v=7iK36OHjpcs "Avoids static and dynamic obstacles")
#### FASTbot in full action.
[![FASTbot Full Demo](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/FASTbot%20Full%20Feature%20Demo%20YouTube%20ScreenShot.png)](https://www.youtube.com/embed/YjjWvV42Nm4 "FASTbot Full Demo")


## Conclusion
Our team provided highly successful overall, achieving all of our measurable goals and one of our stretch goals.  Obstacle avoidance was a non-trivial task and we found it to be an enjoyable challenge.  Once we agreed to use the move_base library, most of our problems were small but plentiful.  The phrase "the devil's in the details" would be the most accurate way to describe the majority of our hurdles.  

## Team
![]()
#### Mariyam Jivani
![Anastasia](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/Anastasia%20Scott.jpg?raw=trues=100)
#### Anastasia Scott
![]()
#### Robert Hoogsteden

Our team worked collaboratively, taking turns typing on the main workstation and writing our code as a team.  Those of us not actively typing at the workstation had out our laptops and would take notes on the process or research issues we were facing at any given time.  Full participation was key in our success and each of the team members were responsible for at least two major code breakthroughs when we got stuck during the process.

## Appendix

### Project Code
- Our code is available in full on the associated github repository and can be accessed using the link on the upper left corner of this page.

### Dispatcher Window
- Rviz and terminal windows displaying what the system looks like to the dispatcher.
![Visualization and terminal windows](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/Final%20Run%202b.jpeg?raw=true)
![Patrolling terminal and visualization](https://github.com/AnastasiaMegabit/FASTbot/blob/master/img/Full%20Patrol%20Terminal.jpeg?raw=true)

### rqt_graphs
#### Active Nodes with No Instructions Given to the Bot
![Active Nodes with no Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/Active%20Nodes%20when%20no%20instructions%20passed.jpeg)

#### ros_graph with No Instructions Given to the Bot
![ROS Graph with no Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/RosGraph%20when%20no%20instruction%20passed.jpeg)

#### Active Nodes with Instructions Given to the Bot
![Active Nodes with Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/ActiveNodes%20when%20instruction%20passed.jpeg)

#### ros_graph with Instructions Given to the Bot
![ROS Graph with Instructions](https://raw.githubusercontent.com/AnastasiaMegabit/FASTbot/master/img/RosGraph%20when%20instruction%20passed.jpeg)


