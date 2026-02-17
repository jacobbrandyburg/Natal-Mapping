import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros

import os

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='turtlebot_description').find('turtlebot_description')
    default_model_path = os.path.join(pkg_share, 'robots/kobuki_hexagons_hokuyo.urdf.xacro') #Changed from hokuyo to astra
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )
    #Adding this node for launching depthimage_to_laserscan
    #depthimage_to_laserscan = launch_ros.actions.Node(
#	package='depthimage_to_laserscan',
#	executable='depthimage_to_laserscan_node',
#	name='depthimage_to_laserscan',
#	remappings=[('depth', '/camera/depth/image_rect_raw'),
#                        ('depth_camera_info', '/camera/depth/camera_info')],
#   	parameters=[param_config])
    ###


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                            description='Flag to enable joint_state_publisher_gui'),
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
#	launch.actions.DeclareLaunchArgument(name='depthimage_to_laserscan',
#					    description='Setting the depthimage_to_laserscan'),

	joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node,
 #       depthimage_to_laserscan
    ])
