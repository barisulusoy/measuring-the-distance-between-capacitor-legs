"""
*******************************************************************************
Barış Ulusoy
2.05.2021-Pazar
baris.ulusy@gmail.com
Elektrik-Elektronik Mühendisi
*******************************************************************************
Kondansatör Bacaklarının Arasındaki Mesafenin Ölçümü (start.py):
- Bu modül ile tüm program başlatılmaktadır.
- Kodların bulunduğu dosya yolu üzerinde bir Komut Satırı (cmd) açılıp, aşağıdaki
  kod satırı yazılarak program başlatılabilir;
  => python start.py
- Eksik kütüphaneniz bulunuyor ise sistem hata verecektir. Eksik kütüphanenizi
  'pip install kütüphane_ismi' kod satırı ile yükleyebilirsiniz.
*******************************************************************************
"""

from ui import UserInterface


if __name__ == '__main__':

    ## ==> Kullanıcı arayüzünün oluşturulduğu sınıfın çağrılması.
    UserInterface()

