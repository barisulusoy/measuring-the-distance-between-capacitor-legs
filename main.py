"""
*******************************************************************************
Barış Ulusoy
2.05.2021-Pazar
baris.ulusy@gmail.com
Elektrik-Elektronik Mühendisi
*******************************************************************************
Kondansatör Bacaklarının Arasındaki Mesafenin Ölçümü (main.py):
- Bu modül içerisinde bulunan kodlar ile kapasitör bacakları arasındaki mesafe
  piksel cinsinden ölçülmektedir. Ölçüm işlemi kapasitör bacaklarının en alt
  noktasından 20 piksel yukarı gelen noktadan ve bacakların orta noktası bulunarak
  hesaplanmıştır.
- Okunan görüntüye sırasıyla BilateralBlur ve Canny yöntemleri uygulanmıştır.
  Daha sonra kenarları bulunan kapasitörün contour alanları tespit edilmiştir.
- Kenarların bulunduğu piksel koordinatları 'coordinatesOfEdges' dizisi içerisinde
  tutulmaktadır.
- 'find_point' metodu ile kapasitörün sol ve sağ bacağındaki istenilen noktaların
  koordinatları bulunmaktadır.
- 'find_distance' metodu ile kapasitör bacakları arasındaki mesafe piksel cinsinden
  hesaplanmaktadır.
*******************************************************************************
"""

import cv2
import numpy as np
import time


class DistanceCalculation:

    def __init__(self):

        ## ==> Görütünün okunması
        self.image = cv2.imread("image_input/IP1_Cap.jpg")

        ## ==> Mesafe'nin tutulduğu attribute'ün tanımlanması
        self.distance = 0

        ## ==> Toplam çalışma zamanının tutulduğu attribute'ün tanımlanması
        self.totalRuntime = 0

        ## ==> Roi sınırlarının belirlenmesi
        self.roiStartX = 0
        self.roiStartY = 480
        self.roiEndX = 1650
        self.roiEndY = 680

    def image_processing(self):
        """
        Görüntü işlemenin yapıldığı metot.
        """

        ## ==> Programın başlangıç zamanının belirlenmesi
        start_time = time.time()

        ## ==> Roi alma işlemi.
        roi = self.image[self.roiStartY:self.roiEndY, self.roiStartX:self.roiEndX]

        ## ==> Bilateral işleminin uygulanması. Bilateral sayesinde kenarlar
        ##     daha belirgin hale getirilebilir.
        bilateralSmoothing = cv2.bilateralFilter (roi, 9,75,75)

        ## ==> Canny kenar bulma yönteminin kullanılarak kenarların bulunması.
        edges = cv2.Canny(bilateralSmoothing, 100, 200)

        ## ==> nonzero() fonksiyonu matris içerisinde bulunan değeri sıfır olmayan indexleri döndürmektedir.
        ##     İlk olarak y ekseni döndürülür.
        ## ==> coordinatesOfEdges[1] => x koordinatları tutulur.
        ## ==> coorcoordinatesOfEdges[0] => y koordinatları tutulur.
        coordinatesOfEdges = np.nonzero(edges)

        ## ==> Contour çıkarma işlemi.
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        ## ==>  Kapasitörün sol ve sağ bacağındaki istenilen noktaların bulunmasını sağlayan metodun çağrılması.
        leftLegPoint, rightLegPoint = self.find_point(contours, coordinatesOfEdges)

        ## ==> Kapasitör bacakları arasındaki mesafenin bulunmasını sağlayan metodun çağrılması.
        self.distance = self.find_distance(leftLegPoint, rightLegPoint)
        print("****************************************************************")
        print("Kapasitör bacakları arasndaki mesafe(piksel):", self.distance)

        ## ==> Kapasitörün bacakları arasındaki orta noktanın bulunması sağlayan metodun çağrılması.
        ##     Orta noktaya yazı yazdırabilmek için orta nokta hesaplanmıştır.
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
        print("Program çalışma süresi(sn):", self.totalRuntime, "saniye")
        print("****************************************************************")

    def find_point(self, _contours, _coordinatesOfEdges):
        """
        Kapasitörün sol ve sağ bacağındaki istenilen noktaların koordinatlarının bulunmasını
        sağlayan metot.
        :param _contours:
        :param _coordinatesOfEdges:
        :return [x_coordinates_left_midpoint, y_coordinates_left_midpoint]:
        """

        ## ==> Bulunan contour alanlarının geometrik merkezlerinin bulunması için gerekli
        ##     metodun çağrılması.
        centroidCoordinates = self.find_centroid(_contours)

        ## ==> Contour sayısının 1 olması durumunda centroidCoordinates dizisi yeniden düzenlenir.
        if len(_contours) == 1:

            ## ==> [[x, y]] => [x, y]
            centroidCoordinates = (centroidCoordinates[0][0], centroidCoordinates[0][1])

        ## ==> 2 adet contour varsa iki adet geometri merkezi olduğu
        ##     anlamına gelir ve bu iki geometri merkezinin orta noktası bulunur.
        elif len(_contours) == 2:

            ## ==> Orta noktanın hesaplandığı metodun çağrılması
            centroidCoordinates = self.find_midpoint(centroidCoordinates[0], centroidCoordinates[1])

        ## ==> Hesaplanan centroid merkezinin x koordinatı baz alınarak kenar koordinatlarının tutulduğu dizi
        ##     sol ve sağ olmak üzere ikiye bölünür. where() metodu sonucunda centroid merkezinin solunda ve sağında
        #      bulunan kenarların koordinatlarının bulunduğu indexler döndürülür.
        indexes_of_x_coordinates_left = np.where(_coordinatesOfEdges[1] < centroidCoordinates[0])[0]
        indexes_of_x_coordinates_right = np.where(_coordinatesOfEdges[1] >= centroidCoordinates[0])[0]

        ## ==> Soldaki Kapasitör Bacağı => [midpoint_x_coordinate_of_left_leg, midpoint_y_coordinate_of_left_leg]
        ###############################

        ## ==> Soldaki koordinatlar içerisindeki y ekseninin maks değeri, sol bacağın y koordinatının maks değerini verir.
        max_y_coordinate_of_left = np.amax(_coordinatesOfEdges[0][indexes_of_x_coordinates_left])

        ## ==> Sol kapasitör bacağının y eksenindeki istenilen orta nokta koordinatının bulunması
        midpoint_y_coordinate_of_left_leg = max_y_coordinate_of_left - 20

        ## ==> Sol kapasitör bacağının y eksenindeki istenilen orta nokta koordinatındaki x indexlerinin bulunması.
        ##     Toplam 4 adet nokta bulunur [x1 x2 x3 x4]. Bu noktalardan iki tanesi sol bacağa, iki tanesi ise sağ
        ##     bacağa düşmektedir.
        x_indexes_of_midpoint_y_coordinate_of_left_leg = np.where(_coordinatesOfEdges[0] ==
                                                                  midpoint_y_coordinate_of_left_leg)[0]

        ## ==> Soldaki kapasitör bacağının, istenilen y koordinatında bulunan x koordinatlarının tutulduğu dizi.
        ##     Sol bacağa düşen koordinatların x ekseni tutulur x_coord_left => [x1 x2].
        x_coord_left = []

        ## ==> Bulunan x koordinatların döngüye sokulması:
        for i in range(len(x_indexes_of_midpoint_y_coordinate_of_left_leg)):

            ## ==> Sol bacağa gelen x koordinatlarının bulunarak x_coord_left dizisine atanması
            if _coordinatesOfEdges[1][x_indexes_of_midpoint_y_coordinate_of_left_leg[i]] < centroidCoordinates[0]:
                x_coord_left.append(_coordinatesOfEdges[1][x_indexes_of_midpoint_y_coordinate_of_left_leg[i]])

        ## ==> Sol kapasitör bacağının x eksenindeki istenilen orta nokta koordinatının bulunması
        midpoint_x_coordinate_of_left_leg = int((x_coord_left[0] + x_coord_left[1])/2)

        ## ==> Sağdaki Kapasitör Bacağı => [midpoint_x_coordinate_of_right_leg, midpoint_y_coordinate_of_right_leg]
        ###############################

        ## ==> Sağdaki koordinatlar içerisindeki y ekseninin maks değeri sağ bacağın y koordinatının maks değerini verir.
        max_y_coordinate_of_right = np.amax(_coordinatesOfEdges[0][indexes_of_x_coordinates_right])

        ## ==> Sağ kapasitör bacağının y eksenindeki istenilen orta nokta koordinatının bulunması
        midpoint_y_coordinate_of_right_leg = max_y_coordinate_of_right - 20

        ## ==> Sağ kapasitör bacağının y eksenindeki istenilen orta nokta koordinatınındaki x indexlerinin bulunması
        ##     Toplam 4 adet nokta bulunur [x1 x2 x3 x4]. Bu noktalardan iki tanesi sol bacağa, iki tanesi ise sağ
        ##     bacağa düşmektedir.
        x_indexes_of_midpoint_y_coordinate_of_right_leg = np.where(_coordinatesOfEdges[0] ==
                                                                  midpoint_y_coordinate_of_right_leg)[0]

        ## ==> Sağdaki kapasitör bacağının, istenilen y koordinatında bulunan x koordinatlarının tutulduğu dizi.
        ##     Sol bacağa düşen koordinatların x ekseni tutulur x_coord_left => [x1 x2].
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

        ## Geometri merkezlerinin tutulduğu dizinin oluşturulması.
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
        İki noktası bilinen doğru parçasının orta noktasının hesaplandığı metod.
        :param _point1:
        :param _point2:
        :return midpointCoordinates:
        """

        ## ==> Orta noktanın bulunması
        midpointCoordinates = (int((_point1[0] + _point2[0]) * 0.5), int((_point1[1] + _point2[1]) * 0.5))

        return midpointCoordinates

    def find_distance(self, _point1, _point2):
        """
        İki nokta arasındaki mesafenin hipotenüs teoremi ile bulunduğu metot.
        :param _point1:
        :param _point2:
        :return result:
        """
        dx = _point2[0] - _point1[0]
        dy = _point2[1] - _point1[1]
        dsquared = dx ** 2 + dy ** 2
        result = dsquared ** 0.5
        return result




