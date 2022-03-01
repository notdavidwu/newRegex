import numpy as np
def MRI_CrossLink_line(self_view_position,self_view_orientation,another_view_position,another_view_orientation,self_pixelspacing,self_vol_size):
    anatomicalPlanesArgs = np.zeros((1,3), dtype=np.float64)
    anatomicalPlanesArgs[0, 0] = another_view_orientation[1]*another_view_orientation[5]-another_view_orientation[4]*another_view_orientation[2]
    anatomicalPlanesArgs[0, 1] = another_view_orientation[2]*another_view_orientation[3]-another_view_orientation[5]*another_view_orientation[0]
    anatomicalPlanesArgs[0, 2] = another_view_orientation[0]*another_view_orientation[4]-another_view_orientation[3]*another_view_orientation[1]
    anatomicalPlanesArgs * another_view_position
    anatomicalPlanesConstant = sum(anatomicalPlanesArgs * another_view_position)
    self_view_orientation_matrix = np.zeros((2,3), dtype=np.float64)
    self_view_orientation_matrix[0] = self_view_orientation[0:3]
    self_view_orientation_matrix[1] = self_view_orientation[3:6]

    another_view_orientation_matrix = np.zeros((2,3), dtype=np.float64)
    another_view_orientation_matrix[0] = another_view_orientation[0:3]
    another_view_orientation_matrix[1] = another_view_orientation[3:6]
    try:
        stepX = (anatomicalPlanesConstant - sum(self_view_position*anatomicalPlanesArgs))/sum(self_view_orientation_matrix[0]*anatomicalPlanesArgs)
        if stepX > 2000:
            stepX = 0
    except:
        stepX = 0
    try:
        stepY = (anatomicalPlanesConstant - sum(self_view_position*anatomicalPlanesArgs))/sum(self_view_orientation_matrix[1]*anatomicalPlanesArgs)
        if stepY > 2000:
            stepY = 0
    except:
        stepY = 0

    step = np.array([stepX,stepY])
    vectorIndex = [np.argmax(step),np.argmin(step)]
    
    intersectionPoint = self_view_position + self_view_orientation_matrix[vectorIndex[0]]*step[vectorIndex[0]]
    decide = np.argmin(np.sum(another_view_orientation_matrix,axis=0))

    endIntersectionPoint = intersectionPoint+another_view_orientation_matrix[vectorIndex[1]]*self_vol_size[vectorIndex[1]]*self_pixelspacing
    another_view_orientation_matrix = np.delete(another_view_orientation_matrix, decide, axis=1)
    
    deltaDistance = endIntersectionPoint - another_view_position
    deltaDistance = np.delete(deltaDistance, decide)
    targetPoint = np.round(np.matmul(np.linalg.inv(np.transpose(another_view_orientation_matrix)),deltaDistance)/self_pixelspacing)
    
    endPointX = targetPoint[0]
    endPointY = targetPoint[1]
    

    deltaDistance = intersectionPoint - another_view_position
    deltaDistance = np.delete(deltaDistance, decide)
    targetPoint = np.round(np.matmul(np.linalg.inv(np.transpose(another_view_orientation_matrix)),deltaDistance)/self_pixelspacing)
    
    startPointX = targetPoint[0]
    startPointY = targetPoint[1]


    return startPointX,startPointY,endPointX,endPointY

self_view_position = [-125.76511761325,-120.20730115231,-0.3932513843826]
self_view_orientation = [0.99946316619053,0.02905856922976,-0.0151320515043,-0.029663404957,0.99870175430236,-0.0414112105564]
self_pixelspacing = 0.4883
self_vol_size = [512,512]

another_view_position = [39.691941005438,-109.09943156246,122.394019414]
another_view_orientation = [-0.0468447937367,0.99890218004556,-1.6686574e-008,0.00044797727697,2.099176174e-005,-0.9999998994378]

self_view_position,self_view_orientation,another_view_position,another_view_orientation,self_pixelspacing,self_vol_size
print(MRI_CrossLink_line(self_view_position,self_view_orientation,another_view_position,another_view_orientation,self_pixelspacing,self_vol_size))