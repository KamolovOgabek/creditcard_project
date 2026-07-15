# Credit Card Customer Analysis Dashboard (CardAnalytics)

Ushbu loyiha banklar va moliya tashkilotlari uchun kredit karta mijozlarining xatti-harakatlarini tahlil qilish, ularning xarajatlari hamda balans statistikalarini monitoring qilish va eng muhimi — **mijozlarning ketib qolish (churn/attrition) xavfini oldindan aniqlash** uchun mo'ljallangan professional **EDA (Exploratory Data Analysis)** tahlil platformasidir.

Loyiha to'liq real ma'lumotlar to'plami (`BankChurners.csv`) bilan ishlaydi va bank xodimlariga mijozlar portfelini boshqarishda ma'lumotlarga asoslangan (data-driven) qarorlar qabul qilishga ko'maklashadi.

---

## 🚀 Loyiha Qanday Muammolarga Yechim Bo'ladi?

1. **Mijozlar Ketishini Oldini Olish (Churn Prevention):**
   Mijozlarning bank xizmatlaridan voz kechish sabablarini demografik ma'lumotlar (yosh, daromad, ta'lim darajasi) va tranzaksiyalar faolligi (miqdori, soni) orqali vizual tahlil qiladi. Bu bankka mijoz ketib qolmasidan oldin unga maxsus takliflar taqdim etish imkonini beradi.
2. **Kredit Risklarini Boshqarish:**
   Mijozlarning o'rtacha kredit limitlari, aylanma qarzdorligi (revolving balance) hamda kredit limitidan foydalanish koeffitsientini (utilization ratio) hisoblab beradi. Bu limitlarni optimallashtirish va risklarni nazorat qilishga yordam beradi.
3. **Ma'lumotlar Xavfsizligi va Izolyatsiyasi:**
   Tizim ko'p foydalanuvchili bo'lganligi sababli, har bir bank tahlilchisi faqat o'ziga tegishli mijozlar bazasini yuklaydi va tahlil qiladi. Tahlilchilar ma'lumotlari bir-biriga aralashmaydi.
4. **Android va Mobil Qurilmalardan Qulay Foydalanish:**
   Dashboard to'liq mobil moslashuvchan (responsive) qilingan. Bank rahbariyati yoki xodimlari istalgan joyda planšet yoki smartfon orqali tizimga kirib, hisobotlarni ko'ra oladi.

---

## 🛠️ Asosiy Funksional Imkoniyatlar (Features)

* **Xavfsiz Autentifikatsiya (Authentication):** Bank xodimlari uchun hisob yaratish (Register), tizimga kirish (Login) va chiqish (Logout) tizimi. Mehmonlar uchun dashboard sahifalariga kirish bloklangan.
* **Umumiy Vizual Dashboard (Chart.js):** 
  - Jami faol mijozlar va ketgan mijozlar nisbati (pie-chart).
  - Mijozlar yoshi taqsimoti (histogramma).
  - Daromad toifalari bo'yicha tahlillar.
* **Xarajatlar Tahlili (Spending Analysis):** 
  - Tranzaksiyalar soni va umumiy xarajat summasi o'rtasidagi bog'liqlik (Scatter plot).
  - Mijozning ta'lim darajasi uning xarajatlariga qay darajada ta'sir qilishi tahlili.
* **Balans va Limitlar Statistikasi (Balance & Limit):**
  - Kredit limitlari taqsimoti.
  - Karta turlari (Blue, Silver, Gold, Platinum) bo'yicha kreditdan foydalanish darajasi.
  - Aylanma balanslar taqsimoti.
* **Mijozlar Ma'lumotlar Bazasi (Customers Table):**
  - Yuklangan datasetdagi barcha mijozlarni sahifalangan (pagination) jadval shaklida chiqarish.
  - Mijoz ID, jinsi, daromadi yoki karta turi bo'yicha tezkor qidiruv (Search) tizimi.
* **Mobil Moslashuvchanlik:**
  - Mobil o'lchamlarda yopiladigan Sidebar, hamburger menyu va sensorli boshqaruv.
  - Katta jadvallarning mobil ekranda buzilmasdan gorizontal skrol bo'lishi.

---

## 💻 Ishlatilgan Texnologiyalar (Tech Stack)

* **Backend:** Python + Django (Web framework)
* **Ma'lumotlarni Qayta Ishlash:** Pandas, NumPy (Ma'lumotlarni tahlil qilish uchun)
* **Frontend:** HTML5, CSS3 (Vanilla responsive styling), Vanilla JS, FontAwesome (ikonkalar uchun)
* **Grafiklar:** Chart.js (Interaktiv dynamic vizualizatsiyalar)
* **Production Deploy:** WhiteNoise (Statik fayllar xizmati), Gunicorn (Production WSGI server)
