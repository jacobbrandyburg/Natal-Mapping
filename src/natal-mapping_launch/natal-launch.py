from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

# This is the launch file for the Natal-Mapping project. This should properly boot up the Kobuki_Node, Camera,
# Map, Turtlebot_Description and Scan

#The teleop, and base_to_camera commands should be run in separate terminals

## (**) means done, I think


def generate_launch_description():

    ####### Files that launch with "launch" (ros2 launch) need to be launched with IncludeLaunchDescription #######

    #Starting up the Kobuki_node (**)
    kobuki_node = IncludeLaunchDescription(
        PathJoinSubstitution([
                FindPackageShare('kobuki_node'),
                'launch',
                'kobuki_node-launch.py'
        ])
    )

    #Starting up the Astra Camera (**)
    camera_astra = IncludeLaunchDescription(
        PathJoinSubstitution([
                FindPackageShare('astra_camera'),
                'launch',
                'astra.launch.xml'
        ])
    )

    #Starting up the Map (**)
    slam_tool = IncludeLaunchDescription(
        PathJoinSubstitution([
                FindPackageShare('slam_toolbox'),
                'launch',
                'online_async_launch.py'
        ])
    )

    #Starting up the Turtlebot_Description (need to add the gui:=False agrument)
    turtlebot = IncludeLaunchDescription(
        PathJoinSubstitution([
                FindPackageShare('turtlebot_description'),
                'launch',
                'display.launch.py'
        ]),
        launch_arguments={
                'gui':'False'
        }.items()
    )

    return LaunchDescription([

        #Nodes to launch
        kobuki_node,
        camera_astra,
        slam_tool,
        turtlebot,

        ####### Files that launch with "run" (ros2 run) need to be launched with Node #######

        #Depthimage_to_laserscan **
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan',
            remappings=[('depth', '/camera/depth/image_raw'),
                        ('depth_camera_info', '/camera/depth/camera_info'),
                        ('scan','/scan')],
            parameters=[
                {'qos_overrides./depth.subscriber.reliability':'best_effort'},
                {'scan_height':1}]
        ),

        #Base_to_Camera **
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_camera',
            arguments=['0','0','0.2','0','0','0','base_link','camera_link']
        ),

	#Door_Detection
	Node(
	    package='door_detection',
    	    executable='door_detection',
            name='door_detection',
            output='screen'
	),

    ])
