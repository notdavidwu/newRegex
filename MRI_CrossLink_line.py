import numpy as np
def MRI_CrossLink_line(self_view_position,self_view_orientation,another_view_position,another_view_orientation,self_view_pixelspacing,another_view_pixelspacing,self_shape):
    anatomicalPlanesArgs = np.array([0,0,0],dtype=np.float64)

    anatomicalPlanesArgs[0] = another_view_orientation[1]*another_view_orientation[5]-another_view_orientation[4]*another_view_orientation[2]
    anatomicalPlanesArgs[1] = another_view_orientation[2]*another_view_orientation[3]-another_view_orientation[5]*another_view_orientation[0]
    anatomicalPlanesArgs[2] = another_view_orientation[0]*another_view_orientation[4]-another_view_orientation[3]*another_view_orientation[1]
    anatomicalPlanesConstant = sum(anatomicalPlanesArgs * another_view_position)
    
    self_view_orientation_matrix = np.zeros((2,3), dtype=np.float64)
    self_view_orientation_matrix[0] = self_view_orientation[0:3]
    self_view_orientation_matrix[1] = self_view_orientation[3:6]

    another_view_orientation_matrix = np.zeros((2,3), dtype=np.float64)
    another_view_orientation_matrix[0] = another_view_orientation[0:3]
    another_view_orientation_matrix[1] = another_view_orientation[3:6]
    self_view_position_Args = []
    step_Args = []

    #左上端點
    step_Args, self_view_position_Args = caculate_step(self_view_position,self_view_position_Args,self_view_orientation_matrix,anatomicalPlanesConstant,anatomicalPlanesArgs,step_Args)

    #右上端點
    self_view_position_rightTop = self_view_position+self_view_orientation_matrix[0]*self_shape[1]*self_view_pixelspacing
    step_Args, self_view_position_Args = caculate_step(self_view_position_rightTop,self_view_position_Args,self_view_orientation_matrix,anatomicalPlanesConstant,anatomicalPlanesArgs,step_Args)
    
    #左下端點
    self_view_position_leftBottom = self_view_position+self_view_orientation_matrix[1]*self_shape[0]*self_view_pixelspacing
    step_Args, self_view_position_Args = caculate_step(self_view_position_leftBottom,self_view_position_Args,self_view_orientation_matrix,anatomicalPlanesConstant,anatomicalPlanesArgs,step_Args)
    
    #右下端點
    self_view_position_rightBottom = self_view_position_leftBottom+self_view_orientation_matrix[0]*self_shape[1]*self_view_pixelspacing
    step_Args, self_view_position_Args = caculate_step(self_view_position_rightBottom,self_view_position_Args,self_view_orientation_matrix,anatomicalPlanesConstant,anatomicalPlanesArgs,step_Args)
    
    #check 負負
    step_Args = np.array(step_Args)
    step_Args[step_Args<0] = 999999
    getValue = step_Args[np.argsort(step_Args)==0]
    decidePoints = getValue.argsort()[0:2]
    decide = np.argmin(np.abs(np.sum(another_view_orientation_matrix,axis=0)))
    another_view_orientation_matrix = np.delete(another_view_orientation_matrix, decide, axis=1)
    startPointX, startPointY = caculate_pixelPoint(self_view_position_Args,decidePoints[0],step_Args,self_view_orientation_matrix,another_view_position,decide,another_view_orientation_matrix,another_view_pixelspacing)
    endPointX, endPointY = caculate_pixelPoint(self_view_position_Args,decidePoints[1],step_Args,self_view_orientation_matrix,another_view_position,decide,another_view_orientation_matrix,another_view_pixelspacing)
    return startPointX,startPointY,endPointX,endPointY

def caculate_step(self_view_position,self_view_position_Args,self_view_orientation_matrix,anatomicalPlanesConstant,anatomicalPlanesArgs,step_Args):
    stepX = (anatomicalPlanesConstant - sum(self_view_position*anatomicalPlanesArgs))/sum(self_view_orientation_matrix[0]*anatomicalPlanesArgs)
    stepY = (anatomicalPlanesConstant - sum(self_view_position*anatomicalPlanesArgs))/sum(self_view_orientation_matrix[1]*anatomicalPlanesArgs)
    step = [stepX,stepY]
    step_Args.append(step)
    self_view_position_Args.append(self_view_position)
    return step_Args,self_view_position_Args

def caculate_pixelPoint(self_view_position_Args,decidePoints,step_Args,self_view_orientation_matrix,another_view_position,decide,another_view_orientation_matrix,another_view_pixelspacing):
    self_view_position_Point = self_view_position_Args[decidePoints]
    step = step_Args[decidePoints]
    vectorIndex = [np.argmin(step),np.argmax(step)]
    intersectionPoint = self_view_position_Point + self_view_orientation_matrix[vectorIndex[0]]*step[vectorIndex[0]]  
    deltaDistance = np.array(intersectionPoint - another_view_position)
    deltaDistance = np.delete(deltaDistance, decide)
    targetPoint = np.round(np.matmul(np.linalg.inv(np.transpose(another_view_orientation_matrix)),deltaDistance)/another_view_pixelspacing)
    PointX = int(targetPoint[0])
    PointY = int(targetPoint[1])
    return PointX,PointY