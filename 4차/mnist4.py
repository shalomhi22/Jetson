import csv, os
import numpy as np
import cv2
import random

size_range = [1, 2, 3]
num_range = [1, 4, 6, 10]
degree_range = [345, 350, 355, 0, 5, 10, 15]

classes = {'0' : '/m/0zero', '1' : '/m/0one', '2' : '/m/0two', \
        '3' : '/m/0three', '4' : '/m/0four', '5' : '/m/0five', \
        '6' : '/m/0six', '7' : '/m/0seven', '8' : '/m/0eight', '9' : '/m/0nine'}

types = ['train', 'test', 'validation']


if __name__ == '__main__' :
    file = open('mnist_train.csv', 'r')
    file.readline()

    cnt = 0; t = 0
    while cnt < 5000 :
        if cnt == 0 or cnt == 4000 or cnt == 4500 :
            f = open(types[t]+'-annotations-bbox.csv', 'w', encoding='utf-8', newline='')
            fs = open('sub-'+types[t]+'-annotations-bbox.csv', 'w', encoding='utf-8', newline='')
            wf = csv.writer(f)
            wfs = csv.writer(fs)
            wf.writerow(['ImageID', 'Source', 'LabelName', 'Confidence' , 'XMin', 'XMax', 'YMin', 'YMax', 'IsOccluded', 'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside'])
            wfs.writerow(['ImageID', 'Source', 'LabelName', 'Confidence' , 'XMin', 'XMax', 'YMin', 'YMax', 'IsOccluded', 'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside', 'id', 'ClassName'])

        num = random.choice(num_range)
        size = random.choice(size_range)
        target_list = []; img_list = []
        for _ in range(num) :
            tmp_data = file.readline()
            tmp_data = tmp_data.split(',')
            target_list.append(tmp_data[0])
            tmp_data = tmp_data[1:]
            tmp_data[len(tmp_data)-1] = tmp_data[len(tmp_data)-1][0]
            tmp_img = np.array(tmp_data, dtype=np.uint8).reshape(28, 28, 1)

            #사이즈 조정
            tmp_img = cv2.resize(tmp_img , (int(tmp_img.shape[1]*size), int(tmp_img.shape[0]*size)))

            #이미지 회전
            degree = random.choice(degree_range)
            (h, w) = tmp_img.shape[:2]
            (cX, cY) = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D((cX, cY), degree, 1.0)
            tmp_img = cv2.warpAffine(tmp_img, M, (w, h))
            if num != 1 : img_list.append(tmp_img)

        #이미지 병합
        if num == 1 : img = tmp_img
        else : 
            for i in range(0, num, 2):
                img1 = img_list[i]
                img2 = img_list[i+1]
                if i == 0 :
                    img = cv2.vconcat([img1, img2])
                else :
                    img = cv2.hconcat([img, cv2.vconcat([img1, img2])])

        #외곽선 검출
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        bR_arr = []
        col, row, _ = color.shape
        row -= 1; col -= 1
        for i in range(len(contours)) : 
            x,y,w,h = cv2.boundingRect(contours[i])
            bR_arr.append([x/row, (x+w)/row, y/col, (y+h)/col])

        #target 순서에 맞게 정렬
        bR_arr = sorted(bR_arr, key=lambda num : num[0])
        for i in range(0, num, 2) : 
            bR_arr[i:i+2] = sorted(bR_arr[i:i+2], key=lambda num : num[2])


        #annotations 작성
        if num != len(bR_arr) : continue
        for i in range(num) :
            wf.writerow(['image'+str(cnt), 'freeform', classes[target_list[i]], 1 , bR_arr[i][0], bR_arr[i][1], bR_arr[i][2], bR_arr[i][3], 0, 0, 0, 0, 0])
            wfs.writerow(['image'+str(cnt), 'freeform', classes[target_list[i]], 1 , bR_arr[i][0], bR_arr[i][1], bR_arr[i][2], bR_arr[i][3], 0, 0, 0, 0, 0, classes[target_list[i]], classes[target_list[i]].split('0')[1].capitalize()])
        
        #이미지 저장
        img_path = os.path.join('./'+types[t], 'image'+str(cnt)+'.jpg')
        cv2.imwrite(img_path, 255-color)
        
        cnt+=1
        if cnt == 4000 or cnt == 4500: 
            f.close(); fs.close()
            t += 1

    file.close()