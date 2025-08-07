**DOCUMENTAZIONE DELLA PARTE RELATIVA AL DATABASE**

in questa parte, abbiamo usato le tecnologie seguente:

-fastapi per il backend 
-sqlalchemy come ORM
-pydantic per la validazione
-sqlite come database

di seguito elencherò i diversi moduli/ file  anziché cosa contengono e cosa fanno

**1- models.py**
contiene le classi che rappresentanno le tabelle presenti nel nel niostro database() . ogni classe possiede degli attributi che rappresentano un istanza della classe, nonchè deglin attributi di tipo relationship che rappresentano le relazioni tra le tabelle della del database.

**2-schemas**
contiene gli schemas pydantic che permettono la validazione dei dati per le situazioni rappresentate mediante classi nel file.ogni classe contiene il nome e il tipo di dato che deve essere passato o ritornato e poi validato .

**3-crud**
contiene tutte le funzioni crud che permetto di interragire con il database(creare utenti, cancellare utenti, creare emails, cancellare emails , interrogare il database ecc...)

**4-db**
contienne la sessione relativa al database, che ci permette di accedere al nostro database e di esguire operazioni specifici.

**5-main**
contiene righe di codice per testare il funzionamento della parte di database.

models ==> contiene le classi relative alle tabelle del database( classe User ,Email e Usermail). è stato  usato sqlalchemy  come ORM e          pydantic per la validazioendei formati dei dati.

schemas ==> contiene i formati di input e output della mail e utenti. è secondo questo formato che la nostra app in backend riceve        e         ritorna dati in formato json .

crud ==> contiene tutte le funzioni che  interragiscono direttamente con il database.

db ==> contiene l'intansiazione del databse che viene poi usato per in crud e negli altri file del progetto.

main ==> contiene righe di codice per popolare e testare questa parte del progetto.