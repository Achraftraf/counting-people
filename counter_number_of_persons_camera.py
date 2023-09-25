import cv2

import time

import numpy as np

# load the COCO class names

def init(confid=0.4,x=300,y=300):
    # load the COCO class names
    with open(r"COCO_labels.txt", 'r') as f:
        class_names = f.read().split('\n')

    # get a different color array for each of the classes
    COLORS = np.random.uniform(0, 255, size=(len(class_names), 3))

    # load the DNN model
    model = cv2.dnn.readNet(model='C:\\Users\\Administrator\\Desktop\\M2I-Zarouki-Achraf-OpenCV.zip\\frozen_inference_graph_V2.pb',
                        config='C:\\Users\\Administrator\\Desktop\\M2I-Zarouki-Achraf-OpenCV.zip\\ssd_mobilenet_v2_coco_2018_03_29.pbtxt.txt',
                        framework='TensorFlow')

    # capture the video

    cap = cv2.VideoCapture(0)

    # cap = cv2.VideoCapture(4)

    # get the video frames' width and height for proper saving of videos
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # create the `VideoWriter()` object
    out = cv2.VideoWriter('C:\\Users\\Administrator\\Desktop\\people_counting\\camera\\results_of_counting\\video_after_counting.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30,
                          (frame_width, frame_height))
    cv2.namedWindow("camera")
    # detect objects in each frame of the video
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            image = frame
            image_height, image_width, _ = image.shape
            # create blob from image
            blob = cv2.dnn.blobFromImage(image=image, size=(x, y), mean=(104, 117, 123),
                                         swapRB=True)
            # start time to calculate FPS
            start = time.time()
            model.setInput(blob)
            output = model.forward()
            # end time after detection
            end = time.time()
            # calculate the FPS for current frame detection
            fps = 1 / (end - start)
            """ count  """
            # Count number of persons
            count_person = 0

            """ count number  """
            # loop over each of the detections
            id_pers = 0
            for detection in output[0, 0, :, :]:
                id_pers += 1

                # extract the confidence of the detection
                confidence = detection[2]
                # draw bounding boxes only if the detection confidence is above...
                # ... a certain threshold, else skip
                if confidence > confid:
                    # get the class id
                    class_id = detection[1]
                    # map the class id to the class
                    class_name = class_names[int(class_id) - 1]
                    """ tester si l'objet est un person """
                    if (class_name == "person"):
                        count_person += 1
                        class_name = "Person " + str(id_pers)
                        color = COLORS[int(class_id)]
                        # get the bounding box coordinates
                        box_x = detection[3] * image_width
                        box_y = detection[4] * image_height
                        # get the bounding box width and height
                        box_width = detection[5] * image_width
                        box_height = detection[6] * image_height
                        # draw a rectangle around each detected object
                        cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color,
                                      thickness=2)
                        # put the class name text on the detected object
                        cv2.putText(image, class_name, (int(box_x), int(box_y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                        # put the FPS text on top of the frame
                        cv2.putText(image, f"{fps:.2f} FPS", (1000, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                    cv2.LINE_AA)

            # put the number of persons on right top of the frame
            """ text position color """
            """         cv2.putText(image, f"number of persons:{count_person} ", (20, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0 ,255), 2) """
            # Get the size of the text
            text_size = cv2.getTextSize(f"{count_person} Persons", cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

            # Calculate the position of the text
            text_x = 20
            text_y = 30

            # Calculate the position of the rectangle
            rect_x = text_x - 5
            rect_y = text_y - text_size[1] - 5
            rect_width = text_size[0] + 10
            rect_height = text_size[1] + 10

            # Draw the rectangle
            cv2.rectangle(image, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), -1)

            # Draw the text on top of the rectangle
            cv2.putText(image, f"Persons: {count_person}", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2, cv2.LINE_AA)
            if cv2.getWindowProperty('camera', cv2.WND_PROP_VISIBLE) < 1:
                break
            cv2.imshow("camera", image)
            out.write(image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()

def closeWin():
    global cv2
    cv2.destroyAllWindows()