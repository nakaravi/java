#using openCV
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'c:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('more.png')
text = pytesseract.image_to_string(img)
print(text)

print("*****************************")
#crop_img = img[y:y+h, x:x+w]
crop_img = img[150:220, 800:1200]	
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)

#img1 = cv2.imread(crop_img)

text = pytesseract.image_to_string(crop_img)
print(text)

