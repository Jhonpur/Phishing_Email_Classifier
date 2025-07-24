# Dataset
- Assassin: features (sender,receiver,date,subject,body,label,urls) - labels (4091 normal, 1718 phishing)
- CEAS-08: features (sender,receiver,date,subject,body,label,urls) - labels (17312 normal, 21842 phishing)
- Enron: features (subject,body,label) - labels (15791 normal, 13976 phishing)
- Ling: features (subject,body,label) - labels (2401 normal, 458 phishing)
- Nazario: features (sender,receiver,date,subject,body,urls,label) - labels (1565 phishing, 0 normal)
- Nigerian_Fraud: features (sender,receiver,date,subject,body,urls,label) - labels(3332 phishing, 0 normal)

Presi questi 6 dataset si è creato un dataset unico con 3 label: subject, body e la label, in più si è aggiunto la source di provenienza del dataset

# Dataset 3 features
- body, object, label e source
- Le source sono sbilanciate, molte mail vengono da ceas-08, usare stratify durante il training oppure leave-one-out per testare
- il dataset totale è bilanciato 51% phishin 49% not phishing
- il dataset ha poche feature, bisogna crearne delle altre --> feature extraction
- analisi di feature importance con la gini impurity
- correlazione tra feature
- distribuzione normale e skew con separazione delle classi

GINI IMPURITY: Gini Impurity is a measurement used to build Decision Trees to determine how the features of a dataset should split nodes to form the tree. More precisely, the Gini Impurity of a dataset is a number between 0-0.5, which indicates the likelihood of new, random data being misclassified if it were given a random class label according to the class distribution in the dataset.

# PRE-PROCESSING
- si è eseguita un'analisi sulla percentuale di label, il dataset stesso è bilanciato, non ci saranno grossi problemi a valutarlo, ma il peso di ogni singolo dataset è diverso. Quindi ci si aspetta un buon risultato nel dataset totale, ma per evitare generalizzazione bisogna testarlo con i dataset singoli
- si controllano i valori nulli e le celle vuote, e si riempiono con una stringa vuota nel caso di testo oppure con la media nel caso di valori numerici
- dal testo vengono estratte delle feature numeriche tra cui: lunghezza dell'oggetto, numero di parole nel soggetto, lunghezza del body, numero parole nel body, densità del body, densità dell'oggetto, numero di link, numero di caratteri speciali, numero di punti esclamativi, flag se ha ip link, flag se ha parole bancarie.
- Inoltre vengon estratte diverse entropie (misura di causalità): tra cui entropia per l'oggetto, per carattere, per carattere non ascii, per digits, per punteggiatura. Per l'entropia si usa l'entropia di shannon (misura di informazione). C'è una formula che la calcola "Il teorema stabilisce che, per una serie di variabili aleatorie indipendenti ed identicamente distribuite (i.i.d.) di lunghezza che tende ad infinito, non è possibile comprimere i dati in un messaggio più corto dell'entropia totale senza perdita di informazione."

# ANALISYS
- adesso che abbiamo le nostre feature passiamo all'analisi
- si inizia con una HEAT MAP, per vedere se le feature sono correlate. Vengono scartate quelle con una valore di correlazione molto alto, perché sarebbero ridondanti e questo può destabilizzare i coefficienti nei modelli lineari. Inoltre rimuovere feature semplifica il modello
- si fa un'altra analisi di feature importance attraverso un classficatore random forest basandosi su quanto ogni feature riduce l'impurità dei nodi dell'albero usando una Gini Impurity Index. Vengono tolte le 3 peggiori
- si fa un'analisi finale sulla distribuzione delle feature. La maggior parte è asimmetrica con una distribuzione skew vicino lo zero. Mentre solo l'entropia ha distribuzione gaussiana. Questo ci dice che modelli come SVM non funzionerebbero bene, mentre Random Forest si.


# Paper
A. I. Champa, M. F. Rabbi, and M. F. Zibran, “Curated datasets and feature analysis for phishing email detection with machine learning,” in 3rd IEEE International Conference on Computing and Machine Intelligence (ICMI), 2024, pp. 1–7.

Processo che hanno seguito
1) Decoding
2) Extraction of Plain Text
3) Duplicate Removal
4) Discrepancy Handling: rimuovere mail vuote
5) Data Cleansing: miminizzare il rumore rimuovendo and the is
6) Vectorization: le email vengono trasformate in vettori numeri per gli algoritmi di ML. Usano TF-IDF, moltiplicato la frequenza di una parola per per la sua frequenza nel documento. L'attributo URLS è trasformato in una feature binaria

Usano 5 algoritmi di ML
- SVM, RandomForest, Extra Tree (ET), XGBoost, AdaBoost (ADB)
- usano stratified kfold. Mantengono la percentuale di sample per ogni classe
- metriche: TP, TN, FP, FN
- feature: nel SVM ogni feature ha un coefficente che rappresenta il peso nella funzione di decisione. In RF e ET la feature importance è calcolata da quanto le feature contribuiscono alla GIni impurity
- dopo aver trovato le feature, effettuano una MinMax normalization, per confrontare tutti gli algoritmi

Usano subject e body feature per ling e enron, per gli altri 5 usano: sender, receiver, date, subject, body e urls

- metriche 2: usano accuracy, precision, recall, f1score
- per dataset sbilanciati i migliori sono ADB e XGB
- per dataset grandi: ADB performa di meno in confronto agli altri
