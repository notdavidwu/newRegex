import cc3d
import numpy as np
from skimage import measure
import h5py
import cv2
import cupy as cp
import math
import numpy as np
from ellipse import LsqEllipse
def measure_Tumor(img,pixelSpacing,sliceThickness,delta_Z):
    labels_out, N = cc3d.connected_components(img, return_N=True,connectivity=26)
    
    '''取得最靠近座標的腫瘤'''
    center = cp.array((int(img.shape[0]/2),int(img.shape[1]/2),int(img.shape[2]/2)))
    labels_out = cp.array(labels_out)
    coords = cp.where(labels_out!=0)
    coords = cp.vstack((coords[0],coords[1],coords[2]))
    center = cp.dstack([center]*coords.shape[1])
    center = coords[:,cp.argmin(cp.sum(cp.square(coords - center),axis = 1))]
    tumor_label = labels_out[center[0],center[1],center[2]]


    '''取得最大截面積的Slice'''
    areas = []
    props = []
    label_vol = cp.array(labels_out==tumor_label,dtype='int').get()
    for slice in label_vol:
        prop = measure.regionprops(slice)
        if len(prop) > 0:
            areas.append(prop[0].area)
        else:
            areas.append(0)
        props.append(prop)
    slice = label_vol[np.argmax(np.array(areas))]
    slice = slice.astype("uint8")
    max_area = float(np.max(np.array(areas)))*pixelSpacing
    '''取最長軸'''
    contours, hierarchy = cv2.findContours(slice, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = cp.array(contours[0][:,0,:])
    distance_matrix_2 = cp.vstack([contours[0]]*len(contours))

    for i in range(1,len(contours)):
        temp = cp.vstack([contours[i]]*len(contours))
        distance_matrix_2 = cp.dstack((distance_matrix_2,temp))

    distance_matrix_1 = cp.dstack([contours]*len(contours))
    distance_matrix_1 = cp.transpose(distance_matrix_1,(2,0,1))
    distance_matrix_2 = cp.transpose(distance_matrix_2,(2,0,1))

    vector_maxtrix = (distance_matrix_2 - distance_matrix_1)
    distance_matrix = cp.sqrt(cp.sum(cp.square(cp.abs(vector_maxtrix)),axis=2))
    maxDia_index = cp.where(distance_matrix==cp.max(distance_matrix))[0]
    maxDia_point1 =  contours[maxDia_index[0]]
    maxDia_point2 =  contours[maxDia_index[1]]
    maxDia = cp.max(distance_matrix)*pixelSpacing

    maxDia_vector_arg = cp.vstack([vector_maxtrix[maxDia_index[0],maxDia_index[1]]]*len(contours))
    maxDia_vector_arg = cp.dstack([maxDia_vector_arg]*len(contours))
    maxDia_vector_arg = cp.transpose(maxDia_vector_arg,(2,0,1))

    '''取得與長軸夾角80~110的次長軸'''
    vector_dot = cp.sum(maxDia_vector_arg*vector_maxtrix,axis=2)
    vector1_norm = cp.sqrt(cp.sum(cp.square(vector_maxtrix),axis=2))
    vector2_norm = cp.sqrt(cp.sum(cp.square(maxDia_vector_arg),axis=2))
    cos_theta = vector_dot/vector1_norm/vector2_norm

    angle1 = math.radians(80)
    angle2 = math.radians(100)
    cos_angle1 = math.cos(angle1)
    cos_angle2 = math.cos(angle2)
    cos_angle = [cos_angle1,cos_angle2]
    cos_theta[cos_theta < min(cos_angle)]=cp.nan
    cos_theta[cos_theta >= max(cos_angle)]=cp.nan
    accept_cos_theta = cp.where(~cp.isnan(cos_theta))
    accept_cos_theta = cp.vstack((accept_cos_theta[0],accept_cos_theta[1]))

    secDia_distance = distance_matrix[accept_cos_theta[0],accept_cos_theta[1]]
    secDia_distance_index = cp.where(secDia_distance==cp.max(secDia_distance))
    secDia_index = cp.transpose(cp.squeeze(accept_cos_theta[:,secDia_distance_index],axis=1),(1,0))
    secDia_index = secDia_index[cp.argmin(cp.abs(cos_theta[secDia_index[:,0],secDia_index[:,1]]-0))]
    secDia_point1 =  contours[secDia_index[0]]
    secDia_point2 =  contours[secDia_index[1]]
    secDia = distance_matrix[secDia_index[0],secDia_index[1]]*pixelSpacing
    
    '''取兩長軸夾角#'''
    radian = math.acos(cos_theta[secDia_index[0],secDia_index[1]])
    vector_angle = math.degrees(radian)
    #slice = np.dstack([slice]*3)
    #cv2.drawContours(slice, contour, -1, (255,255,255), thickness=1)
    #cv2.line(slice,(int(maxDia_point1[0]),int(maxDia_point1[1])) ,(int(maxDia_point2[0]),int(maxDia_point2[1])) , (0, 0, 255), 1)
    #cv2.line(slice,(int(secDia_point1[0]),int(secDia_point1[1])) ,(int(secDia_point2[0]),int(secDia_point2[1])) , (0, 0, 255), 1)
    
    # print(contours)
    # reg = LsqEllipse().fit(contours.get())
    # center, width, height, phi = reg.as_parameters()
    # print(f'center: {center[0]:.3f}, {center[1]:.3f}')
    # print(f'width: {width:.3f}')
    # print(f'height: {height:.3f}')
    # print(f'phi: {phi:.3f}')
    # center=np.round(np.float64(center))
    # width=float(width)
    # height=float(height)
    # phi=float(phi)
    # cv2.ellipse(slice,(15,31),(10,10),0,0,180,255,1)
    #slice = cv2.ellipse(slice, (center[0],center[1]), (2*height,2*width), np.rad2deg(phi), 0, 360, (255,255,0), 1)
    
    #cv2.imshow('My Image', slice)
    #cv2.waitKey(0)

    '''算體積'''
    volume=0
    slice_space=[]
    for slice in label_vol:
        if (np.unique(slice)!=0).any():
            slice_space.append(np.sum(slice==tumor_label.get())*np.square(pixelSpacing))
    if sliceThickness > delta_Z:
        for i in range(len(slice_space)):
            if i ==0:
                volume += slice_space[i]*((sliceThickness/2)-(delta_Z/2)+delta_Z)
            elif i==len(slice_space):
                volume += slice_space[i]*((sliceThickness/2)-(delta_Z/2))
            else:
                volume += slice_space[i]*delta_Z
    else:
        for i in range(len(slice_space)):
            volume += slice_space[i]*delta_Z
    print(volume)
    return maxDia_point1.get(),maxDia_point2.get(),maxDia.get(),secDia_point1.get(),secDia_point2.get(),secDia.get(),vector_angle,max_area,volume

image = np.array(h5py.File('D:\Tumor_unet.h5','r')['Tumor'])
measure_Tumor(image,pixelSpacing=0.6640625,sliceThickness=1,delta_Z=1)