# 🛡️ Phishing Email Classifier

Sistema intelligente per la rilevazione automatica di email di phishing utilizzando tecniche di Machine Learning e Deep Learning.

## 📋 Descrizione del Progetto

**Phishing Email Classifier** è un'applicazione web progettata per identificare e classificare email potenzialmente pericolose (phishing/spam) attraverso l'analisi del contenuto del messaggio. Il sistema utilizza modelli di machine learning addestrati su dataset di email legittime e malevole per fornire predizioni accurate e motivate.

### Funzionalità Principali

- ✅ **Analisi automatica** di subject e body delle email
- 📊 **Score di probabilità** di phishing (0-100%)
- 🔍 **Identificazione dei motivi** che rendono un'email sospetta
- 🌐 **Rilevamento URL** e domini sospetti
- 💾 **Storico delle analisi** salvato su database
- 🖥️ **Interfaccia web intuitiva** per l'utilizzo

### Caratteristiche di Rilevamento

Il sistema analizza diverse caratteristiche per classificare le email:

- **Entropia del testo**: misura della casualità/complessità del contenuto
- **Presenza di parole sensibili**: credenziali, password, account, verify, ecc.
- **URL e indirizzi IP**: collegamenti sospetti o shortener
- **Domini non sicuri**: bit.ly, tinyurl, hosting gratuito
- **Linguaggio aggressivo**: offerte "gratuite", "solo oggi", urgenza
- **Caratteristiche statistiche**: lunghezza, densità, punteggiatura

---

## 🛠️ Stack Tecnologico

### Backend

- **Python 3.x** - Linguaggio principale
- **FastAPI** - Framework web moderno e performante
- **Uvicorn** - Server ASGI per FastAPI
- **SQLAlchemy** - ORM per gestione database
- **SQLite** - Database per storico delle analisi

### Machine Learning & Data Science

- **scikit-learn** - Libreria principale per ML (pipeline, classificatori)
- **pandas** - Manipolazione e analisi dati
- **numpy** - Calcoli numerici e array
- **joblib** - Serializzazione modelli ML
- **matplotlib & seaborn** - Visualizzazione dati (per training/analisi)

### Frontend

- **HTML5/CSS3** - Struttura e stile
- **Bootstrap** - Framework CSS responsive
- **Jinja2** - Template engine per rendering dinamico
- **JavaScript** - Interattività client-side

### Librerie Aggiuntive

- **email-validator** - Validazione indirizzi email
- **dnspython** - Query DNS per validazione domini
- **python-dotenv** - Gestione variabili d'ambiente
- **pydantic** - Validazione dati e serializzazione
- **requests** - Client HTTP per chiamate API

---

## 📁 Struttura del Progetto

```
Phishing_Email_Classifier/
│
├── app/                          # Applicazione principale
│   ├── api/                      # Endpoint API
│   │   ├── routes.py            # Route principali
│   │   ├── routes_ange.py       # Route modulo Angelo
│   │   └── routes_gabri.py      # Route modulo Gabriele
│   ├── database/                 # Configurazione database
│   ├── models/                   # Modelli dati SQLAlchemy
│   ├── utils/                    # Funzioni di utilità
│   └── main.py                  # Entry point FastAPI
│
├── Frontend/                     # Interfaccia utente
│   ├── static/                  # File statici (CSS, JS, immagini)
│   └── templates/               # Template HTML Jinja2
│
├── predicter/                    # Modulo predizione
│   └── spam_classifier_pipeline.joblib  # Modello ML pre-addestrato
│
├── models/                       # Modelli ML/DL
│   └── [file di training e modelli]
│
├── dataset/                      # Dataset per training
│   └── [file CSV/JSON con email]
│
├── predict_spam.py              # Script standalone predizione
├── requirements.txt             # Dipendenze Python
├── .gitignore                   # File da ignorare in Git
└── README.md                    # Questo file
```

---

## 🚀 Installazione e Avvio

### Prerequisiti

- Python 3.8 o superiore
- pip (package manager Python)
- Virtualenv (consigliato)

### Passaggi di Installazione

1. **Clona il repository**
   ```bash
   git clone <url-repository>
   cd Phishing_Email_Classifier
   ```

2. **Crea un ambiente virtuale**
   ```bash
   python -m venv .venv
   ```

3. **Attiva l'ambiente virtuale**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

5. **Avvia il server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Accedi all'applicazione**
   
   Apri il browser e vai su: `http://localhost:8000`

---

## 💡 Utilizzo

### Interfaccia Web

1. Accedi alla homepage dell'applicazione
2. Inserisci il **subject** dell'email nel primo campo
3. Inserisci il **body** (contenuto) dell'email nel secondo campo
4. Clicca su **"Analizza Email"**
5. Visualizza i risultati:
   - ✅ **Legittima** o ⚠️ **Sospetta**
   - Percentuale di probabilità di phishing
   - Motivi della classificazione
   - Presenza di URL

### API Programmatica

Puoi anche utilizzare l'API direttamente tramite richieste HTTP:

```python
import requests

url = "http://localhost:8000/api/predict"
data = {
    "subject": "Verifica il tuo account bancario",
    "body": "Clicca qui: http://bit.ly/fake-bank per verificare"
}

response = requests.post(url, json=data)
result = response.json()

print(f"È spam? {result['is_spam']}")
print(f"Probabilità: {result['spam_probability']}%")
print(f"Motivi: {result['spam_reasons']}")
```

### Script Standalone

```python
from predict_spam import predict_spam

result = predict_spam(
    subject="Congratulazioni! Hai vinto!",
    body="Clicca qui per richiedere il tuo premio: http://suspicious.com"
)

print(result)
```

---

## 🧠 Come Funziona il Modello

### Pipeline di Predizione

1. **Estrazione Features**
   - Lunghezza subject e body
   - Numero di parole
   - Densità del testo
   - Entropia dei caratteri
   - Percentuale di cifre e punteggiatura
   - Numero di punti esclamativi

2. **Preprocessing Testo**
   - Concatenazione subject + body
   - Vettorizzazione TF-IDF (nel modello)
   - Normalizzazione features numeriche

3. **Classificazione**
   - Il modello ML (Random Forest / Logistic Regression / altro) analizza le features
   - Output: probabilità di essere spam (0-1)
   - Soglia decisionale: tipicamente 0.5

4. **Post-processing**
   - Identificazione motivi specifici (regex patterns)
   - Rilevamento URL e domini sospetti
   - Categorizzazione del tipo di minaccia

---

## 🔒 Sicurezza e Privacy

- I dati delle email **non vengono condivisi** con terze parti
- Lo storico delle analisi è salvato **localmente** su database SQLite
- Il modello funziona **offline** dopo l'addestramento
- Non vengono inviate email o dati sensibili a servizi esterni

---

## 📊 Performance del Modello

*(Aggiungere metriche dopo il training finale)*

- **Accuracy**: XX%
- **Precision**: XX%
- **Recall**: XX%
- **F1-Score**: XX%

---

## 👥 Team di Sviluppo

Progetto di team sviluppato da:
- Angelo
- Gabriele
- Lorenzo

---

## 📝 Licenza

*(Specificare la licenza del progetto, es. MIT, Apache 2.0, ecc.)*

---

## 🤝 Contribuire

I contributi sono benvenuti! Per favore:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pusha sul branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

---

## 📧 Contatti

Per domande o supporto, contattare il team di sviluppo.

---

## 🔮 Sviluppi Futuri

- [ ] Integrazione con client email (Gmail, Outlook)
- [ ] Modello Deep Learning (LSTM/Transformer)
- [ ] Analisi allegati email
- [ ] Dashboard analytics avanzata
- [ ] API pubblica con autenticazione
- [ ] Supporto multilingua
- [ ] Sistema di feedback utente per miglioramento continuo