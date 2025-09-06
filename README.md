

FaceID Authentication & Housing Platform

Umumiy ma’lumot:

1. Ushbu loyiha foydalanuvchilarga yuz orqali autentifikatsiya (FaceID) qilish imkonini beradi. Autentifikatsiyadan o‘tgan foydalanuvchilar uylarini sotish yoki sotib olish uchun e’lon joylashlari mumkin. Platforma Bezmakler’ga o‘xshab ishlaydi va foydalanuvchilarga qulay uy qidirish hamda e’lon berish imkoniyatini beradi.

   Asosiy funksiyalar

   FaceID orqali login/register – OpenCV va dlib yordamida yuzni aniqlash va autentifikatsiya.

   Uy e’lonlari – Foydalanuvchilar uy sotish yoki sotib olish uchun e’lon joylashi mumkin.

   Filtr va qidiruv – Narx, joylashuv, turiga qarab qidiruv va saralash imkoniyati.

   Rasmlar yuklash – Uy e’lonlariga suratlarni joylash.

   Xavfsizlik – FaceID tufayli login jarayoni tezlashgan va xavfsizlik oshgan.


2. Texnologiyalar

  Backend: Python, Django, Django REST Framework (DRF)
  
  Face Recognition: OpenCV, Dlib
  
  Database: PostgreSQL
  
  Deployment: Docker

3. Swagger (API hujjatlari)

  API hujjatlarini Swagger orqali ko‘rishingiz mumkin:
  
  http://ijarax.digitallaboratory.uz/swagger/
  
  Bu yerda barcha endpointlar (login, register, e’lon yaratish, e’lonlarni olish va h.k.) ishlatilish tartibi bilan ko‘rsatilgan.

⚙️ O‘rnatish
    git clone https://github.com/FarhodGanijonov/Faceid.git
    cd Faceid
    docker-compose up --build
    
    Keyin loyihani http://localhost:8000 orqali ishga tushiring.

👨‍💻 Muallif

Farhod Ganijonov
Backend Developer (Python/Django, DRF, OpenCV, Dlib, SQLite / PostgreSQL, Swagger (drf-yasg), Git & GitHub)
