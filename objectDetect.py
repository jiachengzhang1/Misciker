import io, os
import cv2
from google.cloud import vision
from google.cloud.vision import types


# define the checklist
check_list = ['Wallet', 'Key']
num_item = len(check_list)

# use camera to take photo of the item
# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()
# out = cv2.imwrite('capture.jpg', frame) # save the photo to current directory

# cap.release()
# cv2.destroyAllWindows()


# pass the photo to the google cloud label detection API, and fetch the prediction
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"GoogleVision.json"
client = vision.ImageAnnotatorClient()

print(client)

file_name = 'image3.jpg'
image_path = os.path.join('/Users/jiachengzhang/Desktop/GoogleVision/GoogleVision', file_name)

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.label_detection(image=image)
labels = response.label_annotations

# print(response)

for label in labels:
    if label.description in check_list:
        num_item = num_item - 1
        print(label.description)
        break
    print(label.description)

print(num_item)