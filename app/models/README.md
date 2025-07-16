# Machine Learning
- sota: randomforest, svm, xgboost, naive bayes

# Deep Learning
- sota: LSTM, GRU, CNN, Transformer

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