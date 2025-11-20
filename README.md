# 🚗 Sürücü Yorgunluk Tespit Sistemi (Driver Drowsiness Detection)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Mesh-orange?style=for-the-badge)

Bu proje, trafik kazalarını önlemek amacıyla geliştirilmiş bir yapay zeka uygulamasıdır. Bilgisayar kamerası üzerinden sürücünün göz hareketlerini anlık olarak takip eder, yorgunluk veya uyku hali tespit ettiğinde **sesli ve görsel alarm** verir.

## 🎯 Proje Nasıl Çalışır?

Sistem, Google'ın **MediaPipe Face Mesh** teknolojisini kullanarak yüz üzerindeki 468 farklı noktayı tespit eder. Özellikle göz kapaklarına odaklanarak **EAR (Eye Aspect Ratio)** adı verilen matematiksel bir oran hesaplar.

* **Normal Durum:** Gözler açıkken EAR değeri 0.25'in üzerindedir.
* **Uyku Durumu:** Gözler kapandığında EAR değeri hızla düşer.
* **Alarm:** Eğer EAR değeri belirlenen eşik değerin altında 1.5 saniye boyunca kalırsa, sistem sürücünün uyuduğuna karar verir ve alarm çalar.

## 🛠️ Kullanılan Teknolojiler

* **Python 3:** Ana programlama dili.
* **OpenCV:** Kamera görüntüsünü işlemek için.
* **MediaPipe:** Yüz ve göz takibi (Landmark tespiti) için.
* **NumPy:** Geometrik ve vektörel hesaplamalar için.
* **Pygame:** Sesli uyarı sistemi için.

## 🚀 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için şu adımları izleyin:

1.  **Projeyi İndirin:**
    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/Driver-Drowsiness-Detection.git](https://github.com/KULLANICI_ADINIZ/Driver-Drowsiness-Detection.git)
    cd Driver-Drowsiness-Detection
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uygulamayı Başlatın:**
    ```bash
    python main.py
    ```

---
⚠️ **Not:** Uygulamanın sesli uyarı verebilmesi için proje klasöründe `alarm.mp3` veya `alarm.wav` dosyası bulunmalıdır.

👨‍💻 **Geliştirici: (https://github.com/emrrephlvn)
