# Natal-Mapping: Turtlebot Grid Occupancy Maps for Building Navigation


## About Natal Mapping
Transitioning to a new campus as a college freshman can be very stressful, especially when figuring out the best route to get to all your classes on time. If the school is large enough, a student may be given a map showing the physical locations of the buildings relative to one another, but the problem doesn’t end there. Upon entering a new building, students will promptly seek room numbers to orient themselves, a process that can be straightforward or disorienting. A mall kiosk displaying the floor plan of neighboring stores, bathrooms, and escalators is a great example of how to solve this problem. Building a map with a similar structure on a bulletin board near a building's entrances would be ideal, but doing so from scratch could be very tedious and may lack accuracy. With Natal Mapping, this could be done in a fraction of the time.

Natal Mapping is the collaborative effort of both the Robot Operating System’s environment visualizer tool (RViz) and a door detection program made from the Probabilistic Houghlines Transform algorithm to build a floor map and classify rooms based on the geometric structure of the door at the same time. The door detection process works by filtering lines from geometric shapes in the camera feed and highlighting the ones that form the basic shapes of a door or elevator. Both tools determine the layout based on the relative positions of classrooms, bathrooms, and elevators during map construction. 
With color-coordinated post-processing, these maps can then be printed out onto large posters or bulletin boards placed near building entrances or next to stairs, elevators, or anywhere where anyone enters a new floor.

The ROS visualizer works off of a Turtlebot model 2e's LiDAR camera and for this project, I went through the process of searching for the correct drivers from ROS Github repositories to find if anyone has started the process of creating drivers that works for specifically the 2e model. This capstone project was also, in part, a passion project for me to learn more about robot software development. A good portion of this assignment was learning ROS, finding drivers, learning the Ubuntu Linux interface and how to manually build and manage packages from source. Somethings might be unorganized, but I will be actively working to polish things up as time continues on.


## Getting started and Setup

This repository has all the drivers needed for running the Turtlebot model 2e with a Kobuki base in specifically the short-term distribution of ROS2, Kilted Kaiju. Some packages may need to be built, so please follow this step-by-step instruction for doing so.

This is also made, in part by ________ in they're turtlebot2 ROS2 repo https://github.com/idorobotics/turtlebot2_ros2. They suggest also following these commands on both the docked and workstation laptop:

This repository will store the code for a ROS2 workspace that will allow the model, Turtlebot 2e, to work in ROS2. This repository also takes the Kobuki base code from the *Idorobotics: Turtlebot2_ROS2* repository and the Astra camera it uses from the *Orbbec: OrbbecSDK_ROS2* repository.

Make sure before SSH-ing into the netbook that both the docked netbook and the control station device are both on the same network. 
- *ssh -XC netbookname@ipaddress*

This project's launch file (natal-launch.py) is made up of many different programs and separate launch files. Those being:
- kobuki_node: Turns on the Kobuki base
- camera_astra: Turns on the Astra Camera
- slam_tool: Boots up RViz
- turtlebot: All the components to build the Turtlebot description model in RViz
- Depthimage_to_laserscan: Turns on the actual scan topic for observing the environment and building the map
- Base_to_Camera: Attaching the camera to the base link of the Turtlebot description model
- Door_Detection: Door detection program

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

The camera feed should now show any pink vertical lines and blue horizontal lines detected if the lighting and the distances are set correctly. Any regular doors or elevators will be detected if the Turtlebot is around 5 feet away from the door.

Once you are satisfied with your map (DO NOT CLOSE RVIZ), open one more terminal and source the workspace again. From the root directory, or whereever you want to store your maps, run this command:  
**ros2 run nav2_map_server map_server_cli -f map_name_here**


## Understanding Concepts / Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.


ROS2 Publisher and Subscriber Model
![alt text](image.png)


## Support
My work email address: jbrandy1@unca.edu  
My personal email adress: jacobbrandyburg@gmail.com


## Authors and acknowledgment
The original owners of the *turtlebot2_ros2* and the *ros2_astra_camera* repositories were Bonolo Mathibela and the Orbbec company


## License
The ROS2 code is under the Apache 2.0 License
