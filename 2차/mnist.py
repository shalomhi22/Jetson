import csv, os
import numpy as np
import cv2

classes = {'0' : '/m/0zero', '1' : '/m/0one', '2' : '/m/0two', \
        '3' : '/m/0three', '4' : '/m/0four', '5' : '/m/0five', \
        '6' : '/m/0six', '7' : '/m/0seven', '8' : '/m/0eight', '9' : '/m/0nine'}

types = ['train', 'test', 'validation']
for t in types :
    #minst 파일 읽기
    file = open(t+'.csv', 'r')
    file.readline()
    data_list = file.readlines()
    file.close()

    
    #annotation 작성
    f = open(t+'-annotations-bbox.csv', 'w', encoding='utf-8', newline='')
    fs = open('sub-'+t+'-annotations-bbox.csv', 'w', encoding='utf-8', newline='')
    wf = csv.writer(f)
    wfs = csv.writer(fs) 
    wf.writerow(['ImageID', 'Source', 'LabelName', 'Confidence' , 'XMin', 'XMax', 'YMin', 'YMax', 'IsOccluded', 'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside'])
    wfs.writerow(['ImageID', 'Source', 'LabelName', 'Confidence' , 'XMin', 'XMax', 'YMin', 'YMax', 'IsOccluded', 'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside', 'id', 'ClassName'])
    
    for i in range(len(data_list)) :
        all_values = data_list[i].split(',')
        target = all_values[0]
        all_values = all_values[1:]
        all_values[len(all_values)-1] = all_values[len(all_values)-1][0]

        #min, max 값 구하기
        xmin = 28; xmax = -1; ymin = 28; ymax = -1
        for j in range(len(all_values)) :
            if all_values[j] == '0' : continue

            if j//28 > ymax : ymax = j//28
            elif j//28 < ymin : ymin = j//28

            if j%28 > xmax : xmax = j%28
            elif j%28 < xmin : xmin = j%28
        xmin /= 27; xmax /= 27; ymin /= 27; ymax /= 27

        #jpg 저장
        img_array = np.array(all_values ,dtype=np.uint8).reshape(28,28,1)
        img_name = os.path.join('./'+t, 'image'+str(i)+'-'+target+'.jpg')
        cv2.imwrite(img_name, 255-img_array)

        #annotation 작성
        wf.writerow(['image'+str(i)+'-'+target, 'freeform', classes[target], 1 , xmin, xmax, ymin, ymax, 0, 0, 0, 0, 0])
        wfs.writerow(['image'+str(i)+'-'+target, 'freeform', classes[target], 1 , xmin, xmax, ymin, ymax, 0, 0, 0, 0, 0, classes[target], classes[target].split('0')[1].capitalize()])
    f.close(); fs.close()
