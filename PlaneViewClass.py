
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtCore import QTimer
import vtk




anatomicalAxes = {'Axial': {'Direction Cosines': [1, 0, 0, 0, -1, 0, 0, 0, 1], 'Normal Direction Minimum': -42,'Normal Direction Maximum': 62, 'Normal Direction Index': 2, 'Text Color': [1, 0, 0], 'Horizontal Line Orientation': 'Coronal', 'Horizontal Line Color': [0, 1, 0], 'Vertical Line Orientation': 'Sagittal', 'Vertical Line Color': [0, 0, 1]},
                  'Coronal': {'Direction Cosines': [0, 1, 0, 0, 0, 1, 1, 0, 0], 'Normal Direction Minimum': -151, 'Normal Direction Maximum': 145, 'Normal Direction Index': 0, 'Text Color': [0, 1, 0], 'Horizontal Line Orientation': 'Axial', 'Horizontal Line Color': [1, 0, 0], 'Vertical Line Orientation': 'Sagittal', 'Vertical Line Color': [0, 0, 1]},
                  'Sagittal': {'Direction Cosines': [1, 0, 0, 0, 0, 1, 0, 1, 0], 'Normal Direction Minimum': -153,'Normal Direction Maximum': 147, 'Normal Direction Index': 1, 'Text Color': [0, 0, 1], 'Horizontal Line Orientation': 'Axial', 'Horizontal Line Color': [1, 0, 0], 'Vertical Line Orientation': 'Coronal', 'Vertical Line Color': [0, 1, 0]}}




class DicomViewer:


    brightness = 100
    contrast = 255
    viewers = []
    def __init__(self):
        self.viewers.append(self)

    def increaseBrightness(self):
        self.brightness = self.brightness + 5
        print(self.viewers[0].imageActor.GetProperty().GetColorLevel())
        self.isDragging = True
        for viewer in self.viewers:
            imageProperty = viewer.imageActor.GetProperty()
            
            imageProperty.SetColorLevel(self.brightness)
            viewer.RenderViewer()

    def decreaseBrightness(self):
        self.brightness = self.brightness - 5
        print(self.viewers[0].imageActor.GetProperty().GetColorLevel())
        self.isDragging = True
        for viewer in self.viewers:
            imageProperty = viewer.imageActor.GetProperty()
            
            imageProperty.SetColorLevel(self.brightness)
            viewer.RenderViewer()
    
    def increaseContrast(self):
        self.contrast = self.contrast + 5
        print(self.viewers[0].imageActor.GetProperty().GetColorWindow())
        self.isDragging = True
        for viewer in self.viewers:
            imageProperty = viewer.imageActor.GetProperty()
            
            imageProperty.SetColorWindow(self.contrast)
            viewer.RenderViewer()

    def decreaseContrast(self):
        self.contrast = self.contrast - 5
        print(self.viewers[0].imageActor.GetProperty().GetColorWindow())
        self.isDragging = True
        for viewer in self.viewers:
            imageProperty = viewer.imageActor.GetProperty()
            
            imageProperty.SetColorWindow(self.contrast)
            viewer.RenderViewer()

    


class Line:

    def __init__(self, planeViewer, orientation, color):
        super().__init__()

        self.line = vtk.vtkLineSource()
        self.planeViewer = planeViewer
        self.SetOrientation(orientation)
        self.SetActor(color)
        self.RenderLine()

    def SetOrientation(self, orientation):

        self.orientation = orientation
        if self.orientation == 'Horizontal': self.SetLineCoordinates((-256, 0, 1), (256, 0, 1))
        elif self.orientation == 'Vertical': self.SetLineCoordinates((0, -256, 1), (0, 256, 1))

    def MoveLine(self, newPosition):

        if self.orientation == 'Horizontal': self.SetLineCoordinates((-256, newPosition, 1), (256, newPosition, 1))
        elif self.orientation == 'Vertical': self.SetLineCoordinates((newPosition, -256, 1), (newPosition, 256, 1))
        self.RenderLine()

    def SetLineCoordinates(self, point1, point2):

        self.line.SetPoint1(point1)
        self.line.SetPoint2(point2)

    def SetActor(self, color):

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.line.GetOutputPort())
        
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        
        self.actor.GetProperty().SetColor(color[0], color[1], color[2])
        self.planeViewer.renderer.AddActor(self.actor)

    def SetColor(self, color):

        self.actor.GetProperty().SetColor(color[0], color[1], color[2])
        self.RenderLine()
    
    def RenderLine(self):

        self.planeViewer.RenderViewer()



class PlaneViewer(DicomViewer):

    def __init__(self, mainWindow, gridLayout, orientation, imageMapToColors, uiLocation):
        super().__init__()

        self.lastX, self.lastY = 0, 0
        self.isDragging = False 
        self.orientation = orientation
        self.uiLocation = uiLocation
        self.orientationSwapped = 'Ready'

        self.sliceNumberBeforeCinePlay = anatomicalAxes[self.orientation]['Normal Direction Minimum'] - 1
        self.InitialiseRenderer(mainWindow, gridLayout)
        self.InitialiseSlicer(imageMapToColors)
        self.AssignUIElements(mainWindow, uiLocation)

        self.horizontalLine = Line(self, 'Horizontal', anatomicalAxes[self.orientation]['Horizontal Line Color'])
        self.verticalLine = Line(self, 'Vertical', anatomicalAxes[self.orientation]['Vertical Line Color'])


    def ConnectSliderToIndicators(self, mainWindow):

        for viewer in [mainWindow.axialViewer, mainWindow.coronalViewer, mainWindow.sagittalViewer]:
            if self.orientation != viewer.orientation:
                if anatomicalAxes[viewer.orientation]['Horizontal Line Orientation'] == self.orientation:
                    self.slider.valueChanged.connect(lambda value, viewer=viewer: viewer.horizontalLine.MoveLine(value))
                if anatomicalAxes[viewer.orientation]['Vertical Line Orientation'] == self.orientation:
                    self.slider.valueChanged.connect(lambda value, viewer=viewer: viewer.verticalLine.MoveLine(value))


    def InitialiseRenderer(self,mainWindow, gridLayout):

        self.renderer = vtk.vtkRenderer()
        self.renderWindowInteractor = QVTKRenderWindowInteractor(mainWindow)
        self.renderWindowInteractor.GetRenderWindow().AddRenderer(self.renderer)

        self.interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
        self.renderWindowInteractor.SetInteractorStyle(self.interactorStyle)

        self.iren = self.renderWindowInteractor.GetRenderWindow().GetInteractor()
        
        # Add mouse wheel event to zoom
        self.iren.AddObserver("MouseWheelForwardEvent", self.zoomIn)
        self.iren.AddObserver("MouseWheelBackwardEvent", self.zoomOut)
        
        # remove default left button press and release events
        self.iren.RemoveObservers("LeftButtonPressEvent")
        self.iren.RemoveObservers("LeftButtonReleaseEvent")

        self.iren.AddObserver("LeftButtonPressEvent", self.onLeftButtonPress)
        self.iren.AddObserver("LeftButtonReleaseEvent", self.onLeftButtonRelease)

        self.iren.AddObserver("MouseMoveEvent", self.onMouseMove)

        self.gridLayout = gridLayout
        self.gridLayout.insertWidget(0, self.renderWindowInteractor)
    

    def onLeftButtonRelease(self, obj, event):
        self.isDragging = False


    def onLeftButtonPress(self, obj, event):
        self.isDragging = True


    def onMouseMove(self, obj, event):
        # check if used is clicking the left button
        if self.isDragging:
            # Get the current X coordinate of the mouse
            currentX = obj.GetEventPosition()[0]
            deltaX = currentX - self.lastX

            # Check if the movement is significant
            if abs(deltaX) > 1:
                if deltaX > 0:
                    # User is dragging the mouse to the right
                    if obj.GetShiftKey(): 
                        self.increaseBrightness()
                        print("increase brightness")
                    else:
                        self.increaseContrast()
                        print("increase contrast")
                else:
                    # User is dragging the mouse to the left
                    if obj.GetShiftKey():
                        self.decreaseBrightness()
                        print("decrease brightness")
                    else:
                        self.decreaseContrast()
                        print("decrease contrast")
            
            # Update the X coordinate of the mouse
            self.lastX = currentX


    def zoomIn(self, obj, event):
        camera = self.renderer.GetActiveCamera()
        camera.Zoom(1.1)
        self.RenderViewer()


    def zoomOut(self, obj, event):
        camera = self.renderer.GetActiveCamera()
        camera.Zoom(0.9)
        self.RenderViewer()


    def InitialiseSlicer(self, imageMapToColors):

        self.reslicer = vtk.vtkImageReslice()
        directionCosines = anatomicalAxes[self.orientation]['Direction Cosines']

        self.reslicer.SetResliceAxesDirectionCosines(directionCosines[0], directionCosines[1], directionCosines[2], directionCosines[3], directionCosines[4], directionCosines[5], directionCosines[6], directionCosines[7], directionCosines[8])
        self.reslicer.SetInputConnection(imageMapToColors.GetOutputPort())
        self.reslicer.SetOutputDimensionality(2)
        self.reslicer.SetInterpolationModeToLinear()
        self.reslicer.UpdateWholeExtent()

        self.imageActor = vtk.vtkImageActor()
        self.imageActor.GetMapper().SetInputConnection(self.reslicer.GetOutputPort())
        self.renderer.AddActor(self.imageActor)
        
        self.renderer.AddActor(self.imageActor)
        self.textActor = vtk.vtkTextActor()
        self.textActor.SetInput(str(self.orientation))
        textColor = anatomicalAxes[self.orientation]['Text Color']
        self.textActor.GetTextProperty().SetColor(textColor[0], textColor[1], textColor[2])  # Set text color to green
        self.textActor.GetTextProperty().SetFontSize(20)
        self.textActor.GetTextProperty().SetFontFamilyToArial()
        self.textActor.GetTextProperty().SetBold(True)
        self.textActor.SetPosition(10, 10)

        self.renderer.AddActor(self.textActor)


    def AssignUIElements(self, mainWindow, uiLocation):

        self.slider = mainWindow.uiElementBlocks[uiLocation]['Slider']
        self.slider.valueChanged.connect(lambda: self.SliderScroll(self.slider.value()))
        self.slider.setMaximum(anatomicalAxes[self.orientation]['Normal Direction Maximum'])
        self.slider.setMinimum(anatomicalAxes[self.orientation]['Normal Direction Minimum'])
        self.slider.setValue(0)


        self.timer = QTimer(mainWindow)
        self.cineShownSliceNumber = -1
        self.timer.timeout.connect(self.CineProcess)

       # self.playButton = mainWindow.uiElementBlocks[uiLocation]['Play Button']
       # self.playButton.clicked.connect(self.CinePlay)
        self.pauseButton = mainWindow.uiElementBlocks[uiLocation]['Pause Button']
        self.pauseButton.clicked.connect(self.CinePause)
        self.stopButton = mainWindow.uiElementBlocks[uiLocation]['Stop Button']
        self.stopButton.clicked.connect(self.CineStop)

        self.orientationCombobox = mainWindow.uiElementBlocks[uiLocation]['Orientation Combobox']
        self.orientationCombobox.currentTextChanged.connect(lambda: self.SetViewerOrientation(mainWindow, None))


    def SetViewerOrientation(self, mainWindow, newOrientation):
        
        if self.orientationSwapped == 'Done': return

        self.pastOrientation = self.orientation
        if newOrientation == None: self.orientation = self.orientationCombobox.currentText()
        else:
            self.orientationSwapped = 'Done'
            self.orientation = newOrientation
            self.orientationCombobox.setCurrentText(self.orientation)
        
        directionCosines = anatomicalAxes[self.orientation]['Direction Cosines']
        self.reslicer.SetResliceAxesDirectionCosines(directionCosines[0], directionCosines[1], directionCosines[2], directionCosines[3], directionCosines[4], directionCosines[5], directionCosines[6], directionCosines[7], directionCosines[8])
        
        self.slider.setMaximum(anatomicalAxes[self.orientation]['Normal Direction Maximum'])
        self.slider.setMinimum(anatomicalAxes[self.orientation]['Normal Direction Minimum'])
        self.cineShownSliceNumber = anatomicalAxes[self.orientation]['Normal Direction Minimum'] - 1
        self.SliderScroll(0)
        
        self.textActor.SetInput(str(self.orientation))
        textColor = anatomicalAxes[self.orientation]['Text Color']
        self.textActor.GetTextProperty().SetColor(textColor[0], textColor[1], textColor[2])
        
        self.horizontalLine.SetOrientation('Horizontal')
        self.verticalLine.SetOrientation('Vertical')
        self.horizontalLine.SetColor(anatomicalAxes[self.orientation]['Horizontal Line Color'])
        self.verticalLine.SetColor(anatomicalAxes[self.orientation]['Vertical Line Color'])

        mainWindow.DisconnectAllSliders()
        mainWindow.ConnectAllSliders()

        self.RenderViewer()

        if self.orientationSwapped == 'Ready': mainWindow.SwapViewers(self)
        elif self.orientationSwapped == 'Done': self.orientationSwapped = 'Ready'


   # def CinePlay(self):

    #    self.slider.setEnabled(False)
     #self.sliceNumberBeforeCinePlay = self.slider.value()
      #  self.timer.start(30)


    def CinePause(self):

        if self.timer.isActive(): 
            self.timer.stop()
        else: 
            self.slider.setEnabled(False)
            self.sliceNumberBeforeCinePlay = self.slider.value()
            self.timer.start(30)


    def CineStop(self):

        self.timer.stop()
        self.SliderScroll(self.sliceNumberBeforeCinePlay)
        self.slider.setEnabled(True)
        self.slider.setValue(self.sliceNumberBeforeCinePlay)


    def CineProcess(self):
    
        if self.cineShownSliceNumber + 1 > anatomicalAxes[self.orientation]['Normal Direction Maximum']: self.cineShownSliceNumber = anatomicalAxes[self.orientation]['Normal Direction Minimum'] - 1
        else: self.cineShownSliceNumber = self.cineShownSliceNumber + 1
        self.SliderScroll(self.cineShownSliceNumber)


    def SliderScroll(self, sliceNumber):

        resliceMatrix = self.reslicer.GetResliceAxes()
        resliceMatrix.SetElement(anatomicalAxes[self.orientation]['Normal Direction Index'], 3, sliceNumber)
        self.reslicer.UpdateWholeExtent()
        self.RenderViewer()

    
    def RunViewer(self): self.iren.Initialize()


    def RenderViewer(self): self.renderWindowInteractor.GetRenderWindow().Render()


    def CloseViewer(self): self.renderWindowInteractor.close()
