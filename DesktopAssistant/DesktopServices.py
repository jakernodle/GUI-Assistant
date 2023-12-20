
import pyautogui
import numpy as np
import os
import cv2
import time
from Quartz import CGDisplayBounds, CGMainDisplayID
import pytesseract

def _get_scaling_factor():
    # Get screenshot dimensions
    screenshot = pyautogui.screenshot()
    screenshot_width, screenshot_height = screenshot.size

    # Get the main display ID and its bounds
    main_display_id = CGMainDisplayID()
    display_bounds = CGDisplayBounds(main_display_id)
    display_width = display_bounds.size.width

    # Calculate scaling factor
    scaling_factor = screenshot_width / display_width
    return scaling_factor

def _extract_pixel_vals(xyxyn, original_image):
    # Extract the coordinates
    numpy_array = xyxyn.numpy()[0]
    x1, y1, x2, y2 = numpy_array[0], numpy_array[1], numpy_array[2], numpy_array[3]
    
    # Convert normalized coordinates to pixel values
    height, width, _ = original_image.shape

    # return pixel vals from image
    return int(x1 * width), int(y1 * height), int(x2 * width), int(y2 * height)

def extract_desktop_coordinates_from_bounding_box(xyxyn, screenshot):
    
    pixel_x1, pixel_y1, pixel_x2, pixel_y2  = _extract_pixel_vals(xyxyn, screenshot)
    #scaling factor for desktop resolution
    scaling_factor = _get_scaling_factor()

    # Adjust coordinates for the display scaling factor
    return int(pixel_x1 / scaling_factor), int(pixel_y1 / scaling_factor), int(pixel_x2 / scaling_factor), int(pixel_y2 / scaling_factor)

def crop_image_with_box(xyxyn, image):
    
    x1, y1, x2, y2  = _extract_pixel_vals(xyxyn, image)
    
    return image[y1:y2, x1:x2]

def click(coordinates):
    # Move the mouse to the coordinate
    pyautogui.moveTo(x=coordinates[0], y=coordinates[1], duration=0.4)  # Move the mouse over 1 second

    # Click at the coordinate
    pyautogui.click(x=coordinates[0], y=coordinates[1], button='left')

def take_screenshot():
    # Take a screenshot using pyautogui
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a numpy array for saving
    frame = np.array(screenshot)

    # Convert it from BGR to RGB (OpenCV uses BGR by default)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Define the folder path
    folder_path = 'screenshots'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the screenshot with the timestamp as its name
    cv2.imwrite('./last_screenshot.png', frame)
    
    # sleep whil image is saved
    time.sleep(0.5)

    # return the image
    return cv2.imread('./last_screenshot.png')

# Function to perform OCR
def perform_ocr(image):
    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image)

    return text

def type_text(text):
    pyautogui.typewrite(text, interval=0.025)