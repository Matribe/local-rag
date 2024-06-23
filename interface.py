import streamlit as st
import os
import shutil
import time
from pandas import DataFrame
import pandas as pd

from src.execute import Execute
from src.llm import Llm
from data.dataset_queries import TEST_QUERIES
from src.settings import *

class Interface:
     
    def __init__(self):
        
        # Setting title
        self.title = "Projet ChatGPT vs SQL"
        st.title(self.title)
        st.markdown("---")

        # Setting sessions
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "generation_value" not in st.session_state:
            st.session_state.generation_value = NUMBER_OF_GENERATIONS


        self.number_of_generations = st.session_state.generation_value

        self.llm = Llm()

# Initials methods

    def run(self):
            
            # Initial prompt not in historic
            with st.chat_message(name=AI):
                st.markdown(INITIAL_PROMPT)

            # Reprint message in historic
            for message in st.session_state.messages:
                
                match message['typeChat']:

                    case 'chat':
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])

                    case 'table':
                        st.table(message['content'])

                    case 'sql_code':
                        st.code(message['content'], language='sql')

                    case 'doc_display':
                        st.success(message['content'])

            # Setting chat input
            if prompt := st.chat_input("Que voulez-vous faire ?"):
                with st.chat_message(name=USER):
                    st.markdown(prompt)

                self.add_chat_historic(USER, prompt)

                self.response(prompt)
    
    def response(self, prompt: str):
        
        if prompt == '--sql run tests':
            self.sql_run_tests()
            return
        
        if prompt == '--ingest see':
            self.ingest_see()
            return
        
        if prompt == '--set see':
            self.see_number_of_generations()
            return
        
        if prompt == '--help':
            self.see_help()
            return
        
        if prompt == '--project':
            self.see_project()
            return
        
        if '--sql' in prompt:
            self.sql_execute_query(prompt)
            return
        
        if '--set ' in prompt:
            self.set_number_of_generations(prompt)
            return
        
        if '--ingest add' in prompt:
            self.ingest_add(prompt)
            return
        
        self.ai_display('Il semblerai que vous :red[n\'ayez pas tapé une commande reconnue]...')

# Command methods

#  --ingest [...]

    def ingest_add(self, prompt: str):

        _,_,path = prompt.partition('--ingest add ')
        is_file_exist = os.path.isfile(path)

        _,_,extension = path.partition('.')

        if is_file_exist and extension in ('md', 'pdf', 'docx'):

            try :
                shutil.copy(path, UPLOADS_PATH)
                self.llm.get_chat_chain(path)
                self.ai_display("Le fichier spécifié a été :green[vectorisé dans la base de données !]")

            except Exception as e:
                self.ai_display_error(e)
            
            return
        
        self.ai_display('Le fichier spécifié :red[n\'est pas au bon format].')

    def ingest_see(self):
        
        uploaded_documents = os.listdir(UPLOADS_PATH)

        self.ai_display("Voici les document chargés dans le programme :")

        for doc in uploaded_documents:
            
            logo = '❌ document non pris en charge : '

            if '.md' in doc.lower():
                logo = '🗒️'
            if '.pdf' in doc.lower():
                logo = '📑'
            if '.docx' in doc.lower():
                logo = '📄'
            
            content = f' {logo} {doc}'
            st.success(content)

            self.add_chat_historic('none', content, 'doc_display')

# --set [...]

    def set_number_of_generations(self, prompt: str):

        try:

            _,_,second_part = prompt.partition(' ')
            number = int(second_part)

            if number >= 3 and number<= 30:

                st.session_state.generation_value = number
                self.ai_display(f"Changement du nombre de generation par {number} !")
                return
            
            self.ai_display_error(ValueError("The specified value isn't between 3 and 30."))

        except Exception as e:

            self.ai_display_error(e)

    def see_number_of_generations(self):
        
        self.ai_display(f'''Le nombre de génération actuel est : {self.number_of_generations}  
                            Pour le modifier tapez `--set <Votre valeur>`.''')
        
# --help

    def see_help(self):

        self.ai_display(INITIAL_PROMPT)

# --project

    def see_project(self):

        self.ai_display(PROJECT_PROMPT)
        self.ai_display('Que puis-je faire d\'autre pour vous ?')

# --sql [...]

    def sql_execute_query(self, prompt: str):

        try:
            # Treat query
            query = prompt.replace("--sql ", "")

            # Initialisation widget
            placeholder = st.empty()
            placeholder.status("Initialisation...")

            # Initialisation Execute instance
            with placeholder.status("Initialisation...") as status:
                
                try:
                    execute = Execute(query)
                
                except Exception as e:

                    status.update(label="L'initialisation a echouee !", 
                                  state="error", 
                                  expanded=False)
                    
                    time.sleep(1)
                    placeholder.empty()

                    raise e
                
                else:
                    status.update(label="Initialisation effectuée avec succès !", 
                                  state="complete", 
                                  expanded=False)
            
            # Clearing initialisation placeholder
            time.sleep(2)
            placeholder.empty()

            # Placing progress bar
            progress_text = "Opération en cours. Veuillez patienter."
            my_bar = st.progress(0, text=progress_text)
            
            # Preparing necessities
            number_of_tables = len(execute.tables.keys()) 
            total_percentage = number_of_tables*self.number_of_generations

            response = f"""Voici le résultat de votre demande :"""
            code = f'''{query}''' 

            answer_dict = {}

            index_generation = 1

            # Main loop for each table
            for table, columns in execute.tables.items():

                answer_dict[table] = {"column_names": columns}
                data_cache = []

                # For each attribute
                for _ in range(self.number_of_generations):

                    # Main use
                    table_name = str(table).replace("_", " ")

                    answer,_ = execute.llm.ask(f"{tuple(columns)} for {table_name}", 
                                                f"Give me some for {tuple(columns)}")

                    answer = execute.tuple_analyzer.treat_results(answer)
                    answer = execute.tuple_manage.verif_size_columns(len(columns), answer)

                    data_cache.extend(answer)

                    # Updating progress bar
                    percent_complete = round((((index_generation)))/total_percentage, 2)
                    my_bar.progress(percent_complete, text=f'Travail en cours sur la table : {table_name}')
                    index_generation +=1
                
                # Data cache
                data_cache = execute.tuple_analyzer.get_most_frequent_tuples(data_cache, 3)
                answer_dict[table]["data"] = data_cache

            
            # Making progress bar disappear
            time.sleep(2)
            my_bar.empty()


            table_with_type = execute.database_table_analyzer.type_of_attributs(execute.tables, answer_dict)

            # Sql
            execute.database.create_tables(table_with_type)
            execute.database.fill_tables(answer_dict)
            execute.sql_answer = execute.database.query(query, [])

            # Displaying SQL formula in chat
            self.ai_display(response)
            st.code(code, language='sql')
            self.add_chat_historic('None', code, 'sql_code')

            # Displaying response if not empty
            if execute.sql_answer:

                columns_database = execute.sql_answer[0] if isinstance(execute.sql_answer[0], tuple) else execute.sql_answer

                df = pd.DataFrame(execute.sql_answer, columns=("colonne %d" % i for i in range(1,len(columns_database)+1)))
                st.table(df)
                
                self.add_chat_historic('None', df, 'table')

            else:

                self.ai_display(':red[Aucun réponse trouvée...]')

        except Exception as e:
            self.ai_display_error(e)
        
    def sql_run_tests(self):

        self.ai_display("""En fonction des paramètres :orange[cette opération 
                        peut prendre beaucoup de temps]...""")
        
        st.toast('Lancement du dataset de test !', icon='🧪')

        for query in TEST_QUERIES:
            self.sql_execute_query(query)

        self.ai_display('Les tests sont terminés, que voulez faire d\'autre ?')

# BOT print and historic methods

    def ai_display_error(self, error: Exception):
        
        response =  f"""
                        L\'erreur suivante est survenue :\\
                        :red-background[**_ERROR:_** {str(error)}]
                    """
        
        self.ai_display(response)

        st.toast('Oups... Une erreur est survenue', icon='❌')

    def ai_display(self, message: str):
        
        with st.chat_message(name=AI):
            st.markdown(message)

        self.add_chat_historic(AI, message)

    def add_chat_historic(self, role:str, text: str | DataFrame, typeChat='chat'):
        st.session_state.messages.append({"role": role, "content": text, "typeChat": typeChat})
        
# MAIN

if __name__ == "__main__":
    gui = Interface()
    gui.run()