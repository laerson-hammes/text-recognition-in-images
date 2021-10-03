# https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
# https://github.com/UB-Mannheim/tesseract/wiki
# pip install opencv-python
# pip install pytesseract
import pytesseract # type: ignore
import cv2 # type: ignore
import argparse
import requests
import os


IMAGE_TEMP_DIRECTORY: str = "C:\\Windows\\Temp\\download.png"
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Laerson\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"


class TextRecognize(object):
   """
   This class is responsible for reading the image and extracting the text from it
   """
   def __init__(self, arguments: argparse.Namespace, /) -> None:
      self.arguments: argparse.Namespace = arguments
      self.image_content: bytes = b""
   
   
   def recognize(self, image_path: str, /) -> str:
      """
      This function read a image and return the extracted text
      :param image_path: image path to extract text
      :return extracted text
      """
      image = cv2.imread(image_path)
      return pytesseract.image_to_string(image)
   
   
   def get_image(self, url: str, /) -> bool:
      """
      This function get a image from the given URL
      :param url: URL to get the image
      :return bool: return True if it was possible to get the image or False if an error occurred
      """
      try:
         r = requests.get(url)
         self.image_content = r.content
         return True
      except:
         return False
      
   
   def save_image(self, /) -> None:
      """
      This function save the image content in a image in the windows temp directory
      """
      with open(IMAGE_TEMP_DIRECTORY, "wb") as image:
         image.write(self.image_content)
   
   
   def execute(self, /) -> str:
      """
      This function is responsible for taking the argument passed on the command
      line and executing the functions responsible for text recognition
      :return image extracted text or error 
      """
      if self.arguments.path:
         return self.recognize(self.arguments.path)
      elif self.get_image(self.arguments.url):
         self.save_image()
         image_text: str = self.recognize(IMAGE_TEMP_DIRECTORY)
         os.remove(IMAGE_TEMP_DIRECTORY)
         return image_text
      return "An error occurred during the process"

   
def get_arguments() -> argparse.Namespace:
   """
   This function get command line arguments
   :return the arguments
   """
   parser = argparse.ArgumentParser()
   parser.add_argument("-p", "--path", dest="path", help="Relative or absolute image path from which you want to extract text")
   parser.add_argument("-u", "--url", dest="url", help="Url image from which you want to extract text")
   return parser.parse_args()
   
   
def main():
   """
   This function is responsible for checking the command line arguments
   """
   arguments: argparse.Namespace = get_arguments()
   if arguments.url or arguments.path:
      tr: TextRecognize = TextRecognize(arguments)
      text: str = tr.execute()
      print(text)
   else:
      print("You must specify a image path or a image url...")
      print("Use py .\\text-recognition-in-images.py -h to get help...")  

      
if __name__ == '__main__':
   main()