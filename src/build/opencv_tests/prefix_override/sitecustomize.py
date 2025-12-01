import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/jacob/ROS2_WORKSPACES/Natal/src/install/opencv_tests'
