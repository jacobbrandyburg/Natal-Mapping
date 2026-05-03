import cv2
import numpy as np
import rclpy
from rclpy.node import Node

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class DoorDetector(Node):

    def __init__(self):
        super().__init__('door_detector')

        self.publisher_ = self.create_publisher(Image,'/door_detection/image', 10) #Creating the Publisher

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(Image,'/camera/color/image_raw',self.callback, 10) #Creating the Subscriber

    #We will use this function to look for rectangles in a frame that will be identified as certain types of doors
    def callback(self,msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except CvBridgeError as e:
            print(e)
            return

        grayScale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert to grayscale
        blurred = cv2.GaussianBlur(grayScale, (5, 5), 0) # Reduces noise and decreases detailed for finding shapes
        cannyEdges = cv2.Canny(blurred, 50, 150,apertureSize = 3) #Raw images to binary maps finds edges with canny detector
        kernel = np.ones((3, 3), np.uint8) #Check this one again
        cannyEdges = cv2.dilate(cannyEdges, kernel, iterations=1) #I have to change the thickness of the lines to form a rectangle, this can't be done without it
        lines = cv2.HoughLinesP(cannyEdges,2,np.pi/180,100,minLineLength=200,maxLineGap=10) #Dectecting points to form a line

        #The lines to identify in a frame should be stored here 
        horizontal_lines = []
        vertical_lines = [] 

        #The rectangles to be formed
        cornersDetected=[]

        if lines is not None: #If lines are none, it would normally fail and the stream would end. This needs to instead catch this from happening
            for line in lines: 
                x1,y1,x2,y2 = line[0]

                y_diff = y2 - y1 # Number difference between y values
                x_diff = x2 - x1 # Number difference between x values

                length = np.sqrt(x_diff*x_diff + y_diff*y_diff) #Finds the length of the lines

                if length < 100: 
                    continue  # If the lines are too short, skip the comparisons

                #One thing that must change is if a line is found, we want to filter out all the other lines that are too close. Limit lines that have been added to see if they are around 20 pixels apart from any lines in the arrays
                #if the x position of the current line is close to a line that already exists in the array, skip it (20 pixels-ish)

                # Horizontal lines would be lines with both end points having roughly the same y-value
                if (abs(y_diff) < 20): #look for a twenty pixel difference
                    horizontal_lines.append((x1,y1,x2,y2)) #Each line has a size 4 for each part of both coords
                
                # Vertical lines would be lines with both end points having roughly the same x-value
                elif (abs(x_diff) < 20): #look for a twenty pixel difference
                    #Check if a line close to the current line already exists in the array if so skip it
                    too_close = False

                    for old_line in vertical_lines:
                        if abs(x1 - old_line[0]) < 20:
                            too_close = True
                            break

                    if not too_close:
                        vertical_lines.append((x1,y1,x2,y2)) #Each line has a size 4 for each part of both coords

                #This is to show every line in horizontal array
                #for (x1,y1,x2,y2) in horizontal_lines:
                    #cv2.line(frame, (x1,y1),(x2,y2), (255,0,0),2)

                #This is to show every line in vertical array
                #for (x1,y1,x2,y2) in vertical_lines:
                    #cv2.line(frame, (x1,y1),(x2,y2), (255,0,255),2) 

            # I think I need to see if one of the end points of the horizontal lines matches or is very close to one of the vertical lines
            for i, vertical in enumerate(vertical_lines): #Left or Right Side of the Door
                for j, vertical2 in enumerate(vertical_lines): #Left or Right Side of the Door
                    if i >= j:
                        continue
                    
                    for vertical3 in vertical_lines: #Potientially the center of an elevator
                        lineDistance = abs(vertical[0] - vertical2[0]) #pixel x-difference between both vertical lines

                        if not (300 < lineDistance < 400): #We assume that doors are fairly wide when driven up close 300 - ~400ish pixels from how far away the robot is from an adjacent door in the hallway.
                            continue

                        for horizontal in horizontal_lines:
                            horX1 = horizontal[0] #One of the end points of the horz
                            horX2 = horizontal[2] #One of the other ends of the horz

                            leftmostXCoord = min(horX1,horX2) #Find the furthest left x-coord of the horizontal line
                            rightmostXCoord = max(horX1,horX2) #Find the furthest right coord of the horizontal line

                            center = (vertical[0] + vertical2[0]) // 2 #The technical halfway point of the two lines

                            if(leftmostXCoord <= vertical[0] <= rightmostXCoord and leftmostXCoord <= vertical2[0] <= rightmostXCoord): #See if the distance between the both of the lines ...
                                cornersDetected.append((vertical,horizontal,vertical2,vertical3)) #Add to cornerDectected as a potential elevator
                                is_Elevator = False


            # Drawing the Rectangle Bound Box for elevators
            for(vertical,horizontal,vertical2,vertical3) in cornersDetected: #Create a bounding box
                x_left = min(vertical[0], vertical2[0]) # Whichever one is furthest left
                x_right = max(vertical[0],vertical2[0]) # Whichever one is furthest right
                bottom = horizontal[1] 

                #The "elevator" line is being drawn on the right side of the elvator instead of the
                if(center-20 <= vertical3[0] <= center+20):
                    cv2.line(frame, (vertical3[0],vertical3[1]),(vertical3[2],vertical3[3]), (255,0,255),2) #Show where the elevator line is 
                    is_Elevator = True
                #Since I don't need a top, finding halfway of the vertical lines should be a good enough estimate (-1000). Higher than the bottom to give the illusion of the top of the door missing up close

                cv2.rectangle(frame,(x_left, bottom - 1000),(x_right,bottom), (0,255,255), 2)
                # Adding text beside the box 

                if(is_Elevator == True):
                    label = "Elevator"
                    color = (12, 123, 242)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.9
                    thickness = 2
                    text_position = (x_right,bottom)
                    ######
                    frame = cv2.putText(frame, label, text_position, font, font_scale, color, thickness, cv2.LINE_AA)

                else:
                    label = "Door"
                    color = (222, 117, 117)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.9
                    thickness = 2
                    text_position = (x_right,bottom)
                    #####
                frame = cv2.putText(frame, label, text_position, font, font_scale, color, thickness, cv2.LINE_AA)

        try:
            return_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher_.publish(return_msg)
        except CvBridgeError as e:
            print(e)

        return frame


def main(args= None):
    rclpy.init(args=args)

    detector = DoorDetector()
    rclpy.spin(detector)

    detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
