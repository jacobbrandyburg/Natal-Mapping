# Natal-Mapping: Using ROS 2 Kilted Kaiju on the Turtlebot 2e Model


## About Natal Mapping
For my Capstone project, I will be studying the Robotic Operating System language to understand how Turtlebots operate in observing the area around them to create a map using SLAM (Simultaneous Localization and Mapping). 

The migration of adult sea turtles back to the exact beaches where they were born is called Natal Homing, and similarly with the goal of this project, using LiDAR with a TurtleBot to map classrooms, hallways and identifying landmarks to direct first year students to specific classrooms, this is Natal Mapping.


## Getting started and Installation

This repository has all the code needed for running the model: Turtlebot 2e in ROS2, but some packages need to be built, so please follow this step-by-step instruction for doing so.

This is also made, in part by ________ in they're turtlebot2 ROS2 repo https://github.com/idorobotics/turtlebot2_ros2. They suggest also following these commands on both the docked and workstation laptop:

sudo apt-get install ros-kilted-teleop-twist-keyboard 
ros-kilted-joy-teleop 
ros-kilted-teleop-twist-joy

(This is just making sure you can control the Turtlebot with either the keyboard or a joystick)

## Progression Timeline
Talk about what I've learned up to this point


## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

This repository will store the code for a ROS2 workspace that will allow the model, Turtlebot 2e, to work in ROS2. This repository also takes the Kobuki base code from the *Idorobotics: Turtlebot2_ROS2* repository and the Astra camera it uses from the *Orbbec: OrbbecSDK_ROS2* repository.

As of the end of Capstone 1, I am hoping that this repository will contain all the code needed for getting the Turtlebot 2e to move completely in ROS2 and the Astra camera to 

## Understanding Concepts / Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.


//Attempting to upload a gif from the ROS2 Kilted Tutorial
![alt text](image.png)


## Roadmap
I am hoping by December of 2025 to have all the code for running a ROS1 Kinetic Turtlebot2e in ROS2 Kilted from this repository alone. In April of 2026, I am planning on either getting a package put together for object identification or building something similar as a stretch goal. I'm not entirely sure how long that will take or if this is enough, but I will hopefully have a definite answer soon. 

## Support
My email address: jbrandy1@unca.edu

## Authors and acknowledgment
The original owners of the *turtlebot2_ros2* and the *ros2_astra_camera* repositories were Bonolo Mathibela and the Orbbec company

## License
The ROS2 code is under the Apache 2.0 License
