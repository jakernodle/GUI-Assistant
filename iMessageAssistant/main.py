from ultralytics import YOLO
import time
from DesktopAssistant.GPTServices import respond_to_message_thread
from DesktopAssistant.DesktopServices import extract_desktop_coordinates_from_bounding_box, crop_image_with_box, click, take_screenshot, perform_ocr, type_text

# After initialization the iMessage assistant class should be able to perform tasks with simple function calls
class iMessageAssistant:

    _exposed_functions_description = """
    name:respond_to_unread_messages
    description:Send responses to all visible unread message threads.
    """

    unread_messages_coordinates = []
    message_box_coordinates = []

    def __init__(self, window_screenshot):

        #run inference on screenshot
        predictions = self.run_inference(window_screenshot)

        #get click coordinates for 
        self.set_class_coordinates(predictions,window_screenshot)

    def run_inference(self, window_screenshot):

        # Load model
        model = YOLO('./iMessageAssistant/iMessage_GUI_Object_Detection/weights/best.pt')

        # Run inference
        results = model(window_screenshot)

        # get predictions
        return results[0].boxes

    def set_class_coordinates(self, predictions, window_screenshot):
        for prediction in predictions:
            #igrnore low confidence predictions
            if prediction.conf < 0.5:
                continue

            #get the class of the prediction
            class_mapping = ["message box", "recipients", "thread", "unread message"]
            mapped = class_mapping[int(prediction.cls[0].item())]

            #save classes
            if mapped == class_mapping[3]:
                x1, y1, x2, y2 = extract_desktop_coordinates_from_bounding_box(prediction.xyxyn, window_screenshot)
                self.unread_messages_coordinates.append([(x1+x2)/2,(y1+y2)/2])

            if mapped == class_mapping[0]:
                x1, y1, x2, y2 = extract_desktop_coordinates_from_bounding_box(prediction.xyxyn, window_screenshot)
                self.message_box_coordinates = [(x1+x2)/2,(y1+y2)/2]


    ##CLICK ON UNREAD MESSAGES, CLICK ON MESSAGE BOX, READ THEIR CHATS, AND TYPE A RESPONSE
    def respond_to_unread_messages(self):
        for click_location in self.unread_messages_coordinates:
            click(click_location)
            time.sleep(1)
            click(click_location)
            time.sleep(1)
            click(self.message_box_coordinates)
            time.sleep(.4)
            new_screenshot = take_screenshot()
            
            # Run inference
            predictions = self.run_inference(new_screenshot)

            for result in predictions:
                if result.conf < 0.5:
                    continue
            
                class_mapping = ["message box", "recipients", "thread", "unread message"]
                mapped = class_mapping[int(result.cls[0].item())]

                if mapped == class_mapping[2]:
                    # Crop the image
                    cropped_image = crop_image_with_box(result.xyxyn, new_screenshot)
                    # run ocr on the image
                    ocr_text = perform_ocr(cropped_image)
                    #respond to the message
                    gpt_response = respond_to_message_thread(ocr_text)
                    type_text(gpt_response)
