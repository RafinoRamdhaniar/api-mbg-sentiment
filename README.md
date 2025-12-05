Sentiment Analysis API (SVM & IndoBERT)

Aplikasi berbasis Flask ini menyediakan API untuk melakukan analisis sentimen pada teks Bahasa Indonesia menggunakan dua pendekatan model:

SVM (Support Vector Machine) (Machine Learning Tradisional)

IndoBERT (Deep Learning / Transformer)

Prasyarat

Pastikan Anda telah menginstal:

Python 3.8 atau lebih baru

Git

Struktur File yang Dibutuhkan

Sebelum menjalankan aplikasi, pastikan Anda memiliki file model dan dataset berikut di dalam folder root project (sejajar dengan app.py):

File Model SVM:

svm_model.pkl

tfidf_vectorizer.pkl

label_encoder.pkl

File Model BERT:

Folder ./saved_model (berisi config.json, pytorch_model.bin, tokenizer.json, dll).

Dataset Pendukung:

colloquial-indonesian-lexicon.csv (Kamus kata alay/slang).

Cara Menjalankan (Step-by-Step)

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda.

1. Clone Repository

Buka terminal (Command Prompt/PowerShell/Terminal) dan clone repository ini:

git clone https://github.com/RafinoRamdhaniar/api-mbg-sentiment.git
cd api-mbg-sentiment


2. Membuat Virtual Environment (Venv)

Sangat disarankan menggunakan virtual environment agar library tidak bentrok dengan project lain.

Untuk Windows:

python -m venv venv
venv\Scripts\activate


Untuk macOS / Linux:

python3 -m venv venv
source venv/bin/activate


Jika berhasil, Anda akan melihat (venv) di sebelah kiri baris perintah terminal Anda.

3. Install Dependencies

Install semua library yang dibutuhkan menggunakan requirements.txt:

pip install -r requirements.txt


Catatan: Instalasi PyTorch (torch) dan Transformers mungkin memakan waktu agak lama tergantung koneksi internet karena ukurannya cukup besar.

4. Menjalankan Aplikasi

Jalankan server Flask dengan perintah:

python app.py


Jika berhasil, Anda akan melihat output seperti ini:

📂 Memuat Model SVM...
✅ Model SVM berhasil dimuat.
📂 Memuat Model BERT...
✅ Model BERT berhasil dimuat.
 * Running on [http://0.0.0.0:5000/](http://0.0.0.0:5000/) (Press CTRL+C to quit)


Cara Menggunakan API

Anda bisa menggunakan Postman, Insomnia, atau cURL untuk mengetes API.

1. Cek Status API

URL: http://localhost:5000/

Method: GET

2. Prediksi Menggunakan SVM

URL: http://localhost:5000/predict/svm

Method: POST

Body (JSON):

{
    "text": "Barangnya bagus banget, pengiriman cepat!"
}


Response:

{
    "model": "SVM",
    "sentiment": "Positif",
    "text_cleaned": "barang bagus banget kirim cepat"
}


3. Prediksi Menggunakan IndoBERT

URL: http://localhost:5000/predict/bert

Method: POST

Body (JSON):

{
    "text": "Saya sangat kecewa dengan pelayanan toko ini."
}


Response:

{
    "model": "IndoBERT",
    "score": "98.5%",
    "sentiment": "Negatif",
    "text_cleaned": "saya sangat kecewa dengan layan toko ini"
}