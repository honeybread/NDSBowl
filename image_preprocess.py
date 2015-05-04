import scipy as sp
import scipy.misc as misc
import scipy.ndimage as ndimage
import os, re
from skimage import io
from sklearn.preprocessing import normalize
from matplotlib import pyplot as plt
from matplotlib import cm
import sys
import numpy as np
import cPickle as pickle
import random


''' class to pre process images'''
b = 1
class Image_Preprocess(object):
    def __init__(self, dir_name = '../data/train' ):
        self.up_dir = '../data'
        self.dir_name = self.up_dir + '/train'
        self.dir_name_resized = self.up_dir + '/train_100'
        self.dir_name_normalized = self.up_dir + '/train_100_normal'
        self.labeldic = {}

    def image_resize(self, resize_shape = (60, 60)):
        ''' method to resize images to resize_shape'''
        if not os.path.exists(self.dir_name_resized):
            os.mkdir(self.dir_name_resized)
            
        all_folders = list(os.walk(self.dir_name))

        for folder in all_folders[0][1]:
            print "resizing images in :", folder
            
            if not os.path.exists(self.dir_name_resized + '/' + folder):
                os.mkdir(self.dir_name_resized + '/' + folder)
                
            all_images = list(os.walk(self.dir_name + '/'+folder))
            for image in all_images[0][2]:
                image_nparray = io.imread(self.dir_name + '/'+folder+'/'+image)
                image_resized = misc.imresize(image_nparray,resize_shape)
                image_resized = image_resized/255.

                misc.imsave(self.dir_name_resized+'/'+folder+'/'+image, image_resized)


    def image_rotate(self, rotation_angles = (90, 180, 270)):
        '''method to rotate images'''
        
        if not os.path.exists(self.dir_name_resized):
            print "Error: Resize Images and Try rotating on top of it"
        
        all_folders = list(os.walk(self.dir_name_resized))
        
        for folder in all_folders[0][1]:
            print "rotating images in :", folder
  
            all_images = list(os.walk(self.dir_name_resized + '/'+folder))
            for image in all_images[0][2]:
                if image == '.DS_Store':
                    continue
                image_nparray = io.imread(self.dir_name_resized + '/'+folder+'/'+image)
                for angle in rotation_angles:
                    image_rotated = ndimage.interpolation.rotate(image_nparray,angle, mode = 'nearest')
                    image_rotated_name = re.sub('.jpg', '_' + str(angle) + '.jpg', image)
                    misc.imsave(self.dir_name_resized +'/'+folder+'/'+image_rotated_name, image_rotated)

        
                    
    def image_normalize(self):
        all_folders = list(os.walk(self.dir_name_resized))
        
        for folder in all_folders[0][1]:
            if not os.path.exists(self.dir_name_normalized + '/' + folder):
                os.mkdir(self.dir_name_normalized + '/' + folder)
            print "normalizing images in :", folder
  
            all_images = list(os.walk(self.dir_name_resized + '/'+folder))
            print "len_all_images",len(all_images)
            for image in all_images[0][2]:
                if image == '.DS_Store':
                    continue
                np_array =  io.imread(self.dir_name_resized + '/'+folder+'/'+image)
                shape = np_array.shape
                np_array_normalized = normalize(np_array.reshape(shape[0] * shape[1],), axis = 1)
                plt.imsave(self.dir_name_normalized +'/'+folder+'/'+image, np_array_normalized.reshape(shape), cmap = cm.gray)
                
    

    ''' create split for training
        10% for validation, 10% for tesing, 80% for training
    '''
    def create_split(self, image_dir, resize_shape = (60, 60)):
        # total number of images
        cpt = sum([len(files) for r,d, files in os.walk(image_dir)]) 

        imagesize = resize_shape[0] * resize_shape[1]
        train_set_x = np.empty([cpt,resize_shape[0] * resize_shape[1]], dtype=np.float32)
        train_set_y = np.empty(cpt, dtype=int)

        all_folders = list(os.walk(image_dir))
        labeldic = {item:i for i,item in enumerate(all_folders[0][1])}
        image_index = 0

        for folder in all_folders[0][1]:
            print "loading images in :", folder
  
            all_images = list(os.walk(image_dir + '/'+folder))
            for image in all_images[0][2]:
                image_nparray = io.imread(image_dir + '/'+folder+'/'+image)
                train_set_x[image_index] = image_nparray.flatten()
                train_set_y[image_index] = labeldic[folder]
                image_index += 1

        # create indices for train set and test set
        indices = range(cpt)
        random.shuffle(indices)
        
        holdout = cpt/10
        test_pile = indices[:holdout]
        valid_pile = indices[-holdout:]
        train_pile = indices[holdout:-holdout]

        train_set = (train_set_x[train_pile],train_set_y[train_pile])
        valid_set = (train_set_x[valid_pile],train_set_y[valid_pile])
        test_set = (train_set_x[test_pile],train_set_y[test_pile])
        with open(self.up_dir + '/' + 'data.pkl','wb') as f:
            pickle.dump([train_set,valid_set,test_set],f) 
            
                

if __name__ == "__main__":
    ip = Image_Preprocess()
    #ip.image_resize()
    #ip.image_rotate()
    ip.create_split(image_dir = ip.dir_name_resized)
    #b = ip.image_normalize()
