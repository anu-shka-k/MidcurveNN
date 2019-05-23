import os
from keras.preprocessing.image import img_to_array, load_img
from random import shuffle
import PIL
import json
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

def get_training_data(datafolder = "output"):
    profile_pngs,midcurve_pngs = read_input_image_pairs(datafolder)
    
    profile_pngs_objs = [img_to_array(load_img(f, color_mode='rgba', target_size=(100, 100))) for f in profile_pngs ]
    midcurve_pngs_objs = [img_to_array(load_img(f, color_mode='rgba', target_size=(100, 100))) for f in midcurve_pngs]

#     profile_pngs_objs = np.array([x.reshape((1,) + x.shape) for x in profile_pngs_objs])
#     midcurve_pngs_objs = np.array([x.reshape((1,) + x.shape) for x in midcurve_pngs_objs])

    profile_pngs_gray_objs = [x[:,:,3] for x in profile_pngs_objs]
    midcurve_pngs_gray_objs =[x[:,:,3] for x in midcurve_pngs_objs]
    
#     profile_pngs_gray_objs = [np.where(x>128, 0, 1) for x in profile_pngs_gray_objs]
#     midcurve_pngs_gray_objs =[np.where(x>128, 0, 1) for x in midcurve_pngs_gray_objs]
        
    # shufle them
    zipped_profiles_midcurves = [(p,m) for p,m in zip(profile_pngs_gray_objs,midcurve_pngs_gray_objs)]
    shuffle(zipped_profiles_midcurves)
    profile_pngs_gray_objs, midcurve_pngs_gray_objs = zip(*zipped_profiles_midcurves)
    
    return profile_pngs_gray_objs, midcurve_pngs_gray_objs

def get_profile_dict(shapename,profiles_dict_list):
    for i in profiles_dict_list:
        if i['ShapeName'] == shapename:
            return i
    profile_dict = {}
    profile_dict['ShapeName'] = shapename
    return profile_dict

def read_dat_files(datafolder="data"):
    profiles_dict_list = []
    for file in os.listdir(datafolder):
        if os.path.isdir(os.path.join(datafolder, file)):
            continue
        filename = file.split(".")[0]
        profile_dict = get_profile_dict(filename,profiles_dict_list)        
        if file.endswith(".dat"):
            with open(os.path.join(datafolder, file)) as f:
                profile_dict['Profile'] = [tuple(map(float, i.split('\t'))) for i in f]  
        if file.endswith(".mid"):
            with open(os.path.join(datafolder, file)) as f:
                profile_dict['Midcurve'] = [tuple(map(float, i.split('\t'))) for i in f]
                                
        profiles_dict_list.append(profile_dict)
    return profiles_dict_list

import drawSvg as draw
def create_image_file(fieldname,profile_dict,datafolder="output",isOpenClose=True):
    d = draw.Drawing(100, 100, origin='center')
    profilepoints = []
    for tpl in profile_dict[fieldname]:
        profilepoints.append(tpl[0])
        profilepoints.append(tpl[1])
    d.append(draw.Lines(profilepoints[0],profilepoints[1],*profilepoints,close=isOpenClose,fill='none',stroke='black'))
    
    shape = profile_dict['ShapeName']
#     d.saveSvg(datafolder+"/"+shape+'.svg')
    d.savePng(datafolder+"/"+shape+'_'+fieldname+'.png')

def get_original_png_files(datafolder="output"):
    pngfilenames = []
    for file in os.listdir(datafolder):
        fullpath = os.path.join(datafolder, file)
        if os.path.isdir(fullpath):
            continue
        if file.endswith(".png") and file.find("_rotated_") == -1 and file.find("_translated_")==-1 and file.find("_mirrored_")==-1:
            pngfilenames.append(fullpath)
    return pngfilenames

from PIL import Image
def rotate_images(pngfilenames, angle=90):
    for fullpath in pngfilenames:
        picture= Image.open(fullpath)
        newfilename = fullpath.replace(".png", "_rotated_"+str(angle)+".png")
        picture.rotate(angle).save(newfilename)

def mirror_images(pngfilenames, mode=PIL.Image.TRANSPOSE):
    mirrored_filenames = []
    for fullpath in pngfilenames:
        picture= Image.open(fullpath)
        newfilename = fullpath.replace(".png", "_mirrored_"+str(mode)+".png")
        picture.transpose(mode).save(newfilename)
        mirrored_filenames.append(newfilename)
    return mirrored_filenames
        
def translate_images(pngfilenames, dx=1,dy=1):
    for fullpath in pngfilenames:
        picture= Image.open(fullpath)
        x_shift = dx
        y_shift = dy
        a = 1
        b = 0
        c = x_shift #left/right (i.e. 5/-5)
        d = 0
        e = 1
        f = y_shift #up/down (i.e. 5/-5)
        translate = picture.transform(picture.size, Image.AFFINE, (a, b, c, d, e, f))
#         # Calculate the size after cropping
#         size = (translate.size[0] - x_shift, translate.size[1] - y_shift)
#         # Crop to the desired size
#         translate = translate.transform(size, Image.EXTENT, (0, 0, size[0], size[1]))
        newfilename = fullpath.replace(".png", "_translated_"+str(dx)+"_"+str(dy)+".png")
        translate.save(newfilename)
        
def read_input_image_pairs(datafolder="output"):
    profile_pngs = []
    midcurve_pngs = []
    for file in os.listdir(datafolder):
        fullpath = os.path.join(datafolder, file)
        if os.path.isdir(fullpath):
            continue
        if file.endswith(".png"):
            if file.find("Profile") != -1:
                profile_pngs.append(fullpath)
            if file.find("Midcurve") != -1:
                midcurve_pngs.append(fullpath)
    profile_pngs = sorted(profile_pngs)
    midcurve_pngs = sorted(midcurve_pngs)
    return profile_pngs,midcurve_pngs
    
def generate_images(datafolder = "output"):
    for file in os.listdir(datafolder):
        if file.endswith(".png") and (file.find("_rotated_") != -1 or file.find("_translated_") !=-1):
            print("files already present, not generating...")
            return
                
    print("transformed files not present, generating...")
    profiles_dict_list = read_dat_files()
    
    for profile_dict in profiles_dict_list:
        create_image_file('Profile',profile_dict,datafolder,True)
        create_image_file('Midcurve',profile_dict,datafolder,False)
        
    pngfilenames = get_original_png_files(datafolder)
    mirrored_filenames_left_right = mirror_images(pngfilenames, PIL.Image.FLIP_LEFT_RIGHT)
    mirrored_filenames_top_bottom = mirror_images(pngfilenames, PIL.Image.FLIP_TOP_BOTTOM)
    mirrored_filenames_transpose = mirror_images(pngfilenames, PIL.Image.TRANSPOSE)
    
    files_list_list = [pngfilenames,mirrored_filenames_left_right,mirrored_filenames_top_bottom,mirrored_filenames_transpose]
    for filelist in files_list_list:
        for angle in range(30,360,30):
            rotate_images(filelist,angle)
            
        for dx in range(5,21,5):
            for dy in range(5,21,5):
                translate_images(filelist,dx,-dy)
            
        
if __name__ == "__main__":
    generate_images()
    profile_pngs,midcurve_pngs = read_input_image_pairs()


    
