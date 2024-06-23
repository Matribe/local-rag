# PROGRAM

MODEL_LLM = "mistral"

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"

DATA_PATH = "data"
UPLOADS_PATH = "data/uploads/"
CHROMA_PATH = "data/chroma"
SQLITE_PATH = "data/sqlite/"


DATABASE_NAME = "database.db"

SQL_REQUEST = """
SELECT r.model_name 
FROM Overview_of_LLM r JOIN 
Large_Language_Models o
ON r.model_name = o.model_name;
"""

NUMBER_OF_GENERATIONS = 20

INITIAL_INDEX_TUPLE = 0

# USER INTERFACE

USER = "user"
AI = "assistant"

INITIAL_PROMPT = """
                    **Bienvenu sur le chatBOT du projet ChatGPT vs SQL.**  
                    Pour interagir avec les rêquetes SQL : 
                    - Tester une rêquete SQL en la tapant `--sql <Formule SQL>`.
                    - Lancer le dataset de test en tapant `--sql run tests`.

                    Pour intéragir avec les documents du RAG :
                    - Voir les documents ingérés en tapant `--ingest see`.
                    - Ingérer un nouveau document en tapant `--ingest add <chemin du fichier>`.
                    
                    Pour des informations complémentaires :
                    - Si vous souhaitez revoir les commandes tapez `--help`.
                    - Pour obtenir plus d'informations sur le projet tapez `--project`.

                    Pour modifier ou afficher les paramètres :
                    - Pour modifier le nombre de fois que le LLM fait sa recherche tapez `--set <Votre nombre>`
                      Attention :orange[plus le nombre spécifié est grand, plus le temps d'éxécution sera long].  
                      Votre nombre de générations doit être contenu entre 3 et 30 inclus.
                    - Pour afficher le nombre de générations tapez `--set see`.
                """

PROJECT_PROMPT = """
                    **Projet ChatGPT vs SQL.**  

                    ### Participants :  
                    - Mathieu RIBEYRON  
                    - Claire MATHIEU  
                    - Raphaël PIETRZACK  
                    - Robin VIOLET  
                      
                      
                    ### Résumé :  
                      
                    SQL versus GPT est un sujet proposé par la faculté de science de Aix-Marseille pour l'UE
                    *Projet Mathématique Informatique*.  
                    L'objectif de ce dernier est de marier dans un programme l'emploi de SQL sur des données non 
                    structurées (comme du texte) à l'aide de l'utilisation des Large Language Models. 
                    Vous êtes en train d'utiliser le chatBOT permettant de manipuler le programme proposé 
                    en réponse au sujet.

                       
                    ### Remarques Importantes :
                      
                    - Les :orange[**formules SQL doivent êtres écrites correctement**],
                      sinon elle seront jugées inutilisables.
                    - Les formules SQL avec de multiples tables 
                    :orange[**doivent utiliser nécessairement des alias**] !  
                    Seule les requêtes utilisant 2 tables ou plus sont concernées.
                    - Le nombre de générations réglables directement via le chatBOT est le nombre de fois que le LLM
                    relance votre requête. Plus le nombre est grand, plus le nombre d'hallucinations est minimisé.  
                    Cela car seuls les résultats 3 fois identitques sont fusionnés et gardés dans la réponse.  
                    Cependant, pour un trop grand nombre l'effet inverse peut se produire. Initialiement ce nombre
                    est de 20. 
                """