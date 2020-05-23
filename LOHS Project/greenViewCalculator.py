import pymeanshift as pms
import numpy as np

def greenViewClassification(Image):
    
    #Use Pymeanshift Algorithim to segment the image
    (segmented_image, labels_image, number_regions) = pms.segment(Image,spatial_radius=6, range_radius=7, min_density=40)
    
    image = segmented_image/255.0
    
    r_image = image[:,:,0]
    g_image = image[:,:,1]
    b_image = image[:,:,2]
    
    diff_green_red  = g_image - r_image
    diff_green_blue = g_image - b_image
    
    exg_array   =  diff_green_red + diff_green_blue
    diff_images =  diff_green_red * diff_green_blue
    
    red_Image_Threshold   = r_image <0.6
    green_Image_Threshold = g_image <0.9
    blue_Image_Threshold  = b_image <0.6
    
    green_Image_0 = red_Image_Threshold * green_Image_Threshold * blue_Image_Threshold

    red_Shadow   = r_image < 0.3
    green_Shadow = g_image < 0.3
    blue_Shadow  = b_image < 0.3
    
    green_Image_Shadow_0 = red_Shadow * green_Shadow * blue_Shadow
    
    cal_threshold =  calcThresh(exg_array, 0.1)
    
    
    if cal_threshold > 0.1:
        cal_threshold = 0.1
    elif cal_threshold < 0.05:
        cal_threshold = 0.05
    
    green_Image_1 = exg_array > cal_threshold
    green_Image_Shadow_1 = exg_array > 0.05
    
    
    f_green_image = green_Image_0*green_Image_1 + green_Image_Shadow_0* green_Image_Shadow_1
    greenPixels = len(np.where(f_green_image != 0)[0])
    greenPercent = greenPixels/(1000*500) * 100
    
    del image, r_image, g_image, b_image
    del red_Image_Threshold,green_Image_Threshold, blue_Image_Threshold
    del red_Shadow, green_Shadow , blue_Shadow
    del green_Image_0, green_Image_Shadow_0
    
    return f_green_image,greenPercent

def calcThresh(array,level):
    
    maxVal = np.max(array)
    minVal = np.min(array)

    if maxVal <= 1:
        array = array*255
    elif maxVal >= 256:
        array = np.int((array - minVal)/(maxVal - minVal))
    
    neg_Index = np.where(array < 0)
    array[neg_Index] = 0
    
    dims = np.shape(array)
    hist = np.histogram(array,range(257))
    P_hist = hist[0]*1.0/np.sum(hist[0])
    
    omega = P_hist.cumsum()
    temp = np.arange(256)
    mu = P_hist*(temp+1)
    mu = mu.cumsum()
    
    n = len(mu)
    mu_t = mu[n-1]
    
    sigma_b_squared = (mu_t*omega - mu)**2/(omega*(1-omega))
    
    indInf = np.where(sigma_b_squared == np.inf)
    
    CIN = 0
    if len(indInf[0])>0:
        CIN = len(indInf[0])
    
    maxval = np.max(sigma_b_squared)
    
    IsAllInf = CIN == 256
    if IsAllInf !=1:
        index = np.where(sigma_b_squared==maxval)
        idx = np.mean(index)
        threshold = (idx - 1)/255.0
    else:
        threshold = level
    
    if np.isnan(threshold):
        threshold = level
    
    return threshold