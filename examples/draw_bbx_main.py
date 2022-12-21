import cv2
import os
from PIL import Image

#import pic_augmenter

class BoundingBoxWidget(object):
    def __init__(self,input_pic):
        self.original_image = cv2.imread(input_pic)
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
        self.image_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            print('top left: {}, bottom right: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
            print('x,y,w,h : ({}, {}, {}, {})'.format(self.image_coordinates[0][0], self.image_coordinates[0][1], self.image_coordinates[1][0] - self.image_coordinates[0][0], self.image_coordinates[1][1] - self.image_coordinates[0][1]))
            pic_cropper(self.image_coordinates[0][0], self.image_coordinates[0][1], self.image_coordinates[1][0] - self.image_coordinates[0][0], self.image_coordinates[1][1] - self.image_coordinates[0][1], self.image_coordinates[0], self.image_coordinates[1])

            # Draw rectangle 
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone) 

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        return self.clone

def draw_bbx_MAIN(input_pic):
    boundingbox_widget = BoundingBoxWidget(input_pic)
    while True:
        cv2.imshow('image', boundingbox_widget.show_image())
        key = cv2.waitKey(1)

        #WRITE boundingbox_widget.show_image() TO A DIRECTORY AND GET THE FILE ON LINE 64


        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)

def pic_cropper( x, y, w, h, top_left_point, bottom_right_point):
    print("cr")
    print( x, y, w, h, top_left_point, bottom_right_point)

    #Cropping code source: https://www.geeksforgeeks.org/python-pil-image-crop-method/
    # Importing Image class from PIL module
    #from PIL import Image
    
    # Opens a image in RGB mode
    im = Image.open(r"../captured_frames_folder/frame20sec.jpg")
    print("hhhh")
    
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    # width, height = im.size
    
    # Setting the points for cropped image
    # left = 5
    
    # top = height / 4
    # right = 164
    # bottom = 3 * height / 4
    
    # Cropped image of above dimension
    # (It will not change original image)


 
    im1 = im.crop((top_left_point[0], top_left_point[1], bottom_right_point[0], bottom_right_point[1]))
    
    # Source: https://www.tutorialspoint.com/python_pillow/python_pillow_cropping_an_image.htm
    #Save the cropped image
    #im1.save("examples/output_frames")
    
    #Now that we have saved the cropped image to a folderw the next move is to send it to the auto_augment_pic function.
    
    # Shows the image in image viewer
    im1.show()
   # pic_augmenter.run_auto_augmenter()
    
