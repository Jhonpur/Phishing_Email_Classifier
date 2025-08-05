# Machine Learning
- carico il dataset
- droppo le colonne che non mi servono
- il dataset di train sarà composto da una sola colonna testuale dalla dalla concatenazione del subject + body, in più abbiamo le feature numeriche.
- la feature testuale viene codificata in numero con il TF-IDF, mentre quelle numeriche vengono scalate
- creo la pipeline ed addestro il primo modello, un Random Forest, lo stesso con cui ho fatto l'analisi per la feature selection
-  ottengo dei buoni risultati, con accuracy 0.98 ma c'è una probabilità che il modello stia generalizzando
## Procedimento con Leav-one-out Cross Validation
### Random Forest
- rifaccio il processo di prima ma questa volta tolgo dalla fase di train una source per volta, in modo tale che il modello non la veda durante la fase di training, ma verrà comunque testata.
- qui ottengo i risultati reali, alcuni modelli funzionano bene, altri no come Nazario e Enron. L'obiettivo è che con tutti abbiamo un accuracy, precision e recall alta.
- provo altro algoritmi
                support  accuracy  precision  recall  f1-score
Assassin         5809.0     0.878      0.801   0.782     0.792
CEAS-08         39154.0     0.851      0.886   0.841     0.863
Nigerian_Fraud   3332.0     0.957      1.000   0.957     0.978
Nazario          1565.0     0.668      1.000   0.668     0.801
Enron           29767.0     0.781      0.744   0.816     0.778
Ling             2859.0     0.942      0.798   0.856     0.826
### XGboost
- XgBoost (Extreme Gradient Boosting) è un algoritmo di apprendimento automatico basato sul gradient boosting, ovvero una tecnica di ensemble che costruisce modelli in sequenza, dove ogni modello successivo cerca di correggere gli errori dei precedenti
- i risultati sono un po' migliori rispetto al precedente
XGBoosting
                 support  accuracy  precision  recall  f1-score
Assassin         5809.0     0.878      0.808   0.772     0.790
CEAS-08         39154.0     0.825      0.873   0.804     0.837
Nigerian_Fraud   3332.0     0.962      1.000   0.962     0.981
Nazario          1565.0     0.687      1.000   0.687     0.814
Enron           29767.0     0.802      0.737   0.902     0.811
Ling             2859.0     0.913      0.660   0.943     0.776
### ET - Extra Tree
- Extra Trees (Extremely Randomized Trees) è un ensemble di alberi decisionali che introduce ancora più casualità rispetto ad una Random Forest. Mentre la Random Forest cerca il miglior split tra un sottoinsieme casuale di feature, ET sceglie il punto di split in modo complemanente casuale.
- Abbiamo risultati buoni su nazario ma pessimi sugli altri.
ET - Extra Trees
                 support  accuracy  precision  recall  f1-score
Assassin         5809.0     0.764      0.562   0.919     0.697
CEAS-08         39154.0     0.646      0.837   0.454     0.589
Nigerian_Fraud   3332.0     0.522      1.000   0.522     0.686
Nazario          1565.0     0.788      1.000   0.788     0.881
Enron           29767.0     0.609      0.553   0.877     0.678
Ling             2859.0     0.765      0.395   0.878     0.544
### AdaBoost - Adaptive Boosting
- anche questp è un ensemble che combina classificatori deboli (di solito alberi di profondità 1) in modo sequenziale. Ogni nuovo classificatore si concentra sugli errori fatti dai precedenti, assegnando il loro peso
- Più semplice di XGBoost ma meno potente in contesti complessi, sensibile
- AdaBoost dovrebbe funzionare meglio con dataset piccoli, infatti otteniamo il risultato migliore
AdaBoost
                 support  accuracy  precision  recall  f1-score
Assassin         5809.0     0.777      0.594   0.776     0.673
CEAS-08         39154.0     0.718      0.821   0.631     0.714
Nigerian_Fraud   3332.0     0.779      1.000   0.779     0.876
Nazario          1565.0     0.781      1.000   0.781     0.877
Enron           29767.0     0.671      0.599   0.903     0.720
Ling             2859.0     0.750      0.375   0.836     0.518

Il migliore algoritmo di ML per adesso è XGBoost

# Deep Learning
- adesso proviamo il Deep Learning
- Proviamo un modello ibrido LSTM + dati numerici: prima tokenizziamo il testo, creando un vocabolario di parole più frequenti, quelle non presenti verrano marcate come OOV. I testi vengono trasformati in sequenze di interi e padded (riempiti per avere una lunghezza fissa). Vengono normalizzati i dati numerici.
Abbiamo prima il testo
- input: sequenze di interi (1 per parola)
- embedding: mappa ogni parola in un vettore denso (dimensione 128)
- LSTM(64): layer ricorrente che apprende le dipendenze sequenziali tra parole -> utile per testo con struttura (email messaggi)
Poi abbiamo le feature numeriche. I due vengono contatenzati e passati attravero un layer dense + dropout per ridurre overfitting. Ed infine abbiamo una sigmoid per classificazione binaria
LSTM - teoria
LSTM (Long Short-Term Memory) è un tipo di RNN (rete neruale ricorrente) che mantiene informazioni a lungo termine tra le parole in un testo. E' progettato per superare i limiti delle RNN standard (come il vanishing gradient), e perfetto per analizzare testo sequenziale, come email, messaggi e frasi.
LSTM serve in questo caso a catturare la struttura del testo che un TF-DF o XGBoost non può cogliere perché lavora su un bag-of-words o n-gram senza contesto



# Papers
1) `SecureNet`: A Comparative Study of DeBERTa and Large Language Models for Phishing Detection (giugno 2024): Confronta DeBERTa V3 con modelli LLM tipo GPT‑4 nella classificazione di phishing (email, SMS, URL, dati sintetici). DeBERTa ottiene un recall del 95.17 %, GPT‑4 circa 91 % su dataset pubblici. [https://arxiv.org/abs/2406.06663?utm_source=chatgpt.com](link) - GPT4 vs transformers
2) `ChatSpamDetector`: Leveraging Large Language Models for Effective Phishing Email Detection (febbraio 2024): Sistema che utilizza GPT‑4 come LLM per classificare email sospette con accuracy di 99.70 %, restituendo anche spiegazioni interpretative (XAI) del motivo della classificazione. GPT4 vs transformers
3) An Explainable Transformer-based Model for Phishing Email Detection (febbraio 2024): Fine‑tuning di DistilBERT con tecniche XAI (LIME, Transformer Interpret), affrontando anche il bilanciamento del dataset e spiegabilità delle predizioni. [https://arxiv.org/abs/2402.13871?utm_source=chatgpt.com](link). XAI
4) `MultiPhishGuard`: An LLM-based Multi‑Agent System for Phishing Email Detection (maggio 2025): Framework multi-agente che combina modelli specializzati su testo, URL, metadata, con apprendimento rinforzato e generazione di attacchi adversarial. Accuracy del 97.89 %, false positive ~2.7 %, false negative ~0.2 %, con spiegazioni semplificate per l’utente. [https://arxiv.org/abs/2505.23803?utm_source=chatgpt.com](link). - Multi-agent, adversarial learning
5) Advanced `BERT and CNN‑Based` Computational Model for Phishing Detection in Enterprise Systems (ottobre 2024): Utilizza BERT per estrarre feature e una CNN per la classificazione. Ottiene accuracy intorno al 97.5 % in contesti aziendali. [https://www.techscience.com/CMES/v141n3/58510]()
6) Comparative Investigation of Traditional ML vs Transformer Models (2024, MDPI Electronics). Su vari dataset, confronta logistic regression, SVM, random forest con transformer (BERT, RoBERTa, ALBERT). RoBERTa raggiunge fino al 99.43 % di accuracy, mentre distilBERT e BERT seguono da vicino. [https://www.mdpi.com/2079-9292/13/24/4877?utm_source=chatgpt.com](link)
7) Systematic Review of Deep Learning for Phishing Email Detection (MDPI). Analizza vari studi con BERT, RoBERTa, DeBERTa e modelli ensemble, evidenziando accuracies 98–99 % e F1 tra 0.92 e 0.97. Manca però il trattamento dei link o metadati nell'email. [https://www.mdpi.com/2079-9292/13/19/3823?utm_source=chatgpt.com](link)

## LSTM

1. A Novel Deep Learning Model for Phishing Email Detection using BiLSTM and Attention Mechanism (2023): BiLSTM + attention per classificazione binaria.

2. Phishing Detection using LSTM and GloVe Word Embeddings (2022): Classificazione basata su embedding statici (GloVe) + LSTM. Funziona bene, ma meno robusto rispetto a modelli contextualizzati (es. BERT).

3. CNN-BiLSTM Hybrid Model for Phishing Email Detection (2022): CNN per estrazione locale + BiLSTM per sequenze. Performance migliorata rispetto a CNN-only o LSTM-only.