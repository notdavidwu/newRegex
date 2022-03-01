import h5py
import numpy as np
import time
import os
import sys
import pydicom
import argparse
import cv2

def rt_anno_vol(h5_path):
    # ROI names
    f = h5py.File(h5_path, "r")

    CT_vol = f['ct_vol'][()]
    CT_header = f['ct_header'][()]
    ds = pydicom.dataset.Dataset.from_json(f['rtss_header'][()])
    
    header_temp = []
    for header in CT_header:
        header_temp.append(pydicom.dataset.Dataset.from_json(header))
    CT_header = header_temp

    ROIname = [ds.StructureSetROISequence[i].ROIName for i in range(len(ds.StructureSetROISequence))]
    ROIname = np.array(list(map(lambda x: x.upper(), ROIname)))

    # draw contours
    ds_ROIContourSequence = ds.ROIContourSequence
    pixelSpacing = CT_header[0]['PixelSpacing'].value
    sliceThickness = CT_header[0]['SliceThickness'].value
    patient_position = np.array(CT_header[0].ImagePositionPatient, dtype="float32")
    rt_annotation_volume = np.zeros(((len(ds.StructureSetROISequence),) + (CT_vol.shape)), dtype=np.int8)
    temp_map = [[ ds_ROIContourSequence[i].ContourSequence[j].ContourData for j in range(len(ds_ROIContourSequence[i].ContourSequence)) ] for i in range(len(ds_ROIContourSequence))]

    print("patient_position:", patient_position)
    print("Countour num:", len(ds_ROIContourSequence))

    print("Coordinate transform start.")
    starttime = time.time()
    for i in range(len(ds_ROIContourSequence)): # i-th countour in vol
        print("Countour name: {}".format(ROIname[i]))
        try:
            rt_annotation_volume = pixel_translation(rt_annotation_volume, i, temp_map,  patient_position, pixelSpacing, sliceThickness)
        except:
            rt_annotation_volume[i, :, :, :] = 0
    print("Coordinate transform complete.")
    stoptime = time.time()
    print("Contour drawing time: {}".format(stoptime-starttime))

    return rt_annotation_volume

def pixel_translation(rt_annotation_volume, i, temp_map,  patient_position, pixelSpacing, sliceThickness):
    for j in range(len(temp_map[i])): # j-th z-axis layer of countour
        for k in range(int(len(temp_map[i][j])/3)): # k-th point of j-th layer
            point_x, point_y, point_z = np.array(temp_map[i][j][(k * 3):(k * 3 + 3)], dtype="float32") # ContourData is a continous list in format [x1,y1,z1,x2,y2,z2,x3......]
            point_x = int(np.round(abs(point_x - patient_position[0]) / pixelSpacing[0]))  # 將mm座標轉換為pixel座標
            point_y = int(np.round(abs(point_y - patient_position[1]) / pixelSpacing[1]))
            point_z = int(np.round(abs((point_z - patient_position[2]) / sliceThickness)))

            rt_annotation_volume[i, point_z, point_y, point_x] = 1  # 0是背景 1是某某東西
            # rt_contour_pixelmap[i][j].extend([point_x, point_y, point_z])
    return rt_annotation_volume

def render(rt_annotation_volume, vol, ds, output_path):
    print("Rendering RT-CT images......")
    vfill = np.zeros(vol.shape+(3,))
    for i in range(len(vol)):
        vfill[i] = cv2.cvtColor(np.uint8(vol[i]), cv2.COLOR_GRAY2BGR)
    ROIname = [ds.StructureSetROISequence[i].ROIName for i in range(len(ds.StructureSetROISequence))]
    ROIname = np.array(list(map(lambda x: x.upper(), ROIname)))
        
    for i in range(len(ds.StructureSetROISequence)): # i-th countour
        color = tuple(np.random.choice(range(256), size=3))
        color = (int(color[0]),int(color[1]),int(color[2])) 
        for j in range(len(vfill)): # j-th z layer
            cv2.putText(vfill[j], ROIname[i], (10, 10+10*i), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1, cv2.LINE_AA)
            imgTemp = rt_annotation_volume[i, j, :, :]
            imgTemp = imgTemp.astype("uint8")
            ret, binary = cv2.threshold(imgTemp, 0, 255, cv2.THRESH_BINARY)
            img = imgTemp.copy()
            contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                cv2.drawContours(vfill[j], [contour], -1, color, thickness=1)

    for i in range(len(vfill)):
        cv2.imwrite(os.path.join(output_path, str(i)+".png"), vfill[i])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to dicom data folders", nargs="*")
    args = parser.parse_args()

    if len(args.path)>0:
        for i in range(len(args.path)):
            if os.path.isfile(args.path[i]):
                print("Processing path:", args.path[i])
                rt_anno_vol(args.path[i])
            else:
                print(args.path[i], "is not a file, skipped.")
    else:
        print("No dataset path input")

if __name__ == '__main__':
    main()