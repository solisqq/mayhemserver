import cv2
for i in range(1,4):
    path = "C:/Users/kamil/Downloads/drive-download-20210329T180437Z-001/"+str(i)+".jpg"
    img = cv2.imread(path)
    img = cv2.resize(img,(1280,960),fx=0,fy=0, interpolation = cv2.INTER_CUBIC) 
    cv2.imwrite("C:/Users/kamil/Downloads/drive-download-20210329T180437Z-001/_"+str(i)+".jpg", img)
