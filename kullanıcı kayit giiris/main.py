from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from threading import Lock
app = Flask(__name__)
lock = Lock()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])  # GİRİŞ YAP 
def login():
    # Veritabanı bağlantısını oluştur
    conn = sqlite3.connect('database_adı.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Kullanıcıyı veritabanından kontrol et
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        if user:
        
            return redirect(url_for('success', username=username, password=password))
        else:
           
            return render_template('login.html', message='Hatalı kullanıcı adı veya şifre!')
    # Bağlantıyı kapat
    conn.close()
    return render_template('login.html', message='')

@app.route('/success')#LOGİN BAŞARILI  İSE : 
def success():
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template('success.html', username=username, password=password)
#? *******************************************************************************************************


@app.route('/register', methods=['GET', 'POST']) #KAYIT OL SAYFASI: 
def register():
    # Veritabanı bağlantısını oluştur
    conn = sqlite3.connect('database_adı.db')
    cursor = conn.cursor()

    if request.method == 'POST':            #htmlden gelen formdan gelen veriler
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')

        # Kullanıcıyı veritabanına ekle
        veri_ekle(new_username, new_password)  # veri_ekle  fonksiyonuna gönderdik 

        # Kayıt işleminden sonra login sayfasına yönlendir
        return redirect(url_for('login'))

    # Bağlantıyı kapat
    conn.close()

    return render_template('register.html')

def veri_ekle(username, password) :          # Kayıt ol bilgilerini : veritabanına ekleyen fonksiyon
      with lock:
        # Her fonksiyon içinde bağlantı ve cursor oluşturun
        baglanti = sqlite3.connect("database_adı.db")
        islem = baglanti.cursor()
        kayit = "INSERT INTO users(username, password) VALUES (?, ?)"
        islem.execute(kayit, (username, password))
        # Bağlantıyı ve cursor'ı kapatın
        baglanti.commit()
        baglanti.close()

# Kullanıcının şifresini güncelle
@app.route('/degistir_sifre',methods=['GET', 'POST'])
def degistir_sifre():
    if request.method == 'POST':
        current_username = request.form.get('current_username')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        conn = sqlite3.connect('database_adı.db')
        cursor = conn.cursor()

        # Kullanıcının mevcut şifresini kontrol et
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (current_username, current_password))
        user = cursor.fetchone()
        if user:
            # Kullanıcı adı ve şifre doğruysa, şifreyi güncelle
            cursor.execute('UPDATE users SET password=? WHERE username=?', (new_password, current_username))
            conn.commit()
            conn.close()
            return render_template('degistir_sifre.html', success_message='Şifre başarıyla değiştirildi.')
        else:
            # Kullanıcı adı veya şifre hatalıysa, hata mesajı ile birlikte sayfaya yönlendir
            conn.close()
            return render_template('degistir_sifre.html', error_message='Hatalı kullanıcı adı veya şifre!')
    return render_template('degistir_sifre.html')


# hesabı sil :

@app.route('/hesap_sil', methods=['GET', 'POST'])
def hesap_sil():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('database_adı.db')
        cursor = conn.cursor()

        #!  Kullanıcının mevcut şifresini kontrol et
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()

        if user:
            # Kullanıcı adı ve şifre doğruysa, hesabı sil
            cursor.execute('DELETE FROM users WHERE username=? AND password=?', (username, password))
            conn.commit()
            conn.close()
            return render_template('hesap_sil.html', success_message='Hesap başarıyla silindi.')
        else:
            # Kullanıcı adı veya şifre hatalıysa, hata mesajı ile birlikte sayfaya yönlendir
            conn.close()
            return render_template('hesap_sil.html', error_message='Hatalı kullanıcı adı veya şifre!')
    
    return render_template('hesap_sil.html')












if __name__ == '__main__':
    app.run(debug=True, port=8080)
