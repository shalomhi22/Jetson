import csv, os

classes = {'0' : '/m/0zero', '1' : '/m/0one', '2' : '/m/0two', \
        '3' : '/m/0three', '4' : '/m/0four', '5' : '/m/0five', \
        '6' : '/m/0six', '7' : '/m/0seven', '8' : '/m/0eight', '9' : '/m/0nine'}

types = ['train', 'test', 'validation']
for t in types :
    path = "./"+t
    file_list = os.listdir(path)

    f = open(t+'-annotations-bbox.csv', 'w', encoding='utf-8', newline='')
    fs = open('sub-'+t+'-annotations-bbox.csv', 'w', encoding='utf-8', newline='')
    wf = csv.writer(f)
    wfs = csv.writer(fs) 
    wf.writerow(['ImageID', 'Source', 'LabelName', 'Confidence' , 'XMin', 'XMax', 'YMin', 'YMax', 'IsOccluded', 'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside'])
    wfs.writerow(['ImageID', 'Source', 'LabelName', 'Confidence' , 'XMin', 'XMax', 'YMin', 'YMax', 'IsOccluded', 'IsTruncated', 'IsGroupOf', 'IsDepiction', 'IsInside', 'id', 'ClassName'])

    for file in file_list :
        image = file.split('.')[0]
        num = image[len(image)-1]
        wf.writerow([image, 'freeform', classes[num], 1 , 0, 1, 0, 1, 0, 0, 0, 0, 0])
        wfs.writerow([image, 'freeform', classes[num], 1 , 0, 1, 0, 1, 0, 0, 0, 0, 0, classes[num], classes[num].split('0')[1].capitalize()])
    f.close(); fs.close()
