# Natal-Mapping: Turtlebot Grid Occupancy Maps for Building Navigation


## About Natal Mapping
Transitioning to a new campus as a college freshman can be very stressful, especially when figuring out the best route to get to all your classes on time. If the school is large enough, a student may be given a map showing the physical locations of the buildings relative to one another, but the problem doesn’t end there. Upon entering a new building, students will promptly seek room numbers to orient themselves, a process that can either be straightforward or immediately disorienting. Having a map with an intuitive key to follow would be ideal, but doing so from scratch could be very tedious and may lack accuracy if drawn manually. With Natal Mapping, this could be done in a fraction of the time for all of UNCA's buildings.

Natal Mapping is the collaborative effort of both the Robot Operating System’s environment visualizer tool (RViz) and a door detection program made from the Probabilistic Houghlines Transform algorithm to build a floor map and classify rooms based on the geometric structure of the door at the same time. The door detection process works by filtering lines from geometric shapes in the camera feed and highlighting the ones that form the basic shapes of a door or elevator. Both tools determine the layout based on the relative positions of classrooms, bathrooms, and elevators during map construction. With color-coordinated post-processing, these maps can then be printed out onto large posters or bulletin boards placed near building entrances or next to stairs, elevators, or anywhere where anyone enters a new floor.

The ROS visualizer works off of a Turtlebot model 2e's LiDAR camera and for this project, I went through the process of searching for the correct drivers from ROS Github repositories to find if anyone has started the process of creating drivers that works for specifically the 2e model. So special thanks to [Bonolo Mathibela] (https://github.com/idorobotics) for the Kobuki Turtlebot 2 drivers and [Joe Dong] (https://github.com/jian-dong) and [lixby03] (https://github.com/lixby03) for the Astra Camera drivers. This capstone project was also, in part, a passion project for learning about robot software development. A good portion of this assignment was learning ROS, finding drivers, learning the Ubuntu Linux interface and how to manually build and manage packages from source. Somethings might appear unorganized here, but I intend to polish things up as time continues on.


## Getting started and Setup

This repository has all the drivers needed for running the Turtlebot model 2e with a Kobuki base in specifically the short-term distribution of ROS2, Kilted Kaiju. Some packages may build finicky, so please follow these step-by-step instructions if anything involving the Kobuki base or the Astra camera doesn't seem to build correctly. The Kobuki base (**kobuki_node**) from the [**Idorobotics**: Turtlebot2_ROS2] (https://github.com/idorobotics/turtlebot2_ros2) repository and the Astra Camera (**camera_astra**) it uses from the [**Orbbec: OrbbecSDK_ROS2**] (https://github.com/orbbec/ros2_astra_camera/tree/master) repository. Remember, where there are mentions of a different ROS distro, replace it with Kilted Kaiju (ros-kilted-kaiju).

Make sure before SSH-ing into the netbook that both the docked netbook and the control station device are both on the same network and includes the correct flags too. -X is for running graphical interfaces on the remote device (RViz) and -C flag is for data compression (as the netbooks did struggle a bit with streaming RViz).  
- *ssh -XC netbookname@ipaddress*

This project's launch file (natal-launch.py) is made up of many different programs and separate launch files. Those being:
- **kobuki_node**: Turns on the Kobuki base
- **camera_astra**: Turns on the Astra Camera
- **slam_tool**: Boots up RViz
- **turtlebot**: All the components to build the Turtlebot description model in RViz
- **Depthimage_to_laserscan**: Turns on the actual scan topic for observing the environment and building the map
- **Base_to_Camera**: Attaching the camera to the base link of the Turtlebot description model
- **Door_Detection**: Door detection program

You can run each of these nodes individually if you wanted to like so:
- ros2 launch kobuki_node kobuki_node-launch.py
- ros2 launch astra_camera astra.launch.xml
- ros2 launch slam_toolbox online_async_launch.py
- ros2 launch turtlebot_description display.launch.py gui:=False
- ros2 run depthimage_to_laserscan depthimage_to_laserscan_node   --ros-args   -r depth:=/camera/depth/image_raw   -r depth_camera_info:=/camera/depth/camera_info   -r scan:=/scan     -p qos_overrides./depth.subscriber.reliability:=best_effort -p scan_height:=240
- ros2 run tf2_ros static_transform_publisher 0 0 0.2 0 0 0 base_link camera_link
- ros2 run door_detection door_detection

-----------------------------------------------------------------------------------------------------------------------------

In order to operate the Turtlebot after first SSH-ing into the docked netbook and cloning this repository, you must first open up two linux tabs (one for the launch file and one for the keyboard control) and source this workspace with the following command from the root directory in each one:  
**source ./install/setup.bash**

In the launch file terminal, simply navigate to the folder with the launch file:  
**cd natal_mapping/src/natal-mapping_launch**  
and run:  
**ros2 launch natal-launch.py**

After a little while, you should hear the turtlebot chime on, the LiDAR's camera turn on and RViz pop up on your screen (if the x forwarding is working correctly). This means everything worked successfully! :D 
RViz can now be used and the displays based on all the nodes of the launch file can be toggled on from here. Here are all the displays I usually use and what topics they are subscribed to:
- Fixed Frame: /map
- Image: /camera/color/image_raw
- LaserScan: /scan
- Map: /map

In the second terminal, source it the same way, but after doing so, run this command to start up the teleoperation via the keyboard:  
**ros2 run teleop_twist_keyboard teleop_twist_keyboard** 

You should then see a popup on this terminal with a guide showing you how to control the Turtlebot. I personally set the turn and movement speed closer to 0.31 as anything higher is too unstable to move around in and the odom is 
struggling to keep up.

Finally, to see the door detection program in RViz, simply pull up the image display again change it to:  
**/door_detection/image**

The camera feed should now show any pink vertical lines and blue horizontal lines detected if the lighting and the distances are set correctly. Any regular doors or elevators will be detected if the Turtlebot is around ~5 feet away from the door.

Once you are satisfied with your map (DO NOT CLOSE RVIZ), open one more terminal and source the workspace again. From the root directory, or whereever you want to store your maps, run this command:  
**ros2 run nav2_map_server map_server_cli -f map_name_here**


## Understanding Concepts / Visuals  
My door detection program works in this codebase through the publisher and subscriber method of ROS2's node communication implementations and OpenCV's cv_bridge. By following [this tutorial](https://docs.ros.org/en/kilted/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html) on how publsiher and subscriber nodes talk to each other, I was able to convert my code into a format that could be seen through as a topic.


ROS2 Publisher and Subscriber Model
![alt text](image.png)


## Support
My work email address: jbrandy1@unca.edu  
My personal email adress: jacobbrandyburg@gmail.com


## Authors and acknowledgment
The original owners of the *turtlebot2_ros2* and the *ros2_astra_camera* repositories were Bonolo Mathibela and the Orbbec company


## License
The ROS2 code is under the Apache 2.0 License
