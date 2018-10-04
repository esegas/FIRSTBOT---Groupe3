# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 10:41:19 2018

@author: moton
"""
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import cv2
import numpy as np
import ui_sliders as IHM
from functools import partial

class MainInterfaceConfig(QtWidgets.QMainWindow, IHM.Ui_MainWindow):
    """
    Dessine l'interface graphique
    """
    def __init__(self):
        super(MainInterfaceConfig, self).__init__()
        self.setupUi(self)
        self.test = True
        self.nb_color = 2
        self.tab_color = [None]* self.nb_color
        self.show()
        self.cap = cv2.VideoCapture(0)
        self.initialisation()

    def maj_value(self, upper, lower):
        self.hs_b_min.setValue(lower[0])
        self.hs_v_min.setValue(lower[1])
        self.hs_r_min.setValue(lower[2])
        self.hs_b_max.setValue(upper[0])
        self.hs_v_max.setValue(upper[1])
        self.hs_r_max.setValue(upper[2])
    
    def get_value(self):
        upper = np.array([self.hs_b_max.value(), self.hs_v_max.value(),self.hs_r_max.value()])
        lower = np.array([self.hs_b_min.value(), self.hs_v_min.value(),self.hs_r_min.value()])
        self.tab_color[self.not_pick - 1] = [upper, lower]
        
        print("test upper lower")
        print(upper)
        print(lower)
        self.image_mask = cv2.inRange(self.frame,self.tab_color[self.not_pick - 1][1],self.tab_color[self.not_pick - 1][0])
        cv2.imshow('nb', np.array(self.image_mask))
    
    def fermer(self):
        self.not_pick += 1
        if (self.not_pick > self.nb_color):
            self.hide()

    def initialisation(self):
        # Recupere l'image

        self.test_mask = []
        self.seuil_min = 10
        self.seuil_max = 10
        self.not_pick = 0
        self.image_mask = []
        self.grid_matrix = []

        def pick_color(event,x,y,flags,param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if self.not_pick < self.nb_color:
                    pixel = self.frame[y-10:y+10,x-10:x+10]
                    #you might want to adjust the ranges(+-10, etc):
                    upper =  np.array([np.mean(pixel[0,:,0]) + self.seuil_max, np.mean(pixel[0,:,1]) + self.seuil_max,np.mean(pixel[0,:,2]) + self.seuil_max])
                    lower =  np.array([np.mean(pixel[0,:,0]) - self.seuil_min, np.mean(pixel[0,:,1]) - self.seuil_min,np.mean(pixel[0,:,2]) - self.seuil_min])

                    self.maj_value(upper, lower)

                    self.pb_submit.clicked.connect(self.get_value)
                    self.pb_enter.clicked.connect(self.fermer)

#                        upper, lower = self.get_value()
                    

#                    self.not_pick += 1

        while(True):
            ret, self.frame = self.cap.read()
            cv2.imshow('frame', np.array(self.frame))

            if (self.not_pick < self.nb_color):
                cv2.setMouseCallback('frame', pick_color)
            else:
                self.traitement()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def traitement(self):
        def select_indexes(tab):
            indexes = [x for x in range(0,len(tab)) if tab[x] == max(tab)]     
            return indexes
        
        def find_center(tab):
            return np.mean(np.array(tab)*64+32)
        
        while(True):
            # Capture frame-by-frame
            ret, self.frame = self.cap.read()
            #    edges = cv2.Canny(frame,100,200)
        
            image_mask = cv2.inRange(self.frame, self.tab_color[0][1], self.tab_color[0][0])
            cv2.imshow("mask",image_mask)

            def color_grid( grid):
                for y in range(0,432,48):
                    for x in range(0,576,64): 
                        grid.append(np.mean(image_mask[y:y+47,x:x+63]))
                grid_matrix = np.array(grid).reshape(9,9)
                return grid_matrix
            
            def convert(coord, angleCam, heightCam):
                oc = np.tan(angleCam+45)*heightCam
                ob = np.tan(angleCam)*heightCam
                pixelRatio = (oc-ob)/480
                y = coord[1]*pixelRatio+ob
                pixelAngle = 60/640
                x = np.tan(coord[0]*pixelAngle)*y

            grid = []
            grid_matrix = color_grid(grid)
        #color_lines = [x for x in range(0,len(grid_matrix[8])) if grid_matrix[8][x] == max(grid_matrix[8])]
#        color_lines = list(map(select_indexes,grid_matrix))
#        positions = list(map(find_center,color_lines))
#        print(positions)
            color_center = select_indexes(grid_matrix[4])
            x = find_center(color_center)
            vector = (x-320, 240)
            print(vector)
            #   test_mask = [np.mean(frame[])]
            # Display the resulting frame
            cv2.imshow('frame', np.array(self.frame[245:397, 165:317])) #edges)
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()
    
    # Faire une liste de boundaries pour chaque parcours
    
    # Parcourir chaque parcours jusqu'au signal de fin


        
    def closeEvent(self, event):
        """
        ajoute une boite de dialogue pour confirmation de fermeture
        """
        result = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit...",
                                                ("Are you sure you want "
                                                 "to exit ?"),
                                                (QtWidgets.QMessageBox.Yes |
                                                 QtWidgets.QMessageBox.No),
                                                QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            # permet d'ajouter du code pour fermer proprement
            event.accept()

        else:
            event.ignore()
if __name__ == '__main__':
    APP = QtWidgets.QApplication(sys.argv)
    MON_IHM = MainInterfaceConfig()
    sys.exit(APP.exec_())
        
