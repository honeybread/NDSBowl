import scipy as sp
import scipy.misc as misc
import os, re
from skimage import io
from sklearn.preprocessing import normalize
from matplotlib import pyplot as plt
from matplotlib import cm

''' class to pre process images'''
b = 1
class Image_Preprocess(object):
    def __init__(self, dir_name = '../data/train' ):
        self.dir_name = '../data/train'
        self.dir_name_resized = '../data/train_100'
        self.dir_name_normalized = '../data/train_100_normal'

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
                image_resized = misc.imresize(image_nparray,resize_shape)
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
                    image_rotated = sp.ndimage.interpolation.rotate(image_nparray,angle, mode = 'nearest')
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
                

  
            
                

if __name__ == "__main__":
    ip = Image_Preprocess()
    #ip.image_resize()
    #ip.image_rotate()
    b = ip.image_normalize()