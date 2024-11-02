import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

list_of_names = []


def delete_old_data():
   for i in os.listdir("generated-certificates/"):
      os.remove("generated-certificates/{}".format(i))


def cleanup_data():
   with open('name-data.txt') as f:
      for line in f:
          list_of_names.append(line.strip())


def generate_certificates():

   for index, name in enumerate(list_of_names):
        try:
            certificate_template_image = cv2.imread("./certificate_template.png")
            top_left = (441, 645)
            bottom_right = (1520, 779 )

            cv2.putText(certificate_template_image, name.strip(), (815,1500), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 250), 5, cv2.LINE_AA)

            # Convert OpenCV image to PIL format for custom font usage
            certificate_pil = Image.fromarray(certificate_template_image)

            font_path = "./ShadeBlueFont.ttf" 
            font = ImageFont.truetype(font_path, 125)

            # Create a drawing context
            draw = ImageDraw.Draw(certificate_pil)

            # Calculate text size and position it in the middle of the box
            # Get bounding box of the text, which returns (left, top, right, bottom)
            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            text_x = top_left[0] + (bottom_right[0] - top_left[0] - text_width) // 2
            text_y = top_left[1] + (bottom_right[1] - top_left[1] - text_height) // 2

            # Draw the name text in black color
            draw.text((text_x, text_y), name, fill="black", font=font)

            # Convert back to OpenCV format
            certificate_template_image = cv2.cvtColor(np.array(certificate_pil), cv2.COLOR_RGB2BGR)
            cv2.imwrite("generated-certificates/{}.jpg".format(name.strip()), certificate_template_image)
            print("Processing {} / {}".format(index + 1,len(list_of_names)))
        except Exception as e:
            print("Error: ", e)
            raise e
            # print("Error in processing {}".format(name.strip()))
def main():
   delete_old_data()
   cleanup_data()
   generate_certificates()

if __name__ == '__main__':
   main()
