import cv2
import mediapipe as mp
import numpy as np
import pygame # Ses için

# --- AYARLAR (HASSASİYET) ---
# Eğer alarm çok çabuk çalıyorsa bu değeri küçültün (örn: 0.20)
EAR_THRESHOLD = 0.22 

# Kaç kare boyunca göz kapalı kalırsa alarm çalsın?
# (Ortalama bir web kamerası 30 FPS çeker. 40 kare ≈ 1.3 saniye demektir)
CLOSED_FRAMES_THRESHOLD = 40 

# --- SES SİSTEMİNİ BAŞLAT ---
pygame.mixer.init()
try:
    # Klasörünüzde 'alarm.wav' adında bir dosya olduğundan emin olun!
    alarm_sound = pygame.mixer.Sound("alarm.mp3")
    print("Ses dosyası yüklendi.")
except:
    print("UYARI: 'alarm.mp3' dosyası bulunamadı! Ses çalmayacak.")
    alarm_sound = None

# --- MEDIAPIPE GÖZ İNDEKSLERİ ---
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_INDICES = [33, 160, 158, 133, 144, 153]

def calculate_ear(landmarks, indices, img_w, img_h):
    """Göz Açıklık Oranını (EAR) hesaplar."""
    coords = []
    for i in indices:
        lm = landmarks[i]
        coords.append((int(lm.x * img_w), int(lm.y * img_h)))

    # Dikey mesafeler
    d1 = np.linalg.norm(np.array(coords[1]) - np.array(coords[5]))
    d2 = np.linalg.norm(np.array(coords[2]) - np.array(coords[4]))
    # Yatay mesafe
    horizontal = np.linalg.norm(np.array(coords[0]) - np.array(coords[3]))

    # EAR Formülü
    ear = (d1 + d2) / (2.0 * horizontal)
    return ear, coords

# --- KURULUMLAR ---
mp_face_mesh = mp.solutions.face_mesh
cap = cv2.VideoCapture(0)
FRAME_COUNTER = 0 # Gözün kapalı kaldığı süreyi sayacak sayaç

print("Sistem Başlatılıyor... Çıkış için 'q' tuşuna basın.")

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # 1. Görüntüyü EN BAŞTA çevir (Ayna etkisi + Düzgün yazı için)
        image = cv2.flip(image, 1)
        img_h, img_w, _ = image.shape

        # 2. MediaPipe İşlemleri
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb_image.flags.writeable = False
        results = face_mesh.process(rgb_image)

        # 3. Yüz Bulunduysa İşle
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark

                # EAR Hesapla
                left_ear, left_coords = calculate_ear(landmarks, LEFT_EYE_INDICES, img_w, img_h)
                right_ear, right_coords = calculate_ear(landmarks, RIGHT_EYE_INDICES, img_w, img_h)
                avg_ear = (left_ear + right_ear) / 2.0

                # Gözleri Çiz (Yeşil Çerçeve)
                cv2.polylines(image, [np.array(left_coords)], True, (0, 255, 0), 1)
                cv2.polylines(image, [np.array(right_coords)], True, (0, 255, 0), 1)

                # --- KARAR MEKANİZMASI ---
                if avg_ear < EAR_THRESHOLD:
                    FRAME_COUNTER += 1 # Sayaç artıyor
                    
                    # Eşik değer aşıldı mı? (Gerçekten uyuyor mu?)
                    if FRAME_COUNTER >= CLOSED_FRAMES_THRESHOLD:
                        # ALARM DURUMU!
                        color = (0, 0, 255) # Kırmızı
                        
                        # Ekrana Uyarı Bas
                        cv2.putText(image, "UYANIIN!!!", (50, 150), 
                                    cv2.FONT_HERSHEY_COMPLEX, 3, color, 5)
                        
                        cv2.putText(image, "KAZA RISKI!", (50, 250), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

                        # Ses Çal (Eğer zaten çalmıyorsa)
                        if alarm_sound and not pygame.mixer.get_busy():
                            alarm_sound.play()
                
                else:
                    # Gözler açıldı, her şeyi sıfırla
                    FRAME_COUNTER = 0
                    color = (0, 255, 0) # Yeşil
                    if alarm_sound:
                        alarm_sound.stop()

                # İstatistikleri Ekrana Yaz
                cv2.putText(image, f'EAR: {avg_ear:.2f}', (30, 50), 
                            cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)

        # Görüntüyü Göster
        cv2.imshow('Surucu Yorgunluk Takip Sistemi v1.0', image)

        # 'q' tuşu ile çıkış
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()