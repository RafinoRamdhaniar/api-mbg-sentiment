from flask import Flask, request, jsonify
import pandas as pd
import re
import emoji
import string
import os
import joblib
from bs4 import BeautifulSoup
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

app = Flask(__name__)

# Global Setup
SLANG_PATH = "colloquial-indonesian-lexicon.csv"
MODEL_BERT_PATH = "./saved_model"
factory = StopWordRemoverFactory()
stopwords_default = factory.get_stop_words()

# Kata penting yang TIDAK BOLEH DIHAPUS
excluded_stopwords = [
    'tidak', 'tak', 'nggak', 'gak', 'bukan', 'non', 
    'jangan', 'dilarang', 
    'kurang', 'lebih', 'sangat', 'paling', 'terlalu', 
    'tapi', 'tetapi', 'namun', 
    'baik', 'bagus', 'buruk', 'jelek', 'kecewa', 'parah', 'puas', 'senang', 'jelas'
]
final_stopwords = [w for w in stopwords_default if w not in excluded_stopwords]
dictionary = ArrayDictionary(final_stopwords)
stopword_remover = StopWordRemover(dictionary)

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

if os.path.exists(SLANG_PATH):
    df_slang = pd.read_csv(SLANG_PATH)
    slang_dict = dict(zip(df_slang['slang'], df_slang['formal']))
else:
    slang_dict = {}

# Load SVM Model
print("📂 Memuat Model SVM...")
try:
    svm_model = joblib.load('svm_model.pkl')
    svm_vectorizer = joblib.load('tfidf_vectorizer.pkl')
    svm_encoder = joblib.load('label_encoder.pkl')
    print("✅ Model SVM berhasil dimuat.")
except Exception as e:
    print(f"❌ Error SVM: {e}")
    svm_model = None

# Load Bert Model
print("📂 Memuat Model BERT...")
try:
    bert_tokenizer = AutoTokenizer.from_pretrained(MODEL_BERT_PATH, local_files_only=True)
    bert_model = AutoModelForSequenceClassification.from_pretrained(MODEL_BERT_PATH, local_files_only=True)
    
    bert_pipe = pipeline("text-classification", model=bert_model, tokenizer=bert_tokenizer)
    print("✅ Model BERT berhasil dimuat.")
except Exception as e:
    print(f"❌ Error BERT: {e}")
    bert_pipe = None

# Preprocessing
def normalize_slang(text):
    words = text.split()
    normalized_words = [slang_dict.get(word, word) for word in words]
    return ' '.join(normalized_words)

def clean_text(text):
    text = str(text).lower()
    text = normalize_slang(text)
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r"http\S+|www.\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = emoji.replace_emoji(text, "")
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    
    text = stopword_remover.remove(text) 
    text = stemmer.stem(text)
    return text

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "API Aktif",
        "endpoints": {
            "svm": "/predict/svm",
            "bert": "/predict/bert"
        }
    })

@app.route('/predict/svm', methods=['POST'])
def predict_svm():
    if not svm_model:
        return jsonify({'error': 'Model SVM gagal dimuat'}), 500

    try:
        data = request.json
        raw_text = data.get('text', '')
        processed_text = clean_text(raw_text)

        if not processed_text:
            return jsonify({'text_original': raw_text, 'sentiment': 'Netral', 'info': 'Text kosong'})

        # Vectorize & Predict
        text_vectorized = svm_vectorizer.transform([processed_text])
        prediction_index = svm_model.predict(text_vectorized)
        sentiment_label = svm_encoder.inverse_transform(prediction_index)[0]

        return jsonify({
            'model': 'SVM',
            'text_cleaned': processed_text,
            'sentiment': sentiment_label
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/bert', methods=['POST'])
def predict_bert():
    if not bert_pipe:
        return jsonify({'error': 'Model BERT gagal dimuat'}), 500

    try:
        data = request.json
        raw_text = data.get('text', '')
        processed_text = clean_text(raw_text)

        if not processed_text:
             return jsonify({'text_original': raw_text, 'sentiment': 'Netral', 'info': 'Text kosong'})

        # Predict Pipeline
        result = bert_pipe(processed_text)[0]

        return jsonify({
            'model': 'IndoBERT',
            'text_cleaned': processed_text,
            'sentiment':result['label'],
            'score': f"{round(result['score'] * 100, 2)}%"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)