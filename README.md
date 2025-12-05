# Sentiment Analysis API (SVM & IndoBERT)

Requirement
Python 3.10

## Cara Menjalankan (Step-by-Step)

### 1. Clone Repository

Buka terminal (Command Prompt/PowerShell/Terminal) dan clone repository ini:
```
git clone https://github.com/RafinoRamdhaniar/api-mbg-sentiment.git
cd api-mbg-sentiment
```

### 2. Downlod Model
Download model melalui link berikut ini:
https://drive.google.com/drive/folders/14rID3n81r6jCsUPmWJV14u2yiYzuUwta?usp=drive_link

setelah berhasil terdownload unzip dan pindahkan pada folder api-mbg-sentiment

### 3. Membuat Virtual Environment (Venv)

Sangat disarankan menggunakan virtual environment agar library tidak bentrok dengan project lain.

Untuk Windows:
```
python -m venv venv
venv\Scripts\activate
```

Untuk macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```

Jika berhasil, Anda akan melihat (venv) di sebelah kiri baris perintah terminal Anda.

### 4. Install Dependencies

Install semua library yang dibutuhkan menggunakan requirements.txt:
```
pip install -r requirements.txt
```

Catatan: Instalasi PyTorch (torch) dan Transformers mungkin memakan waktu agak lama tergantung koneksi internet karena ukurannya cukup besar.

### 5. Menjalankan Aplikasi

Jalankan server Flask dengan perintah:
```
python app.py
```

Jika berhasil, Anda akan melihat output seperti ini:
```
📂 Memuat Model SVM...
✅ Model SVM berhasil dimuat.
📂 Memuat Model BERT...
✅ Model BERT berhasil dimuat.
 * Running on [http://0.0.0.0:5000/](http://0.0.0.0:5000/) (Press CTRL+C to quit)
```