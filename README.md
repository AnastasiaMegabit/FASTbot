# This is FASTbot 
A First Aid Supply Transport Robot
![FASTbot](https://1712507217.rsc.cdn77.org/wp-content/uploads/2016/08/medical-robot.jpg)

## FASTbot in the Real World

It was important to our team to solve for a real world problem.  In emergency and disaster situations, first responders are always short-handed.  Doctors and Paramedics in the field will run low on supplies and have to return to the triage tent to replenish them.  FASTbot can help with that.

## Objectives and Goals

We wanted to design a bot that would receive requests from a dispatcher to autonomously pick up and deliver supplies to specific spots over unpredictable, rough terrain by using simultaneous localization and mapping.  AR Markers were meant to represent pick up and drop off locations, to later be replaced with color block recognition for locating pick ups at the Red Cross tent and facial recognition to locate particular people in the field for delivery.  In this type of emergency environment, we expected the bot to be able to identify and navigate to a specified destination while dynamically avoiding static or dynamic obstacles and maneuver rocky ground. 

## Design

#### Measurable Goals
- Command Based Autonomous Navigation: a dispatcher should be able to feed locations to the bot for pickup and drop off.
- AR Tag Recognition: AR tags will be used for identifying pickup and drop off locations.
- Obstacle Avoidance: the bot should avoid both static and dynamic obstacles in its path.

#### Stretch Goals
- First Aid Box Loop: a dispatcher should be able to assign any number of pickups and drop offs to the bot without the need to return to home base between each.
- Color Block Recognition: the bot should be able to identify the Red Cross tent using color blocking to see the red cross.
- Facial Recognition: the bot should use facial recognition to identify a particular person in the field for delivery.
- Port Code to a Raspberry Pi Rover: the custom designed rover should be able to travel quickly across rugged terrain.

#### Choices, Trade-Offs, Compromises
Because Turtlebots are already well integrated with ROS and rviz, we decided to write the code for a turtlebot, refine our algorithms, and then port the code to the custom hardware where we will face many small challenges such as marking the velocity of the wheels with encoders and interpreting that in 

#### Challenges 

## Implementation

## Results

## Conclusion

## Team
