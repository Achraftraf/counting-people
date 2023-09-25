import cv2
import numpy as np

def init(path="",confid=0.4,x=300,y=300):
    if(path == ""):
        return
    # load the COCO class names
    with open('COCO_labels.txt', 'r') as f:
        class_names = f.read().split('\n')
    # get a different color array for each of the classes
    COLORS = np.random.uniform(0, 255, size=(len(class_names), 3))

    class_names

    #Nous allons charger le MobileNet modèle SSD à l'aide de la fonction readNet()
    model = cv2.dnn.readNet(model='frozen_inference_graph_V2.pb',
                            config='ssd_mobilenet_v2_coco_2018_03_29.pbtxt.txt',
                            framework='TensorFlow')

    #Ensuite, nous allons lire l'image à partir du disque et de préparer l'entrée de fichier blob(pretraitement).
    # read the image from disk
    image = cv2.imread(r"" + path)

    image_height, image_width, _ = image.shape
    # create blob from image
    # We specify the size to be 300×300 as this the input size that SSD models generally expect in almost all frameworks.
    # We are using the swapRB because the models generally expect the input to be in RGB format.
    blob = cv2.dnn.blobFromImage(image=image, size=(x, y), mean=(104, 117, 123), swapRB=True)
    # set the input to the pre-trained deep learning network and obtain
    # the output predicted probabilities for label
    # classes
    model.setInput(blob)
    output = model.forward()
    count_person=0

    """ count number  """
    # loop over each of the detections
    id_pers=0
    for detection in output[0, 0, :, :]:
        id_pers+=1

        # extract the confidence of the detection
        confidence = detection[2]
        # draw bounding boxes only if the detection confidence is above a certain threshold, else skip
        if confidence > confid :
            # get the class id
            class_id = detection[1]
            # map the class id to the class
            class_name = class_names[int(class_id)-1]
            if(class_name=="person"):
                    count_person+=1
                    class_name="       "
                    color = COLORS[int(class_id)]
                    # get the bounding box coordinates
                    box_x = detection[3] * image_width
                    box_y = detection[4] * image_height
                    # get the bounding box width and height
                    box_width = detection[5] * image_width
                    box_height = detection[6] * image_height
                    # draw a rectangle around each detected object
                    cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=4)
                    # put the FPS text on top of the frame
                    cv2.putText(image, class_name, (int(box_x), int(box_y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(image, f"number of persons:{count_person} ", (20, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0 ,255), 2)
    cv2.imshow('image', image)
    cv2.imwrite('C:\\Users\\Administrator\\Desktop\\image_result.jpg', image)

def closeWin():
    global cv2
    cv2.destroyAllWindows()