from main import DistanceCalculation
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from PIL.ImageTk import PhotoImage
from PIL.Image import fromarray
import cv2
import numpy as np

class UserInterface(DistanceCalculation):
    """
    Kullanıcı arayüzünün oluşturulması.
    """

    def __init__(self):

        super().__init__()
        ## ==> Kullanıcı arayüzü üzerine frame eklemek için kullanılan label'ın
        ##     ilk değerinin attribute olarak tanımlanması
        self.panel_frameImshow = None
        self.cont = True
        self.create_window()


    def create_window(self):
        """
        Kullanıcı penceresinin oluşturulduğu metot.
        :return:
        """

        ## ==> Ana pencerenin oluşturulması
        self.window = tk.Tk()
        self.window.geometry("1300x650+1+1")
        self.window.title("Measuring the Distance Between Capacitor Legs")
        self.window.configure(bg='white')

        start_button = tk.Button(self.window, padx=4, pady=2, bd=4,
                                    fg="black", width=10,
                                    font=('arial', 15, 'bold'), text="Start",
                                    bg="green", command=self.start).place(x=920, y=150)


        load_button = tk.Button(self.window, padx=4, pady=2, bd=4,
                                fg="black", width=10,
                                font=('arial', 15, 'bold'), text="Load Image",
                                bg="green", command=self.selectImageFile).place(x=1120, y=150)

        distance_label = tk.Label(self.window,
                              text="Distance (Pixel):",
                              bg="white", font=('arial', 15, 'bold'))
        distance_label.place(x=900, y=250)

        self.distance_info_label = tk.Label(self.window,
                                       width=20, height=2,
                                       bg="powder blue", font=('arial', 20, 'bold'), anchor="w")
        self.distance_info_label.place(x=900, y=290)

        runtime_label = tk.Label(self.window,
                                  text="Runtime (Second):",
                                  bg="white", font=('arial', 15, 'bold'))
        runtime_label.place(x=900, y=390)

        self.runTime_info_label = tk.Label(self.window,
                                       width=20, height=2,
                                       bg="powder blue", font=('arial', 20, 'bold'), anchor="w")
        self.runTime_info_label.place(x=900, y=430)

        self.showImageInUserMenu()

        ## ==> Arayüze logonun eklenmesi
        logo = ImageTk.PhotoImage(Image.open("barisulusoy_logo.png"))
        tk.Label(self.window, image=logo).place(x=1005, y=540)

        ## ==> Kullanıcı arayüzü kapatıncaya kadar arayüzün ekranda kalmasını sağlayan fonksiyon
        self.window.mainloop()

    def start(self):
        """
        Görüntü işlemeyi başlatacak method.
        :return:
        """
        if self.cont:
            self.image_processing()
            self.distance_info_label.config(text=str(self.distance))
            self.runTime_info_label.config(text=str(self.totalRuntime))
            self.cont = False
            self.showImageInUserMenu()

        else:
            messagebox.showerror(title="Error", message="Ölçüm işlemi tamamlandı. Yeniden işlem yapmak için ,"
                                                        "Görüntü Yükle butonuna basınız.")

    def selectImageFile(self):
        """
        Resim kaynağını belirlemek için klasörden dosya seçme işlemini sağlayan
        metot.
        """

        takeFile = filedialog.askopenfilename(title="Dosya Seçiniz")

        if takeFile:

            self.cont = True

            ## => Resim yolunun belirlenmesi:
            self.path = takeFile
            self.image = cv2.imread(str(self.path))
            self.showImageInUserMenu()

    def showImageInUserMenu(self):
        """
        Alınan framelerin arayüz üzerinde gösterilmesini sağlayan method.
        """

        img = cv2.resize(self.image, (850, 610))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = fromarray(img)
        img = PhotoImage(img)



        ## ==> Program ilk çalıştığı anda frame değeri 0'a eşit olduğu için hatayı
        ##     engellemek için oluşturulan if-else yapısı:

        ## ==> Framelerin gösterileceği panel oluşturulmamış ise panel oluşturma
        ##     işlemi gerçekleştirilir:
        if self.panel_frameImshow is None:
            self.panel_frameImshow = tk.Label(self.window, image=img)
            self.panel_frameImshow.image = img
            self.panel_frameImshow.place(x=10, y= 10)

        ## ==> Panel oluşturulmuş ise anlık olarak alınan frame'ler panele eklenir:
        else:
            self.panel_frameImshow.configure(image=img)
            self.panel_frameImshow.image = img
