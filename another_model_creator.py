import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Dropout, Flatten
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import time

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


DIRECTORY = r"D:\Documents\data\dataset"  #bilgisayarınızda datasetin bulunduğu directoryi yazın
CATEGORIES = [ "proper-mask","improper-mask","non-mask"]

EPOCHS=30
BS=20
# grab the list of images in our dataset directory, then initialize
# the list of data (i.e., images) and class images
print("[INFO] loading images...")

data = []
labels = []
dim1 = []
dim2 = []

for category in CATEGORIES:
    path = os.path.join(DIRECTORY, category)
    for img in os.listdir(path):
        img_path = os.path.join(path, img)
        #print(img_path)
        image = load_img(img_path, target_size=(224, 224))
        image = img_to_array(image)
        image = preprocess_input(image)

        data.append(image)
        labels.append(category)
        d1, d2, colors = image.shape
        dim1.append(d1)
        dim2.append(d2)

# perform one-hot encoding on the labels
print("[INFO] Images Loaded.")
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
#labels = to_categorical(labels)

data = np.array(data, dtype="float32")
labels = np.array(labels)
D2labels=labels
start = time.time()

(trainX, testX, trainY, testY) = train_test_split(data, D2labels,
	test_size=0.20, stratify=D2labels)


aug = ImageDataGenerator(
	rotation_range=20,
	zoom_range=0.15,
	width_shift_range=0.2,
	height_shift_range=0.2,
	shear_range=0.15,
	horizontal_flip=True,
	fill_mode="nearest")

# print(len(os.listdir(os.path.join(train_path, 'Viral Pneumonia'))))
# number of images for Normal, Covid, Viral Pneumonia = 70,111,70

# print(np.mean(dim1), np.mean(dim2)) = 728.2 782.6

# Keeping dimensions of images same
image_shape = (224, 224, 3)

# plt.imshow(normal_xray_path_arr)
# plt.show()
# plt.imshow(img_gen.random_transform(normal_xray_path_arr))
# plt.show()

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 3), input_shape=image_shape, activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Conv2D(filters=128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(3, activation='softmax'))


early_stop = EarlyStopping(monitor='val_loss', patience=2)


'''train_image_gen = img_gen.flow_from_directory(trainX, target_size=image_shape[:2],
                                              color_mode='rgb',
                                              batch_size=batch_size,
                                              class_mode='categorical')
test_image_gen = img_gen.flow_from_directory(test_path, target_size=image_shape[:2],
                                             color_mode='rgb',
                                             batch_size=batch_size,
                                             class_mode='categorical',
                                             shuffle=False)'''
model.summary()

# Result index
# print(train_image_gen.class_indices) ={'Covid': 0, 'Normal': 1, 'Viral Pneumonia': 2}
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
results = model.fit(
	aug.flow(trainX, trainY, batch_size=BS),
	steps_per_epoch=len(trainX) // BS,
	validation_data=(testX, testY),
	validation_steps=len(testX) // BS,
	epochs=EPOCHS)
finish = time.time()

print("[INFO] saving mask detector model...")
model.save("another.model", save_format="h5")

print("Time taken in seconds: ", finish-start)
# plot the training loss and accuracy
N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), results.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), results.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), results.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), results.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig("another.png")