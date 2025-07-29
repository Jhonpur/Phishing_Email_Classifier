documentazione della parte relativa al database.

models ==> contiene le classi relative alle tabelle del database( classe User ,Email e Usermail). è stato  usato sqlalchemy  come ORM.

schemas ==> contiene i formati di input e output della mail e utenti. è secondo questo formato che la nostra app in backend riceve e ritorna dati in formato json .

crud ==> contiene tutte le funzioni che  interragiscono direttamente con il database.

db ==> contiene l'intansiazione del databse che viene poi usato per in crud e negli altri file del progetto.

main ==> contiene righe di codice per popolare e testare questa parte del progetto.