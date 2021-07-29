import cv2 
import numpy as np 

filename = 'image1.jpg' 
src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) 
src = cv2.resize(src , (int(src.shape[1]*5), int(src.shape[0]*5))) #이미지가 작아서 크기 키워서 확인

###########
(h, w) = src.shape[:2]
(cX, cY) = (w / 2, h / 2)
# rotate our image by 45 degrees
M = cv2.getRotationMatrix2D((cX, cY), 350, 1.0)
src = cv2.warpAffine(src, M, (w, h), borderValue=(255,255,255))

cv2.imshow('contours', src)


k = cv2.waitKey(0) 
cv2.destroyAllWindows()



#이진화
ret, binary = cv2.threshold(src, 170, 255, cv2.THRESH_BINARY_INV)

#노이즈 제거
binary = cv2.morphologyEx(binary , cv2.MORPH_OPEN , cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2)), iterations = 2)

#외곽선 검출
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
color = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR) 
cv2.drawContours(color, contours, -1, (0,255,0), 3)

bR_arr = []
for i in range(len(contours)) : 
    # bin_tmp = binary.copy()
    x,y,w,h = cv2.boundingRect(contours[i])
    bR_arr.append([x, y, w, h])
    
    # bR_arr.append([x, y, x+w, y+h])

#x값을 기준으로 배열을 정렬 
bR_arr = sorted(bR_arr, key=lambda num : num[0], reverse = False)
print(bR_arr)

for x,y,w,h in bR_arr : 
    cv2.rectangle(color,(x-2,y-2),(x+w+2,y+h+2),(0,0,255),1) 

cv2.imshow('contours', color)

k = cv2.waitKey(0) 
cv2.destroyAllWindows()

