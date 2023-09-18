
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile
from PlaneViewClass import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import vtk
import sys
import os




ui,_ = loadUiType(os.path.join(os.path.dirname(__file__),'MPR_UI2.ui'))




class MainWindow(QtWidgets.QMainWindow, ui):


    def __init__(self, parent = None):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        super().__init__()
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Load and apply the darkeum style sheet
        style_sheet_file = QFile("darkeum_stylesheet.qss")
        style_sheet_file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = style_sheet_file.readAll().data().decode()
        self.setStyleSheet(style_sheet)

        self.uiElementBlocks = {'Top Left': {'Slider': self.topLeftView_verticalSlider,
                                             #'Play Button': self.topLeftView_playButton,
                                             'Pause Button': self.topLeftView_pauseButton,
                                             'Stop Button': self.topLeftView_stopButton,
                                             'Orientation Combobox': self.topLeftView_comboBox},

                                'Top Right': {'Slider': self.topRightView_verticalSlider,
                                              #'Play Button': self.topRightView_playButton,
                                              'Pause Button': self.topRightView_pauseButton,
                                              'Stop Button': self.topRightView_stopButton,
                                              'Orientation Combobox': self.topRightView_comboBox},

                                'Bottom Left': {'Slider': self.bottomLeftView_verticalSlider,
                                                #'Play Button': self.bottomLeftView_playButton,
                                                'Pause Button': self.bottomLeftView_pauseButton,
                                                'Stop Button': self.bottomLeftView_stopButton,
                                                'Orientation Combobox': self.bottomLeftView_comboBox},
                                              
                                'Bottom Right': {'Slider': self.bottomRightView_verticalSlider,
                                                 #'Play Button': self.bottomRightView_playButton,
                                                 'Pause Button': self.bottomRightView_pauseButton,
                                                 'Stop Button': self.bottomRightView_stopButton,
                                                 'Orientation Combobox': self.bottomRightView_comboBox} }
        # Hide the UI components initially
        self.topLeftView_comboBox.setVisible(False)
        self.topRightView_comboBox.setVisible(False)
        self.bottomLeftView_comboBox.setVisible(False)
        self.bottomRightView_comboBox.setVisible(False)
        self.topLeftView_verticalSlider.setVisible(False)
        #self.topLeftView_playButton.setVisible(False)
        self.topLeftView_pauseButton.setVisible(False)
        self.topLeftView_stopButton.setVisible(False) 
        self.topleft_maximizebutton.setVisible(False)

        self.topRightView_verticalSlider.setVisible(False)
        #self.topRightView_playButton.setVisible(False)
        self.topRightView_pauseButton.setVisible(False)
        self.topRightView_stopButton.setVisible(False)
        self.topright_maximizebutton.setVisible(False)

        self.bottomLeftView_verticalSlider.setVisible(False)
       # self.bottomLeftView_playButton.setVisible(False)
        self.bottomLeftView_pauseButton.setVisible(False)
        self.bottomLeftView_stopButton.setVisible(False)
        self.bottomleft_maximizebutton.setVisible(False)

        self.bottomRightView_verticalSlider.setVisible(False)
      #  self.bottomRightView_playButton.setVisible(False)
        self.bottomRightView_pauseButton.setVisible(False)
        self.bottomRightView_stopButton.setVisible(False)
        self.buttomright_maximizebutton.setVisible(False)
       
        self.top_left_minimize_button.setVisible(False)
        self.top_right_minimize_button.setVisible(False)
        self.bottom_left_minimize_button.setVisible(False)
        self.bottom_right_minimize_button.setVisible(False)  

        self.actionOpen.triggered.connect(self.OpenFile)
        self.topleft_maximizebutton.clicked.connect(self.maximize_topleft)
        self.topright_maximizebutton.clicked.connect(self.maximize_topright)
        self.bottomleft_maximizebutton.clicked.connect(self.maximize_bottomleft)
        self.buttomright_maximizebutton.clicked.connect(self.maximize_buttomright)
        
        self.top_left_minimize_button.clicked.connect(self.minimize_topleft)
        self.top_right_minimize_button.clicked.connect(self.minimize_topright)
        self.bottom_left_minimize_button.clicked.connect(self.minimize_bottomleft)
        self.bottom_right_minimize_button.clicked.connect(self.minimize_bottomright)
        
        # self.minimize_button.clicked.connect(self.Minimize)


    def OpenFile(self):

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", os.path.dirname(__file__) + "/Dataset", "Case Files (*.mhd)")
        if file_name == "": return
        self.ReadData()
        print(self.imageMapToColors)
        self.axialViewer = PlaneViewer(self, self.topLeftView_gridLayout, 'Axial', self.imageMapToColors, 'Top Left')
        self.coronalViewer = PlaneViewer(self, self.topRightView_gridLayout, 'Coronal', self.imageMapToColors, 'Top Right')
        self.sagittalViewer = PlaneViewer(self, self.bottomRightView_gridLayout, 'Sagittal', self.imageMapToColors, 'Bottom Right')

        self.ConnectAllSliders()
        self.Initial_nofiletext.setVisible(False)
        self.topLeftView_comboBox.setVisible(True)
        self.topRightView_comboBox.setVisible(True)
        self.bottomLeftView_comboBox.setVisible(True)
        self.bottomRightView_comboBox.setVisible(True)
        self.topLeftView_verticalSlider.setVisible(True)
        #self.topLeftView_playButton.setVisible(True)
        self.topLeftView_pauseButton.setVisible(True)
        self.topLeftView_stopButton.setVisible(True)
        self.topleft_maximizebutton.setVisible(True)

        self.topRightView_verticalSlider.setVisible(True)
        #self.topRightView_playButton.setVisible(True)
        self.topRightView_pauseButton.setVisible(True)
        self.topRightView_stopButton.setVisible(True)
        self.topright_maximizebutton.setVisible(True)

        self.bottomLeftView_verticalSlider.setVisible(True)
        #self.bottomLeftView_playButton.setVisible(True)
        self.bottomLeftView_pauseButton.setVisible(True)
        self.bottomLeftView_stopButton.setVisible(True)
        self.bottomleft_maximizebutton.setVisible(True)

        self.bottomRightView_verticalSlider.setVisible(True)
       # self.bottomRightView_playButton.setVisible(True)
        self.bottomRightView_pauseButton.setVisible(True)
        self.bottomRightView_stopButton.setVisible(True)
        self.buttomright_maximizebutton.setVisible(True)

        self.show()
        
        self.axialViewer.RenderViewer()
        self.axialViewer.RunViewer()
        self.coronalViewer.RenderViewer()
        self.coronalViewer.RunViewer()
        self.sagittalViewer.RenderViewer()
        self.sagittalViewer.RunViewer()
        self.HandleEmptyViewer()
    

    def ConnectAllSliders(self):

        for viewer in [self.axialViewer, self.coronalViewer, self.sagittalViewer]:
            viewer.ConnectSliderToIndicators(self)
            viewer.slider.valueChanged.connect(lambda value, viewer=viewer: viewer.SliderScroll(value))
            viewer.slider.setValue(0)


    def DisconnectAllSliders(self):

        for viewer in [self.axialViewer, self.coronalViewer, self.sagittalViewer]:
            viewer.slider.valueChanged.disconnect()


    def SwapViewers(self, planeViewer):

        viewers = [self.axialViewer, self.coronalViewer, self.sagittalViewer]
        for viewer in viewers:
            if (viewer.orientation == planeViewer.orientation) and (viewer.uiLocation != planeViewer.uiLocation): viewerToSwapWith = viewer
            
        viewerToSwapWith.SetViewerOrientation(self, planeViewer.pastOrientation)


    def ReadData(self):

        imageReader = vtk.vtkMetaImageReader()
        imageReader.SetFileName("Dataset/out.mhd")
        imageReader.UpdateWholeExtent()
        print(imageReader.GetAnatomicalOrientation())
        range = imageReader.GetOutput().GetScalarRange()

        imageShiftScale = vtk.vtkImageShiftScale()
        imageShiftScale.SetInputConnection(imageReader.GetOutputPort())
        imageShiftScale.SetOutputScalarTypeToUnsignedChar()
        imageShiftScale.SetShift(range[0])
        imageShiftScale.SetScale(255.0/(range[1]-range[0]))
        imageShiftScale.UpdateWholeExtent()

        imageWindowLevel = vtk.vtkImageMapToWindowLevelColors()
        imageWindowLevel.SetInputConnection(imageShiftScale.GetOutputPort())
        imageWindowLevel.SetWindow(100.0)
        imageWindowLevel.SetLevel(50.0)
        imageWindowLevel.UpdateWholeExtent()

        self.imageMapToColors = vtk.vtkImageMapToColors()
        self.imageMapToColors.SetOutputFormatToRGBA()
        self.imageMapToColors.SetInputConnection(imageWindowLevel.GetOutputPort())

        grayscaleLut = vtk.vtkLookupTable()
        grayscaleLut.SetNumberOfTableValues(256)
        grayscaleLut.SetTableRange(0, 255)
        grayscaleLut.SetRampToLinear()
        grayscaleLut.SetHueRange(0, 0)
        grayscaleLut.SetSaturationRange(0, 0)
        grayscaleLut.SetValueRange(0, 1)
        grayscaleLut.SetAlphaRange(1, 1)
        grayscaleLut.Build()
        self.imageMapToColors.SetLookupTable(grayscaleLut)
        self.imageMapToColors.UpdateWholeExtent()


    def HandleEmptyViewer(self):

        self.bottomLeftView_renderer = vtk.vtkRenderer()
        self.bottomLeftView_renderWindowInteractor = QVTKRenderWindowInteractor(self)
        self.bottomLeftView_renderWindowInteractor.GetRenderWindow().AddRenderer(self.bottomLeftView_renderer)

        bottomLeftView_interactorStyle = vtk.vtkInteractorStyleImage()
        self.bottomLeftView_renderWindowInteractor.SetInteractorStyle(bottomLeftView_interactorStyle)
        self.bottomLeftView_iren = self.bottomLeftView_renderWindowInteractor.GetRenderWindow().GetInteractor()

        self.bottomLeftView_gridLayout.insertWidget(0, self.bottomLeftView_renderWindowInteractor)
        self.bottomLeftView_renderWindowInteractor.GetRenderWindow().Render()
        self.bottomLeftView_iren.Initialize()


    def closeEvent(self, QCloseEvent):
    
        super().closeEvent(QCloseEvent)

        self.axialViewer.CloseViewer()
        self.coronalViewer.CloseViewer()
        self.sagittalViewer.CloseViewer()

        self.axialViewer.timer.stop()
        self.coronalViewer.timer.stop()
        self.sagittalViewer.timer.stop()

        # Empty 4th viewer
        self.bottomLeftView_renderWindowInteractor.close()
        
    def maximize_topleft(self):
        self.top_left_widget.showMaximized()
        self.top_right_widget.hide()
        self.bottom_left_widget.hide()
        self.bottom_right_widget.hide()
        self.top_left_minimize_button.setVisible(True)
        self.topleft_maximizebutton.setVisible(False)
        
        
    def maximize_topright(self):
        self.top_right_widget.showMaximized()
        self.top_left_widget.hide()
        self.bottom_left_widget.hide()
        self.bottom_right_widget.hide()
        self.top_right_minimize_button.setVisible(True)
        self.topright_maximizebutton.setVisible(False)
        
    def maximize_bottomleft(self):
        self.bottom_left_widget.showMaximized()
        self.top_left_widget.hide()
        self.top_right_widget.hide()
        self.bottom_right_widget.hide()
        self.bottom_left_minimize_button.setVisible(True)
        self.bottomleft_maximizebutton.setVisible(False)
        
    def maximize_buttomright(self):
        self.bottom_right_widget.showMaximized()
        self.top_left_widget.hide()
        self.top_right_widget.hide()
        self.bottom_left_widget.hide()
        self.bottom_right_minimize_button.setVisible(True)
        self.buttomright_maximizebutton.setVisible(False)
        
    def minimize_topleft(self):
        self.top_left_widget.showMinimized()
        self.top_right_widget.show()
        self.bottom_left_widget.show()
        self.bottom_right_widget.show()
        self.top_left_minimize_button.setVisible(False)
        self.topleft_maximizebutton.setVisible(True)

    def minimize_topright(self):
        self.top_right_widget.showMinimized()
        self.top_left_widget.show()
        self.bottom_left_widget.show()
        self.bottom_right_widget.show()
        self.top_right_minimize_button.setVisible(False)
        self.topright_maximizebutton.setVisible(True)

    def minimize_bottomleft(self):
        self.bottom_left_widget.showMinimized()
        self.top_left_widget.show()
        self.top_right_widget.show()
        self.bottom_right_widget.show()
        self.bottom_left_minimize_button.setVisible(False)
        self.bottomleft_maximizebutton.setVisible(True)

    def minimize_bottomright(self):
        self.bottom_right_widget.showMinimized()
        self.top_left_widget.show()
        self.top_right_widget.show()
        self.bottom_left_widget.show()
        self.bottom_right_minimize_button.setVisible(False)
        self.buttomright_maximizebutton.setVisible(True)

   




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())