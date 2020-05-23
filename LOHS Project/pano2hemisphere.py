import os
import time
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from scipy import interpolate
from skimage import filters
from skimage.morphology import disk, binary_dilation
import multiprocessing

import scipy.interpolate as spint
import scipy.spatial.qhull as qhull
import itertools

def pano2fisheye(pil_img):
    
    img_df, shape = img2dataframe(pil_img)
    
    img_conv, fisheye_shape = coordinate_converse(img_df, shape)
    
    img_cali = unique_points(img_conv)
    
    red,green,blue = interpolate_img(img_cali, fisheye_shape)
    
    fisheye_img = merge_layers(red, green, blue)
    
    return fisheye_img


def interpolate_img(img_df, shape):
  
    xi, yi = np.mgrid[0:shape[0], 0:shape[1]]
    mask_hole = np.zeros(shape)
    mask_hole[img_df['x'], img_df['y']] = 1
    mask_circ = createCircularMask(*shape)
    mask = (mask_hole==0) * mask_circ
    red = np.zeros(shape).astype(np.uint16)
    green = np.zeros(shape).astype(np.uint16)
    blue = np.zeros(shape).astype(np.uint16)
    red[img_df['x'], img_df['y']] = img_df['red']
    green[img_df['x'], img_df['y']] = img_df['green']
    blue[img_df['x'], img_df['y']] = img_df['blue']
            
    red_filter = filters.rank.mean(red, disk(1),mask=mask_hole==1)
    green_filter = filters.rank.mean(green, disk(1),mask=mask_hole==1)
    blue_filter = filters.rank.mean(blue, disk(1),mask=mask_hole==1)
            
    red[mask] = red_filter[mask]
    green[mask] = green_filter[mask]
    blue[mask] = blue_filter[mask]   
    return red, green, blue


def unique_points(img_df):
    '''
    remove duplicate points which overlay one the same pixel
    x: conversed x (float)
    y: conversed y (float)
    shape: (height, width)
    return x, y , v_new
    '''
    x_int = img_df['x_cali'].astype(int)
    y_int = img_df['y_cali'].astype(int)
    df_cali = pd.DataFrame(
        {'x': x_int, 'y': y_int, 'red': img_df['red'], 'green': img_df['green'], 'blue': img_df['blue']})
    df_cali = df_cali.groupby(['x', 'y'], as_index=False).mean()

    return df_cali


def coordinate_converse(img_df, panorama_size):
    '''
    panorama size = (h, w)
        h: panorama image height
        w: panorama image width
    model:- assume height of one pixel in panorama = the distance to circle center in fisheye
 
    '''
    h, w = panorama_size
    r = h
    fisheye_size = (2 * r, 2 * r)
    theta = (img_df['y'] + 0.5) / w * 360  # +0.5 is to mark pixel center
    sin_theta = np.sin(np.deg2rad(theta))
    cos_theta = np.cos(np.deg2rad(theta))
    
    img_df['x_cali'] = r + sin_theta * img_df['x']
    img_df['y_cali'] = r + cos_theta * img_df['x']
    
    return img_df, fisheye_size



def img2dataframe(img):
    '''
    if img is a fisheye image, (x, y, r) is required to crop fisheye edge.
    '''
    width, height = img.size
    img_out = img.crop((0, 0, width, int(height / 2)))

    '''PIL.img.size = (w, h)'''
    w, h = img_out.size
    np_img = np.asarray(img_out)

    x_grid, y_grid = np.mgrid[0:h, 0:w]
    red = np_img[:, :, 0]
    green = np_img[:, :, 1]
    blue = np_img[:, :, 2]
    if np_img.shape[2] == 4:
        alpha = np.asarray(img_out)[:, :, 3]
        img_df = pd.DataFrame({'x': x_grid.flatten(), 'y': y_grid.flatten(),
                               'red': red.flatten(), 'green': green.flatten(), 'blue': blue.flatten(),
                               'alpha': alpha.flatten()},
                              columns=['x', 'y', 'red', 'green', 'blue', 'alpha'])
        # remove alpha layer
        img_df = img_df.loc[img_df['alpha'] == 255]
        img_df = img_df.drop(['alpha'], axis=1)
    else:
        img_df = pd.DataFrame({'x': x_grid.flatten(), 'y': y_grid.flatten(),
                               'red': red.flatten(), 'green': green.flatten(), 'blue': blue.flatten()},
                              columns=['x', 'y', 'red', 'green', 'blue'])
    np_shape = (h, w)
    return img_df, np_shape

def merge_layers(r, g, b):
    img = np.zeros((r.shape[0], r.shape[1], 3))
    img[:, :, 0] = r
    img[:, :, 1] = g
    img[:, :, 2] = b
    img[np.isnan(img)] = 0
    img = img.astype('uint8')
    pil_img = Image.fromarray(img)

    return pil_img
    
    
def createCircularMask(h, w, center=None, radius=None):
    if center is None: 
        center = [int(w/2), int(h/2)]
    if radius is None: 
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask