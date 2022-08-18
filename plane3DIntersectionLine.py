import numpy as np

class rectangle3D:
    class lineSegment:
        def __init__(self, position, stepSize, stepNum):
            self.position = position
            self.stepSize = stepSize
            self.stepNum = stepNum
        
        def stepNum_is_in_lineSeg_boundery(self, intput_stepNum):
            if intput_stepNum>=0 and intput_stepNum<self.stepNum:
                return True
            else:
                #print(f"ERROR: intput_stepNum {intput_stepNum} out of boundary [0, {self.stepNum})")
                return False

    def __init__(self, position, orientation, pixelspacing, shape):
        '''
        Arguments:
            position: [x, y, z]
            orientation: [orientation_Xx, orientation_Xy, orientation_Xz, orientation_Yx, orientation_Yy, orientation_Yz]
            pixelspacing: [Row Spacing, Col Spacing]
            shape: [Row, Col]
        '''
        self.position = position
        self.shape = np.array(shape)
        self.orientationX = np.array(orientation[0:3])
        self.orientationY = np.array(orientation[3:6])
        self.pixelspacing = np.array(pixelspacing)
        self.borders = self.computeRectangleBorders()
        self.planeCoefficient, self.planeContant = self.computePlaneCoefficient()

    def computeRectangleBorders(self):
        endpointX = self.position + self.orientationX * self.pixelspacing[1] * self.shape[1]
        endpointY = self.position + self.orientationY * self.pixelspacing[0] * self.shape[0]
        borderX1 = self.lineSegment(self.position, self.orientationX * self.pixelspacing[1], self.shape[1])
        borderX2 = self.lineSegment(endpointY,     self.orientationX * self.pixelspacing[1], self.shape[1])
        borderY1 = self.lineSegment(self.position, self.orientationY * self.pixelspacing[0], self.shape[0])
        borderY2 = self.lineSegment(endpointX,     self.orientationY * self.pixelspacing[0], self.shape[0])
        return [borderX1, borderX2, borderY1, borderY2]

    def computePlaneCoefficient(self):
        '''
        Return an array of plane coefficient
            orientation = [a1, b1, c1, a2, b2, c2]
            ax+by+cz=N
            a = |b1 c1|  b = |c1 a1|  c = |a1 b1|
                |b2 c2|,     |c2 a2|,     |a2 b2|
        '''
        coefficient = np.cross(self.orientationX, self.orientationY)
        constant = np.sum(coefficient*self.position)
        return coefficient, constant

    def spacePosition(self, space_position):
        '''
        Convert position on rectangle to absolute space position
        '''
        x_in, y_in = space_position
        delta_y = y_in * self.orientationY * self.pixelspacing[0]
        delta_x = x_in * self.orientationX * self.pixelspacing[1]
        return self.position + delta_x + delta_y

    def spacePointIsOnPlane(self, absoluteSpacePoint):
        if np.round(sum(absoluteSpacePoint*self.planeCoefficient), 2)==np.round(self.planeContant, 2):
            return True
        else:
            print("Space point is not on plane")
            print(sum(absoluteSpacePoint*self.planeCoefficient), self.planeContant)
            return False

    def rectanglePositionOfSpacePoint(self, absoluteSpacePoint, acceptOOB=False):
        '''
        Compute rectangle position of a space point
        acceptOOB: accept out of boundary i.e. on plane but not in shape range
        '''
        assert len(absoluteSpacePoint)==3
        if self.spacePointIsOnPlane(absoluteSpacePoint):
            absoluteSpacePoint = np.array(absoluteSpacePoint)
            delta = absoluteSpacePoint - self.position
            orientationSum = self.orientationX + self.orientationY

            # Evaluate x and y position by 2 more significant axis
            non_significant_axis = np.argmin(np.absolute(orientationSum))
            orientationMajor = np.matrix([  np.delete(self.orientationX, non_significant_axis), 
                                            np.delete(self.orientationY, non_significant_axis)])
            deltaMajor = np.matrix(np.delete(delta, non_significant_axis))
            onRectanglePosition = np.array((orientationMajor.T.getI() * deltaMajor.T).T).flatten() / self.pixelspacing

            # Check the point is in rectangular(no negative position or out of boundary), flip for self.shape is (y, x) shape
            if (onRectanglePosition>=0).all() and (onRectanglePosition<=np.flip(self.shape)).all(): 
                return onRectanglePosition
            else:
                if acceptOOB:
                    return onRectanglePosition
                else:    
                    #print(f"WARNING: onRectanglePosition {onRectanglePosition} out of boundary, skip")
                    return False
        else:
            #print("ERROR: absoluteSpacePoint is not on plane")
            return False
    
    def rectanglePositionofPointProjection(self, absoluteSpacePoint):
        '''
        Find point projection to plane and distance
        '''
        t = (self.planeContant - np.sum(self.planeCoefficient*absoluteSpacePoint)) / np.sum(self.planeCoefficient**2)
        projection = absoluteSpacePoint + t*self.planeCoefficient

        return projection, np.linalg.norm(t*self.planeCoefficient)

    def rectanglesIntersectionPoint(self, otherrectangle):
        '''
        Calculation 2 rectangle intersection point(s) on self rectangle
        Could be 1 or 2 points
        '''
        if not isinstance(otherrectangle, rectangle3D):
            print("Argument is not class rectangle3D, exit.")

        # Run through all edges of 2 rectangles to find intersections
        intersection_points = [] 
        for i in range(len(self.borders)):
            lineSegrectangleISpoint = self.lineSegmentandRectangleIntersection(self.borders[i], otherrectangle)
            if isinstance(lineSegrectangleISpoint, np.ndarray):
                intersection_points.append(lineSegrectangleISpoint)
        for i in range(len(otherrectangle.borders)):
            lineSegrectangleISpoint = self.lineSegmentandRectangleIntersection(otherrectangle.borders[i], self)
            if isinstance(lineSegrectangleISpoint, np.ndarray):
                intersection_points.append(lineSegrectangleISpoint)
        
        # No intersection
        if len(intersection_points)==0:
            print("No valid intersection point.")
            return False

        # Remove same points
        intersection_points = np.round(intersection_points, 3)
        intersection_points_unique = []
        for i in range(len(intersection_points)):
            intersection_point = intersection_points[i].tolist()
            if intersection_point not in intersection_points_unique:
                intersection_points_unique.append(intersection_point)

        # Convert to position on self plane
        intersection_points_output = []
        for i in range(len(intersection_points_unique)):
            onRectanglePosition = self.rectanglePositionOfSpacePoint(intersection_points_unique[i], acceptOOB=True)
            intersection_points_output.append(onRectanglePosition)

        # Fix points out of boundary
        if len(intersection_points_output)==2:
            intersection_points_output=sorted(intersection_points_output, key = lambda s: s[0], reverse=False)
            slope = (intersection_points_output[1][1]-intersection_points_output[0][1]) / (intersection_points_output[1][0]-intersection_points_output[0][0])
            for i in range(len(intersection_points_output)):
                if intersection_points_output[i][0]<0:
                    new_x = 0
                    new_y = intersection_points_output[i][1] + (new_x - intersection_points_output[i][0]) * slope
                    intersection_points_output[i][0] = new_x
                    intersection_points_output[i][1] = new_y

                elif intersection_points_output[i][0]>=np.flip(self.shape)[0]:
                    new_x = np.flip(self.shape)[0]-1
                    new_y = intersection_points_output[i][1] - (intersection_points_output[i][0]-new_x) * slope
                    intersection_points_output[i][0] = new_x
                    intersection_points_output[i][1] = new_y
            
                if intersection_points_output[i][1]<0:
                    new_y = 0
                    new_x = intersection_points_output[i][0] + (new_y - intersection_points_output[i][1]) / slope
                    intersection_points_output[i][0] = new_x
                    intersection_points_output[i][1] = new_y

                elif intersection_points_output[i][1]>=np.flip(self.shape)[1]:
                    new_y = np.flip(self.shape)[1]-1
                    new_x = intersection_points_output[i][0] - (intersection_points_output[i][1]-new_y) / slope
                    intersection_points_output[i][0] = new_x
                    intersection_points_output[i][1] = new_y

            return np.array(intersection_points_output)
        
        else: 
            print("ERROR: intersection points are more than 2.")
            return False
        
    def lineSegmentandRectangleIntersection(self, lineSeg:lineSegment, rectangle):
        # Formula: sum((lineSeg.position + torectangleSteps * lineSeg.stepSize) * rectangle.planeCoefficient) = rectangle.planeContant
        torectangleSteps = (rectangle.planeContant - sum(lineSeg.position * rectangle.planeCoefficient)) / sum(rectangle.planeCoefficient * lineSeg.stepSize)
        if lineSeg.stepNum_is_in_lineSeg_boundery(torectangleSteps):
            intersectionSpacePosition = lineSeg.position + torectangleSteps*lineSeg.stepSize
            onRectanglePosition = rectangle.rectanglePositionOfSpacePoint(intersectionSpacePosition)
            if isinstance(onRectanglePosition, np.ndarray):
                return intersectionSpacePosition
            else:
                return False 
        else:
            return False 

def customAPI(source_position, source_orientation, target_position, target_orientation, source_pixelSpacing, target_pixelSpacing, source_shape, target_shape):
    rectangle_source = rectangle3D( source_position, 
                                    source_orientation, 
                                    [source_pixelSpacing, source_pixelSpacing], 
                                    source_shape)
    rectangle_target = rectangle3D( target_position, 
                                    target_orientation, 
                                    [target_pixelSpacing, target_pixelSpacing], 
                                    target_shape)
    
    X1 = -9999
    Y1 = -9999
    X2 = -9999
    Y2 = -9999

    endPoint = rectangle_target.rectanglesIntersectionPoint(rectangle_source)
    if isinstance(endPoint, np.ndarray):
        X1 = round(endPoint[0][0])
        Y1 = round(endPoint[0][1])
        X2 = round(endPoint[1][0])
        Y2 = round(endPoint[1][1])

    return X1, Y1, X2, Y2

def MRI_coordinate_API(source_position, source_orientation, target_position, target_orientation, source_pixelSpacing, target_pixelSpacing, source_shape, target_shape,x,y):
    rectangle_source = rectangle3D( source_position, 
                                    source_orientation, 
                                    [source_pixelSpacing, source_pixelSpacing], 
                                    source_shape)

    
    pointA = rectangle_source.spacePosition([x,y])

    projection = []
    distance = []
    target_position = np.array(target_position)
    for i in range(len(target_position)): 
        rectangle_target = rectangle3D( target_position[i], 
                                target_orientation, 
                                [target_pixelSpacing, target_pixelSpacing], 
                                target_shape)
        p,d = rectangle_target.rectanglePositionofPointProjection(pointA)
        projection.append(p)
        distance.append(d)
    
    rectangle_target = rectangle3D( target_position[np.argmin(distance)], 
                        target_orientation, 
                        [target_pixelSpacing, target_pixelSpacing], 
                        target_shape)
    targetSpacePoint = rectangle_target.rectanglePositionOfSpacePoint(projection[np.argmin(distance)])
    
    if np.sum(np.array(targetSpacePoint) != False) ==2:
        x=targetSpacePoint[0]
        y=targetSpacePoint[1]
        z=np.argmin(distance)
        return round(x),round(y),round(z)
    else:
        return -1,-1,-1
        
def main():
    # axialrectangle = rectangle3D(   [-124.0125763,	-114.9357319, 125.4842253], 
    #                                 [0.999463166, 0.029058569, -0.015132052, -0.029663405, 0.998701754, -0.041411211], 
    #                                 [0.4883, 0.4883], 
    #                                 [512, 512])
    # # coronalrectangle = rectangle3D( [-126.8027602, -68.36475095, 120.177609], 
    # #                                 [0.998216933, 0.059690486, -0.000000002515556, -0.003249074, 0.054334929, -0.998517481], 
    # #                                 [0.4883, 0.4883], 
    # #                                 [512, 512])

    # coronalrectangle = rectangle3D( [-131.09410340088,3.4003171076326, 124.09671139667], 
    #                                 [0.998216933, 0.059690486, -0.000000002515556, -0.003249074, 0.054334929, -0.998517481], 
    #                                 [0.4883, 0.4883], 
    #                                 [512, 512])

    # sagittalrectangle = rectangle3D([63.665592891424, -107.97515826229, 122.40478362542], 
    #                                 [-0.0468447937367, 0.99890218004556, -0.000000016686574, 0.00044797727697, 0.00002099176174, -0.999999899437],
    #                                 [0.7813, 0.7813], 
    #                                 [320, 320])

    axialrectangle = rectangle3D(   [-121.93, -142.57, -17.5351], 
                                    [0.999998, -0, -0.0019837, -0, 1, 0], 
                                    [0.4688, 0.4688], 
                                    [512, 512])

    coronalrectangle = rectangle3D( [-139.217, -6.78465, 101.449], 
                                    [0.999849, -0.0173956, 0, 0.00189215, 0.10944, -0.993992], 
                                    [0.5469, 0.5469], 
                                    [512, 512])

    sagittalrectangle = rectangle3D([6.67324, -157.172, 100.216], 
                                    [0.0166328, 0.999862, 0, -0, -0, -1],
                                    [0.5469, 0.5469], 
                                    [512, 512])

    # print(axialrectangle.computePlaneCoefficient())
    # print(coronalrectangle.computePlaneCoefficient())
    # print(axialrectangle.spacePosition([335,207]))
    # print(axialrectangle.rectanglePositionOfSpacePoint([122.7587588, -53.40314016, 119.4716311]))

    # print(axialrectangle.rectanglesIntersectionPoint(coronalrectangle))
    # print(sagittalrectangle.rectanglesIntersectionPoint(coronalrectangle))

    # pointA = axialrectangle.spacePosition([350,250])
    # print(pointA)
    # projection, distance = coronalrectangle.rectanglePositionofPointProjection(pointA)
    #print(coronalrectangle.spacePointIsOnPlane(pointA))

    # pointC = coronalrectangle.spacePosition([357.30, 12.579])
    # print(pointC)
    
    # print("projection:", projection)
    # print("distance:", distance)

    #print(coronalrectangle.rectanglePositionOfSpacePoint(projection))

    endPoint = axialrectangle.rectanglesIntersectionPoint(sagittalrectangle)
    print(endPoint)

if __name__ == '__main__':
    main()