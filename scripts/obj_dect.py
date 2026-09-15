# Python libs
import rclpy
from rclpy.node import Node
from rclpy import qos

# OpenCV
import cv2

# ROS libraries
import image_geometry
from tf2_ros import Buffer, TransformListener

# ROS Messages
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge, CvBridgeError
from tf2_geometry_msgs import do_transform_pose

class ObjectDetector(Node):
    camera_model = None
    image_depth_ros = None
    visualisation = True
    # aspect ration between color and depth cameras
    # calculated as (color_horizontal_FOV/color_width) / (depth_horizontal_FOV/depth_width) from the dabai camera parameters
    color2depth_aspect = 1.0 # for a simulated camera

    def __init__(self):    
        super().__init__('image_projection_3')
        self.bridge = CvBridge()
        self.centroid_set = set()

        self.camera_info_sub = self.create_subscription(CameraInfo, '/limo/depth_camera_link/camera_info',
                                                self.camera_info_callback, 
                                                qos_profile=qos.qos_profile_sensor_data)
        
        self.object_location_pub = self.create_publisher(PoseStamped, '/limo/object_location', 10)

        self.image_sub = self.create_subscription(Image, '/limo/depth_camera_link/image_raw', 
                                                  self.image_color_callback, qos_profile=qos.qos_profile_sensor_data)
        
        self.image_sub = self.create_subscription(Image, '/limo/depth_camera_link/depth/image_raw', 
                                                  self.image_depth_callback, qos_profile=qos.qos_profile_sensor_data)
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def get_tf_transform(self, target_frame, source_frame):
        try:
            transform = self.tf_buffer.lookup_transform(target_frame, source_frame, rclpy.time.Time())
            return transform
        except Exception as e:
            self.get_logger().warning(f"Failed to lookup transform: {str(e)}")
            return None

    def camera_info_callback(self, data):
        if not self.camera_model:
            self.camera_model = image_geometry.PinholeCameraModel()
        self.camera_model.fromCameraInfo(data)

    def image_depth_callback(self, data):
        self.image_depth_ros = data

    def image_color_callback(self, data):
        # wait for camera_model and depth image to arrive
        if self.camera_model is None:
            return

        if self.image_depth_ros is None:
            return

        # covert images to open_cv
        try:
            image_color = self.bridge.imgmsg_to_cv2(data, "bgr8")
            image_depth = self.bridge.imgmsg_to_cv2(self.image_depth_ros, "32FC1")
        except CvBridgeError as e:
            print(e)        
        
        hsv_mask = cv2.cvtColor(image_color, cv2.COLOR_BGR2HSV)
        
        image_mask = cv2.inRange(hsv_mask, (140, 50, 50), (180, 255, 255))

        contours,_ = cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.centroid_set.clear()
        distinct_potholes = 0
        
       

        for cnt in contours:
            
            
            cv2.drawContours(image_color, cnt, -1, (0, 255, 0), 2)
            
            # calculate moments of the binary image
            M = cv2.moments(image_mask)
            area = cv2.contourArea(cnt) 
            # Convert the area from pixels to a real-world unit of measurement (e.g. cm^2) 
            scale_factor = 0.1 # 1 pixel = 0.1 cm 
            size = area * scale_factor
            
            # Print the size of the object 
            #print('Size:', size) 
            
           
            # cx= int(M["m01"] / M["m00"])
            # cy= int( M["m10"] / M["m00"])

            if M["m00"] == 0:
                print('No object detected.')
                return
        
            # calculate the y,x centroid
            image_coords = (M["m01"] / M["m00"], M["m10"] / M["m00"])
            x = int(M["m01"] / M["m00"])
            y = int(M["m10"] / M["m00"])
            self.centroid_set.add((x,y))
            distinct_potholes = len(self.centroid_set)
            cv2.putText(image_color, f"{round(size, 3)}", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)

            # "map" from color to depth image
            depth_coords = (image_depth.shape[0]/2 + (image_coords[0] - image_color.shape[0]/2)*self.color2depth_aspect, 
                image_depth.shape[1]/2 + (image_coords[1] - image_color.shape[1]/2)*self.color2depth_aspect)
            # get the depth reading at the centroid location
            depth_value = image_depth[int(depth_coords[0]), int(depth_coords[1])] # you might need to do some boundary checking first!

            # print('image coords: ', image_coords)
            # print('depth coords: ', depth_coords)
            # print('depth value: ', depth_value)

            # calculate object's 3d location in camera coords
            camera_coords = self.camera_model.projectPixelTo3dRay((image_coords[1], image_coords[0])) #project the image coords (x,y) into 3D ray in camera coords 
            camera_coords = [x/camera_coords[2] for x in camera_coords] # adjust the resulting vector so that z = 1
            camera_coords = [x*depth_value for x in camera_coords] # multiply the vector by depth

            print('camera coords: ', camera_coords)

            #define a point in camera coordinates
            object_location = PoseStamped()
            object_location.header.frame_id = "depth_link"
            object_location.pose.orientation.w = 1.0
            object_location.pose.position.x = camera_coords[0]
            object_location.pose.position.y = camera_coords[1]
            object_location.pose.position.z = camera_coords[2]

            # publish so we can see that in rviz
            self.object_location_pub.publish(object_location)        

            # print out the coordinates in the odom frame
            transform = self.get_tf_transform('depth_link', 'odom')
            p_camera = do_transform_pose(object_location.pose, transform)

            print('odom coords: ', p_camera.position)
            
        print(f'Pothole Count: {distinct_potholes}')
        cv2.imshow("image color", image_color)
        cv2.waitKey(1)

        # if self.visualisation:
        #     # draw circles
        #     cv2.circle(image_color, (int(image_coords[1]), int(image_coords[0])), 10, 255, -1)
        #     cv2.circle(image_depth, (int(depth_coords[1]), int(depth_coords[0])), 5, 255, -1)

        #     #resize and adjust for visualisation
        #     image_color = cv2.resize(image_color, (0,0), fx=0.5, fy=0.5)
        #     image_depth *= 1.0/10.0 # scale for visualisation (max range 10.0 m)

        #     cv2.imshow("image depth", image_depth)
        #     cv2.imshow("image color", image_color)
        #     cv2.waitKey(1)

def main(args=None):

    rclpy.init(args=args)
    image_projection = ObjectDetector()
    rclpy.spin(image_projection)
    # print(f'Pothole Count: {contour_count}')
    image_projection.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
