"""
*******************************************************************************
Barış Ulusoy
2.05.2021-Pazar
baris.ulusy@gmail.com
Elektrik-Elektronik Mühendisi
*******************************************************************************
Kondansatör Bacaklarının Arasındaki Mesafenin Ölçümü (ui.py):
- Bu modülde bir kullanıcı arayüzü oluşturulmuştur. Bu arayüz sayesinde
  görüntüleri test etmek için programı sürekli çalıştırıp durdurmamıza gerek
  kalmamıştır.
- Arayüz, python içerisinde bulunan tkinter kütüphanesi ile oluşturulmuştur.
*******************************************************************************
"""

from main import DistanceCalculation
from PIL.ImageTk import PhotoImage
from PIL.Image import fromarray
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
import tkinter as tk
import cv2


class UserInterface(DistanceCalculation):
    """
    Kullanıcı arayüzünün oluşturulduğu sınıf.
    """

    def __init__(self):

        ## ==> 'DistanceCalculation' sınıfında bulunan attribute'lerin inheritance edilmesi.
        super().__init__()

        ## ==> Kullanıcı arayüzü üzerine görüntü eklemek için kullanılan label'ın
        ##     ilk değerinin tanımlanması.
        self.panel_frameImshow = None

        ## ==> Yeni görüntünün okunup okunmadığına karar verecek attribute
        self.isReadNewImage = True

        ## ==> Arayüzün oluşturulduğu metodun çağrılması.
        self.create_window()


    def create_window(self):
        """
        Kullanıcı penceresinin oluşturulduğu metot.
        """

        ## ==> Ana pencerenin oluşturulması
        self.window = tk.Tk()
        self.window.geometry("1300x650+1+1")
        self.window.title("Measuring the Distance Between Capacitor Legs")
        self.window.configure(bg='white')

        ## ==> Görüntü işlemeyi başlatacak butonun oluşturulması.
        start_button = tk.Button(self.window, padx=4, pady=2, bd=4, fg="black", width=12,
                                    font=('arial', 15, 'bold'), text="Start",
                                    bg="green", command=self.start_image_processing).place(x=900, y=130)

        ## ==> Sisteme yeni görüntü eklenmesini sağlayan butonun oluşturulması.
        load_button = tk.Button(self.window, padx=4, pady=2, bd=4, fg="black", width=12,
                                font=('arial', 15, 'bold'), text="Upload Image",
                                bg="green", command=self.upload_image).place(x=1100, y=130)

        ## ==> Mesafe bilgisinin yazdırılacağı labelın oluşturulması.
        distance_label = tk.Label(self.window, text="Distance (Pixel):", bg="white",
                                                                font=('arial', 15, 'bold'))
        distance_label.place(x=900, y=240)
        self.distance_info_label = tk.Label(self.window, width=21, height=2, bg="powder blue",
                                                font=('arial', 20, 'bold'), anchor="w")
        self.distance_info_label.place(x=900, y=280)

        ## ==> Programın çalışma zamanının yazdırıldığı labelın oluşturulması.
        runtime_label = tk.Label(self.window, text="Runtime (Second):", bg="white",
                                                                font=('arial', 15, 'bold'))
        runtime_label.place(x=900, y=380)
        self.runTime_info_label = tk.Label(self.window, width=21, height=2, bg="powder blue",
                                                        font=('arial', 20, 'bold'), anchor="w")
        self.runTime_info_label.place(x=900, y=420)

        ## ==> Arayüze logonun eklenmesi
        logo = ImageTk.PhotoImage(Image.open("barisulusoy_logo.png"))
        tk.Label(self.window, image=logo).place(x=1005, y=540)

        ## ==> Kullanıcı arayüzünde okunan görüntünün gösterilmesini sağlayan metodun çağrılması.
        ##     Program açılır açılmaz işlenmemiş görüntü arayüz üzerinde gösterilir.
        self.showImageInUserMenu()

        ## ==> Kullanıcı arayüzü kapatıncaya kadar arayüzün ekranda kalmasını sağlayan fonksiyon
        self.window.mainloop()

    def start_image_processing(self):
        """
        Görüntü işlemeyi başlatacak method.
        :return:
        """

        ## ==> Yeni görüntü okunmuş ise görüntü işleme başlatılır.
        if self.isReadNewImage:

            ## ==> Görüntü işlemenin yapıldığı metod çağrılır (main.py içerisinde bulunuyor).
            self.image_processing()

            ## ==> Arayüz üzerinde kapasitör bacakları arasındaki mesafe bilgisi gösterilir.
            self.distance_info_label.config(text=str(self.distance))

            ## ==> Arayüz üzerinde programın toplam çalışma süresi gösterilir.
            self.runTime_info_label.config(text=str(self.totalRuntime))

            ## ==> İşlenmiş görüntünün yeniden işlenmemesi için 'isReadNewImage' değişkenine
                   ## False değeri atanır.
            self.isReadNewImage = False

            ## ==> İşlenmiş görüntünün ekranda gösterilmesi için gerekli metodun çağrılması.
            self.showImageInUserMenu()

        ## ==> Kullanıcı işlenmiş görüntüyü yeniden işlemeye çalışırsa ekranda hata mesajı gösterilir.
        else:
            messagebox.showerror(title="Error", message="The measurement process is complete. To make a new operation, "
                                                        "add an image with the 'Upload Image' button.")

    def upload_image(self):
        """
        Test için yeni görüntünün klasörden seçilmesini sağlayan metot.
        """

        ## ==> İşlenecxek görüntünün dosya üzerinden seçilmesi.
        filePath = filedialog.askopenfilename(title="Select Image")

        ## ==> Dosya seçilmiş ise:
        if filePath:

            ## ==> Sisteme işlenecek yeni görüntü verildiği için 'isReadNewImage' değişkenine True değeri atanır.
            self.isReadNewImage = True

            ## ==> Eklenen yeni görüntünün okunması.
            self.image = cv2.imread(str(filePath))

            ## ==> Okunan yeni görüntünün arayüz üzerinde gösterilmesi
            self.showImageInUserMenu()

    def showImageInUserMenu(self):
        """
        Okunan görüntülerin arayüz üzerinde gösterilmesini sağlayan metot.
        """

        ## ==> Okunan görüntünün arayüz üzerinde gösterilebilecek şekile getirilmesi.
        img = cv2.resize(self.image, (850, 610))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = fromarray(img)
        img = PhotoImage(img)

        ## ==> Görüntülerin gösterileceği panel oluşturulmamış ise panel oluşturma işlemi gerçekleştirilir:
        if self.panel_frameImshow is None:
            self.panel_frameImshow = tk.Label(self.window, image=img)
            self.panel_frameImshow.image = img
            self.panel_frameImshow.place(x=10, y= 10)

        ## ==> Panel oluşturulmuş ise okunan görüntüler panel üzerinde gösterilir.
        else:
            self.panel_frameImshow.configure(image=img)
            self.panel_frameImshow.image = img
