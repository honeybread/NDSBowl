import scipy as sp
import os
from skimage import io

''' class to pre process images'''

class Image_Preprocess(object):
    def __init__(self, dir_name = '../data/train' ):
        self.dir_name = '../data/train'
        self.dir_name_resized = '../data/train_100'

    def image_resize(self, resize_shape = (100, 100)):
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
                image_resized = sp.misc.imresize(image_nparray,resize_shape)
                sp.misc.imsave(self.dir_name_resized+'/'+folder+'/'+image, image_resized)
                

if __name__ == "__main__":
    ip = Image_Preprocess()
    ip.image_resize()