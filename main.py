"""
****************************************************************************
Barış Ulusoy
1.05.2021
baris.ulusy@gmail.com
****************************************************************************
Kondansatör Bacaklarının Arasındaki Mesafenin Ölçümü
(Measuring the Distance Between Capacitor Legs):
****************************************************************************
"""

import cv2
import numpy as np
import time


class DistanceCalculation:


    def __init__(self):

        ## ==> Görütünün okunması
        self.image = cv2.imread("image_input/IP1_Cap.jpg")

        ## ==> İkici kez görüntü okuma
        self.cont = False
        self.path = ""

        ## ==> Mesafe'nin tutulduğu değişkenin tanımlanması
        self.distance = 0

        ## ==> Toplam çalışma zamanının tutulduğu değişkenin tanımlanması
        self.totalRuntime = 0

        ## ==> Roi sınırlarının belirlenmesi
        self.roiStartX = 0
        self.roiStartY = 480
        self.roiEndX = 1650
        self.roiEndY = 680

    def image_processing(self):
        """
        Görüntü işlemenin yapıldığı metot.
        :return image:
        """

        ## ==> Programın başlangıç zamanının belirlenmesi
        start_time = time.time()

        ## ==> Roi alma işlemi.
        roi = self.image[self.roiStartY:self.roiEndY, self.roiStartX:self.roiEndX]

        ## ==> Yumuşatma işleminin uygulanması. Yumuşatma sayesinde kenarlar
        ##     daha belirgin hale getirilebilir.
        gaussSmoothing = cv2.GaussianBlur(roi, (7, 7), 0)

        ## ==> Canny kenar bulma yönteminin kullanılarak kenarların bulunması.
        edges = cv2.Canny(gaussSmoothing, 100, 200)
        cv2.imshow("edges", edges)

        ## ==> nonzero() fonksiyonu matris içerisinde bulunan değeri sıfır olmayan indexleri döndürmektedir.
        ##     İlk olarak y ekseni döndürülür.
        ## ==> coordinatesOfEdges[1] => x koordinatları tutulur.
        ## ==> coorcoordinatesOfEdges[0] => y koordinatları tutulur.
        coordinatesOfEdges = np.nonzero(edges)

        ## ==> Contour bulma işlemi.
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        ## ==>  Kapasitörün sol ve sağ bacağındaki istenilen noktaların bulunduğu methodun çağrılması.
        leftLegPoint, rightLegPoint = self.find_point(contours, coordinatesOfEdges)

        ## ==> Kapasitör bacakları arasındaki mesafenin bulunduğu metodun çağrılması
        self.distance = self.find_distance(leftLegPoint, rightLegPoint)
        print("Kapasitör bacakları arasndaki mesafe(piksel):", self.distance)

        ## ==> Kapasitörün bacakları arasındaki orta noktanın bulunması. Orta noktaya yazı yazdırabilmek için hesaplandı.
        midpoint_between_capacitor_legs = self.find_midpoint(leftLegPoint, rightLegPoint)

        ## ==> İstenilen koordinatara gerekli şekillerin çizilmesi.
        cv2.circle(roi, (leftLegPoint[0], leftLegPoint[1]), radius=4, color=(0, 0, 255), thickness=-1)
        cv2.circle(roi, (rightLegPoint[0], rightLegPoint[1]), radius=4, color=(0, 0, 255), thickness=-1)
        cv2.line(roi, (leftLegPoint[0], leftLegPoint[1]), (rightLegPoint[0], rightLegPoint[1]), (0, 255, 0), 2)
        cv2.putText(roi, "distance="+str(self.distance), (midpoint_between_capacitor_legs[0]-170,
                    midpoint_between_capacitor_legs[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
        cv2.line(self.image, (0,480), (1650, 480), (255, 0, 0), 2)
        cv2.line(self.image, (0, 680), (1650, 680), (255, 0, 0), 2)

        ## ==> Alınan roi'nin yeniden görüntü üzerine yapıştırılması
        self.image[self.roiStartY:self.roiEndY, self.roiStartX:self.roiEndX] = roi

        ## ==> Programın bitiş zamanının belirlenmesi
        end_time = time.time()

        ## ==> Toplam çalışma zamanının belirlenmesi
        self.totalRuntime = end_time - start_time

        ## ==> Programın çalışma süresinin terminal'e bastırılması
        print("Program çalışma süresi(sn):", self.totalRuntime, "saniye")

        ## ==> İşlenmiş görüntünün ekranda gösterilmesi
        cv2.imshow("image", self.image)

    def find_point(self, _contours, _coordinatesOfEdges):
        """
        İstenilen nokta koordinatların hesaplandığı method.
        :param _contours:
        :param _coordinatesOfEdges:
        :return [x_coordinates_left_midpoint, y_coordinates_left_midpoint]:
        :return [x_coordinates_right_midpoint, y_coordinates_right_midpoint]:
        """

        ## ==> Bulunan contour alanlarının geometrik merkezlerinin bulunması için gerekli
        ##     metodun çağrılması.
        centroidCoordinates = self.find_centroid(_contours)

        ## ==> Contour sayısının 1 olması durumunda centroidCoordinates dizisi yeniden düzenlenir.
        if len(_contours) == 1:

            ## ==> [[x, y]] => [x, y]
            centroidCoordinates = (centroidCoordinates[0][0], centroidCoordinates[0][1])

        ## ==> 2 adet contour varsa iki adet geometri merkezi olduğu
        ##     anlamına gelir bu iki geometri merkezinin orta noktası bulunur.
        elif len(_contours) == 2:

            ## ==> Orta noktanın hesaplandığı metodun çağrılması
            centroidCoordinates = self.find_midpoint(centroidCoordinates[0], centroidCoordinates[1])

        ## ==> Hesaplanan centroid merkezinin x koordinatı baz alınarak kenar koordinatlarının tutulduğu dizi
        ##     sol ve sağ olmak üzere ikiye bölünür. where() metodu sonucunda centroid merkezinin solunda ve sağında
        #      bulunan kenarların koordinatlarının bulunduğu indexler döndürülür.
        indexes_of_x_coordinates_left = np.where(_coordinatesOfEdges[1] < centroidCoordinates[0])[0]
        indexes_of_x_coordinates_right = np.where(_coordinatesOfEdges[1] >= centroidCoordinates[0])[0]

        ## ==> Soldaki Kapasitör Bacağı
        ###############################

        ## ==> Soldaki koordinatlar içerisindeki y ekseninin maks değeri sol bacağın y koordinatının maks değerini verir.
        max_y_coordinate_of_left = np.amax(_coordinatesOfEdges[0][indexes_of_x_coordinates_left])

        ## ==> Sol kapasitör bacağının y eksenindeki istenilen orta nokta koordinatının bulunması
        midpoint_y_coordinate_of_left_leg = max_y_coordinate_of_left - 20

        ## ==> Sol kapasitör bacağının y eksenindeki istenilen orta nokta koordinatınındaki x indexlerinin bulunması
        x_indexes_of_midpoint_y_coordinate_of_left_leg = np.where(_coordinatesOfEdges[0] ==
                                                                  midpoint_y_coordinate_of_left_leg)[0]

        ## ==> Soldaki kapasitör bacağının, istenilen y koordinatında bulunan x koordinatlarının tutulduğu dizi
        x_coord_left = []

        ## ==> Bulunan x koordinatların döngüye sokulması:
        for i in range(len(x_indexes_of_midpoint_y_coordinate_of_left_leg)):

            ## ==> Sol bacağa gelen x koordinatlarının bulunarak x_coord_left dizisine atanması
            if _coordinatesOfEdges[1][x_indexes_of_midpoint_y_coordinate_of_left_leg[i]] < centroidCoordinates[0]:
                x_coord_left.append(_coordinatesOfEdges[1][x_indexes_of_midpoint_y_coordinate_of_left_leg[i]])

        ## ==> Sol kapasitör bacağının x eksenindeki istenilen orta nokta koordinatının bulunması
        midpoint_x_coordinate_of_left_leg = int((x_coord_left[0] + x_coord_left[1])/2)

        ## ==> Sağdaki Kapasitör Bacağı
        ###############################

        ## ==> Sağdaki koordinatlar içerisindeki y ekseninin maks değeri sağ bacağın y koordinatının maks değerini verir.
        max_y_coordinate_of_right = np.amax(_coordinatesOfEdges[0][indexes_of_x_coordinates_right])

        ## ==> Sağ kapasitör bacağının y eksenindeki istenilen orta nokta koordinatının bulunması
        midpoint_y_coordinate_of_right_leg = max_y_coordinate_of_right - 20

        ## ==> Sağ kapasitör bacağının y eksenindeki istenilen orta nokta koordinatınındaki x indexlerinin bulunması
        x_indexes_of_midpoint_y_coordinate_of_right_leg = np.where(_coordinatesOfEdges[0] ==
                                                                  midpoint_y_coordinate_of_right_leg)[0]

        ## ==> Sağdaki kapasitör bacağının, istenilen y koordinatında bulunan x koordinatlarının tutulduğu dizi
        x_coord_right = []

        ## ==> Bulunan x koordinatların döngüye sokulması:
        for i in range(len(x_indexes_of_midpoint_y_coordinate_of_right_leg)):

            ## ==> Sağ bacağa gelen x koordinatlarının bulunarak x_coord_left dizisine atanması
            if _coordinatesOfEdges[1][x_indexes_of_midpoint_y_coordinate_of_right_leg[i]] >= centroidCoordinates[0]:
                x_coord_right.append(_coordinatesOfEdges[1][x_indexes_of_midpoint_y_coordinate_of_right_leg[i]])

        ## ==> Sağ kapasitör bacağının x eksenindeki istenilen orta nokta koordinatının bulunması
        midpoint_x_coordinate_of_right_leg = int((x_coord_right[0] + x_coord_right[1]) / 2)

        return [midpoint_x_coordinate_of_left_leg, midpoint_y_coordinate_of_left_leg], \
                            [midpoint_x_coordinate_of_right_leg, midpoint_y_coordinate_of_right_leg]

    def find_centroid(self, _contours):
        """
        Geometri merkezinin bulunduğu metot.
        :param _contours:
        :return centroidCoordinates:
        """

        ## Geometri merkezlerinin tutulduğu dizinin oluşturulması
        centroidCoordinates = []

        for (i, cnt) in enumerate(_contours):

            ## ==> moments() fonksiyonu tespit edilen contour'un momentlerini hesaplar.
            cent_moment = cv2.moments(cnt)

            ## ==> Geometri merkezinin koordinatlarının bulunması.
            centroid_x = int(cent_moment['m10'] / cent_moment['m00'])
            centroid_y = int(cent_moment['m01'] / cent_moment['m00'])
            centroidCoordinates.append([centroid_x,centroid_y])

        return centroidCoordinates

    def find_midpoint(self, _point1, _point2):
        """
        İki noktası bilinen doğrunun orta noktasının hesaplandığı metod.
        :param _point1:
        :param _point2:
        :return midpointCoordinates:
        """

        ## ==> Orta noktanın bulunması
        midpointCoordinates = (int((_point1[0] + _point2[0]) * 0.5), int((_point1[1] + _point2[1]) * 0.5))

        return midpointCoordinates

    def find_distance(self, _point1, _point2):
        """
        İki nokta arasındaki mesafenin bulunduğu metot.
        :param _point1:
        :param _point2:
        :return result:
        """
        dx = _point2[0] - _point1[0]
        dy = _point2[1] - _point1[1]
        dsquared = dx ** 2 + dy ** 2
        result = dsquared ** 0.5
        return result




