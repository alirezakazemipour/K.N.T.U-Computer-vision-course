import numpy as np
import cv2
from sklearn.svm import SVC
from sklearn.externals import joblib
import os
import random
from skimage import feature

dataset = '/home/alireza/Documents/cv-lab13/dataset/train/{}/'
train_labels=[]
train_imgs_list=[]

for i in range(0,10):

    train_images_list = os.listdir( dataset.format( str( i ) ) )

    train_images_list.sort()

    train_labels.extend([int( addr[2] ) for addr in (train_images_list)])

    train_imgs_list.append(train_images_list)
# print(len(train_labels))
# exit(0)

input_data = []

for j in range(0,10):
    # for k in range( 0, 120 ):
     for addr in train_imgs_list[j]:
        I = cv2.imread(os.path.join('/home/alireza/Documents/cv-lab13/dataset/train/{}/'.format(str(addr[2])), addr))
        I=cv2.cvtColor(I,cv2.COLOR_BGR2GRAY)
        (H, hogImage_train) = feature.hog( I, orientations=9, pixels_per_cell=(8, 8),
                                     cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1",
                                     visualise=True )
        input_data.append(H)

classifier = SVC(gamma='auto')
file_name = 'saved_svm.sav'


# if not os.path.isfile(file_name):
#     classifier.fit(input_data, train_labels)
#     joblib.dump(classifier, file_name)
#
# else:
#     classifier = joblib.load(file_name)

os.path.isfile(file_name)
classifier.fit(input_data, train_labels)
joblib.dump(classifier, file_name)

test_dir=dataset = '/home/alireza/Documents/cv-lab13/dataset/test'
test_images_list = os.listdir(test_dir)
test_images_list.sort()

test_labels = [int(addr[2]) for addr in (test_images_list)]

test_data = []

for addr in (test_images_list):
    J = cv2.imread(os.path.join('/home/alireza/Documents/cv-lab13/dataset/test'.format(str(addr[2])), addr))
    J = cv2.cvtColor( J, cv2.COLOR_BGR2GRAY )
    (K, hogImage_test) = feature.hog( J, orientations=9, pixels_per_cell=(8, 8),
                                 cells_per_block=(2, 2), transform_sqrt=True, block_norm="L1",
                                 visualise=True )
    test_data.append(K)


idx = [random.randint(0, len(test_data)-1) for i in range(20)]
test_input = [test_data[i] for i in idx]
test_labels = [test_labels[i] for i in idx]
results = classifier.predict(test_input)
print('predictions: ', results)
print("train lables: ",train_labels)
print("test lables: ",test_labels)
print("Accuracy: ",(np.sum(results==test_labels)/len(results))*100,"%")

print("-------------------------")

idx = [random.randint(0, len(input_data)-1) for i in range(10)]
test_input = [input_data[i] for i in idx]
test_labels = [train_labels[i] for i in idx]
results = classifier.predict(test_input)
print('predictions: ', results)
print("train lables: ",train_labels)
print("test lables: ",test_labels)
print("Accuracy: ",(np.sum(results==test_labels)/len(results))*100,"%")