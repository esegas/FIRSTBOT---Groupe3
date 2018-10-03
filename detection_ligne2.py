# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 10:41:19 2018

@author: moton
"""
import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import cv2
import ui_sliders as IHM


class MainInterfaceConfig(QtWidgets.QMainWindow, IHM.Ui_MainWindow):
    """
    Dessine l'interface graphique
    """
    def __init__(self):
        super(MainInterfaceConfig, self).__init__()
        self.setupUi(self)
        self.show()
        self.pb_submit.clicked.connect(self.maj_affichage)
        self.pb_enter.clicked.connect(self.fermer)

    def bouton_trait(self):
        """
        Bouton permettant de lancer le calcul des régions d'intéret.
        """
        self.recalcul_roy()

    def maj_affichage():
        pass
    
    def fermer():
        self.maj_affiche()
        
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
        
# Recupere l'image

cap = cv2.VideoCapture(1)

test_blue = [255, 0, 0]
test_green = [0, 255, 0]
test_red = [0, 0, 255]

test_mask = []
seuil_min = 10
seuil_max = 10
not_pick = 0
nb_color = 2
tab_color = []
image_mask = []
grid_matrix = []

def color_grid(grid):
    for y in range(0,432,48):
        for x in range(0,576,64): 
            grid.append(np.mean(image_mask[y:y+47,x:x+63]))
    grid_matrix = np.array(grid).reshape(9,9)
    return grid_matrix
    
def pick_color(event,x,y,flags,param):
    global not_pick
    global image_mask
    global grid_matrix
    global tab_color
    if event == cv2.EVENT_LBUTTONDOWN:
        if not_pick < nb_color:
            pixel = frame[y-10:y+10,x-10:x+10]

            #you might want to adjust the ranges(+-10, etc):
            upper =  np.array([np.mean(pixel[0,:,0]) + seuil_max, np.mean(pixel[0,:,1]) + seuil_max,np.mean(pixel[0,:,2]) + seuil_max])
            lower =  np.array([np.mean(pixel[0,:,0]) - seuil_min, np.mean(pixel[0,:,1]) - seuil_min,np.mean(pixel[0,:,2]) - seuil_min])
            print(tab_color)
            tab_color.append([upper, lower])
            print(tab_color)
            not_pick += 1
            
    
            
    
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
#    edges = cv2.Canny(frame,100,200)
    
    if not_pick < nb_color:
        cv2.imshow('frame', np.array(frame))
        cv2.setMouseCallback('frame', pick_color)
        #print(tab_color)        
    else:
        print(tab_color[0][0][0], tab_color[0][1][0])
        image_mask = cv2.inRange(frame,tab_color[0][1],tab_color[0][0])
        cv2.imshow("mask",image_mask)
        
        grid = []
        grid_matrix = color_grid(grid)
        print(grid_matrix)
        color_lines = [x for x in range(0,len(grid_matrix[8])) if grid_matrix[8][x] == max(grid_matrix[8])]
        print(enumerate(grid_matrix[8]))
        print(color_lines)
        # Our operations on the frame come here
        #    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#        im_crop_1 = np.array(cv2.inRange(frame[245:295, 165:215]))
#        im_crop_2 = np.array(frame[296:346, 165:215])
#        im_crop_3 = np.array(frame[347:397, 165:215])
#        im_crop_4 = np.array(frame[245:295, 216:266])
#        im_crop_5 = np.array(frame[296:346, 216:266])
#        im_crop_6 = np.array(frame[347:397, 216:266])
#        im_crop_7 = np.array(frame[245:295, 267:317])
#        im_crop_8 = np.array(frame[296:346, 267:317])
#        im_crop_9 = np.array(frame[347:397, 267:317])
        
        #for bleu, vert, rouge in tab_color[0]
        
#        means = []
#        for im_crop in [im_crop_1, im_crop_2, im_crop_3, im_crop_4, im_crop_5, im_crop_6, im_crop_7, im_crop_8, im_crop_9]:
#            blue_mean = np.mean(im_crop[:, :, 0])
#            green_mean = np.mean(im_crop[:, :, 1])
#            red_mean = np.mean(im_crop[:, :, 2])
#
#        means.append([blue_mean, green_mean, red_mean])
    
        red_nb = 0
        green_nb = 0
        blue_nb = 0
#        for mean in means:
#            if mean[0] > seuil_max and mean[1] < seuil_min and mean[2] < seuil_min:
#                blue_nb += 1
#            if mean[0] < seuil_min and mean[1] > seuil_max and mean[2] < seuil_min:
#                green_nb += 1
#            if mean[0] < seuil_min and mean[1] < seuil_min and mean[2] > seuil_max:
#                red_nb += 1

        #   test_mask = [np.mean(frame[])]
        # Display the resulting frame
        cv2.imshow('frame', np.array(frame[245:397, 165:317])) #edges)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# Faire une liste de boundaries pour chaque parcours

# Parcourir chaque parcours jusqu'au signal de fin


