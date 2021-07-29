import csv, os
import cv2 
import numpy as np 

f = open('eight.csv', 'w', encoding='utf-8', newline='')
wf = csv.writer(f)

filename = 'eight.jpg' 
src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) 
src = cv2.resize(src , (int(src.shape[1]*0.34), int(src.shape[0]*0.17))) #이미지가 작아서 크기 키워서 확인

#이진화
ret, binary = cv2.threshold(src, 170, 255, cv2.THRESH_BINARY_INV)

#노이즈 제거
binary = cv2.morphologyEx(binary , cv2.MORPH_OPEN , cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2)), iterations = 2)

#외곽선 검출
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
color = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR) 

bR_arr = []
for i in range(len(contours)) : 
    x,y,w,h = cv2.boundingRect(contours[i])
    if w < 10 and h < 10 : continue
    bR_arr.append([x, y, w, h])

#x값을 기준으로 배열을 정렬 
bR_arr = sorted(bR_arr, key=lambda num : num[0], reverse = False)

del bR_arr[1]
del bR_arr[1]
bR_arr.append([51, 179, 120, 120])
del bR_arr[3];del bR_arr[3];del bR_arr[3]
del bR_arr[3]
del bR_arr[4]
bR_arr.append([189, 34, 120, 108])

del bR_arr[3]
del bR_arr[4];del bR_arr[5]
del bR_arr[5]
bR_arr.append([201, 339, 132, 108])

del bR_arr[4]
del bR_arr[4]
bR_arr.append([234, 473, 85, 83])
del bR_arr[4];del bR_arr[4]

del bR_arr[6];del bR_arr[6]
del bR_arr[4]
del bR_arr[6]
bR_arr.append([344, 335, 120, 113])

del bR_arr[5]
del bR_arr[6]
bR_arr.append([356, 174, 106, 109])

del bR_arr[5]
del bR_arr[5]
bR_arr.append([367, 474, 80, 74])
del bR_arr[5];del bR_arr[5];del bR_arr[5];del bR_arr[5];del bR_arr[5]

del bR_arr[6]
del bR_arr[6];del bR_arr[6]
bR_arr.append([489, 328, 97, 107])

del bR_arr[7];del bR_arr[8];del bR_arr[8];del bR_arr[8];del bR_arr[8]

col, row, _ = color.shape
row -= 1; col -= 1
for i in range(16) : 
    x, y, w, h = bR_arr[i][0], bR_arr[i][1], bR_arr[i][2], bR_arr[i][3]
    wf.writerow(['image4001', 'freeform', '/m/0eight', 1 , x/row, (x+w)/row, y/col, (y+h)/col, 0, 0, 0, 0, 0, '/m/0eight', 'Eight'])

# 이미지 저장
img_path = os.path.join('./train', 'eight.jpg')
cv2.imwrite(img_path, 255-color)

for x,y,w,h in bR_arr : 
    cv2.rectangle(color,(x-2,y-2),(x+w+2,y+h+2),(0,0,255),1) 

img_path = os.path.join('./train', 'eightbox.jpg')
cv2.imwrite(img_path, 255-color)
