import os
import tensorflow as tf
import cv2
import numpy as np
from object_detection.utils import label_map_util
import base64

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging (1)


class Predictor:
    def __init__(self):
        self.uri = None
        PATH_TO_SAVED_MODEL = "saved_model/"
        PATH_TO_LABELS = 'labelmap.pbtxt'
        # self.uri = uri
        self.detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
        self.category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

    def readb64(self):
        nparr = np.frombuffer(base64.b64decode(self.uri), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    def predict(self, uri):
        self.uri = uri
        uri = base64.b64encode(open("161.jpg", "rb").read())
        image = self.readb64()

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_expanded = np.expand_dims(image_rgb, axis=0)

        input_tensor = tf.convert_to_tensor(image)

        input_tensor = input_tensor[tf.newaxis, ...]

        detections = self.detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))

        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}

        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        captcha_arr = []

        for label, score, box in zip(detections['detection_classes'], detections['detection_scores'],
                                     detections['detection_boxes']):
            if score > 0.7:
                mid_x = (box[1] + box[2]) / 2
                captcha_arr.append((self.category_index[label]['name'], score, mid_x))

        print('Done')

        pos_arr = [i for _, _, i in captcha_arr]

        temp_dict = {}

        for label, score, box in captcha_arr:
            temp_dict[box] = label

        pos_arr.sort()

        result = ""
        for i in pos_arr:
            result = result + temp_dict[i]

        print()
        print("The captcha code is ----", result)
        return result
