import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = list()
    labels = list()


    print("Importing dataset...")
    
    # Accessing every element in the data_dir
    for element in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, element)
        # If element is a directory
        if os.path.isdir(folder_path):
            # Get an image
            print(f"Loading images from {folder_path}")
            for img in os.listdir(folder_path):

                # Loading image
                img_path = os.path.join(folder_path, img)
                image = cv2.imread(img_path, cv2.IMREAD_COLOR)

                # Resizing image

                # cv2.resize(src, dsize[], dst[, fx[, fy[, interpolation]]]]) 
                # src is the source, original or input image in the form of numpy array
                # dsize is the desired size of the output image, given as tuple
                # fx is the scaling factor along X-axis or Horizontal axis
                # fy is the scaling factor along Y-axis or Vertical axis
                # interpolation could be one of the following values : INTER_NEAREST, INTER_LINEAR, INTER_AREA, INTER_CUBIC, INTER_LANCZOS4

                dsize = (IMG_WIDTH, IMG_HEIGHT)
                res = cv2.resize(image, dsize)  

                # Verify if image size and width are as desired:
                # img.shape[0] = height, image.shape[1] = width
                
                # Appending image to list
                images.append(res)

                # Label = Name of parent directory of image
                labels.append(str(element)) 
    
    print(f'Dataset imported! \n')   
    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """



if __name__ == "__main__":
    main()
