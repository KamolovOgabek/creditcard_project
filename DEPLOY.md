# Django Loyihasini Tekinga Serverga Joylash (Deploy)

Ushbu loyiha GitHubga yuklandi: `https://github.com/KamolovOgabek/creditcard_project.git`

Loyihani internetga bepul joylashtirish uchun **Render.com** yoki **PythonAnywhere** xizmatlaridan foydalanish tavsiya etiladi.

---

## 1-Yo'l: Render.com orqali deploy (Tavsiya etiladi)

Render loyihani to'g'ridan-to'g'ri GitHubdan olib, avtomatik internetga chiqaradi.

### Qadamlar:
1. [Render.com](https://render.com) saytida ro'yxatdan o'ting va GitHub profilingizni ulang.
2. Dashboardda **New +** tugmasini bosing va **Web Service** ni tanlang.
3. GitHub ro'yxatidan `creditcard_project` repozitoriyasini tanlang (**Connect** bosing).
4. Sozlamalarni quyidagicha to'ldiring:
   - **Name:** loyiha nomi (masalan: `card-analytics`)
   - **Runtime:** `Python 3`
   - **Build Command:** 
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```bash
     gunicorn creditcard_project.wsgi:application
     ```
   - **Instance Type:** `Free` (Tekin)
5. **Deploy Web Service** tugmasini bosing. Loyiha bir necha daqiqada ishga tushadi va sizga tekin havola (URL) beriladi.

> [!WARNING]
> Render.com bepul versiyasida SQLite ma'lumotlar bazasi va yuklangan rasmlar (media) vaqtinchalik hisoblanadi (server o'chib yonganda o'chadi). Doimiy saqlash uchun Renderda tekin PostgreSQL ochib, settings.py ga ulash tavsiya etiladi.

---

## 2-Yo'l: PythonAnywhere orqali deploy (Doimiy SQLite uchun)

PythonAnywhere SQLite ma'lumotlar bazasini doimiy (persistent) saqlab qoladi.

### Qadamlar:
1. [PythonAnywhere.com](https://www.pythonanywhere.com) saytidan bepul hisob oching.
2. **Consoles** bo'limiga o'tib, **Bash** konsolini oching.
3. Loyihani GitHubdan yuklab oling:
   ```bash
   git clone https://github.com/KamolovOgabek/creditcard_project.git
   cd creditcard_project
   ```
4. Virtual muhit ochib, kutubxonalarni o'rnating:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 creditcard-env
   pip install -r requirements.txt
   ```
5. **Web** bo'limiga o'ting, **Add a new web app** bosing:
   - **Domain:** bepul domain beriladi
   - **Select Web Framework:** `Manual Configuration` -> `Python 3.10`
6. Quyidagi sozlamalarni o'rnating:
   - **Source code directory:** `/home/username/creditcard_project`
   - **Working directory:** `/home/username/creditcard_project`
   - **Virtualenv:** `/home/username/.virtualenvs/creditcard-env`
7. **WSGI configuration file** havolasini bosing, ichidagi hamma narsani o'chirib, faqat quyidagini yozing:
   ```python
   import os
   import sys

   path = '/home/username/creditcard_project'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'creditcard_project.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
   *(Eslatma: `username` o'rniga o'z PythonAnywhere loginizni yozing).*
8. Web bo'limida **Reload** tugmasini bosing. Loyiha internetda tayyor bo'ladi!
