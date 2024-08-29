import os
import pandas as pd
import openai
import openpyxl as xl
import re
from sqlalchemy import create_engine
import sqlite3
pd.set_option('display.max_rows', None)
import logging


class csv_exc_sql:
    def __init__(self) -> None:
        pass

    def column_formatting(self, columns):
        column_list = columns.str.strip()
        column_list = column_list.str.replace(' ', '_')
        column_list = list(map(lambda x: '_' + x if x[0].isdigit() else x, column_list))
        return column_list

    def sql_approach(self, user_q, file, user_name):
        AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        AZURE_OPENAI_API_KEY_2 = os.getenv("AZURE_OPENAI_API_KEY_2")
        AZURE_OPENAI_SERVICE = os.getenv("AZURE_OPENAI_SERVICE")
        AZURE_OPENAI_SERVICE_2 = os.getenv("AZURE_OPENAI_SERVICE_2")
        openai_api_type = "azure"
        #openai_api_version = "2023-03-15-preview" 
        openai_api_version = "2024-02-01" 
        openai_api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com" 
        openai_api_base_2=f"https://{AZURE_OPENAI_SERVICE_2}.openai.azure.com"
        #print("openai_api_base",openai_api_base)
        openai_api_key = AZURE_OPENAI_API_KEY
        try:
            temp_database = "./temp_database"
            os.makedirs(os.path.join(temp_database, user_name), exist_ok=True)

            # print("-----------------------------path file")
            # print(f'{os.path.abspath(os.path.join(temp_database, user_name))}/my_database.sqlite')
            # print(os.path.dirname(__file__))
            # print(os.path.dir('temp_database',user_name))
            
            connection = sqlite3.connect(f'{os.path.abspath(os.path.join(temp_database, user_name))}/my_database.db')
            # engine = create_engine(f'sqlite:///{os.path.abspath(os.path.join(temp_database, user_name))}/my_database.sqlite')
            
            excel_flag = False
            table_name = ""
            if file.endswith('.csv'):
                df = pd.read_csv(file)
                df.columns = self.column_formatting(df.columns)
                # logging.info("------ Before df.to_sql----------")
                df.to_sql('my_table', con=connection, if_exists='replace', index=False)
                # logging.info("------ after df.to_sql----------")
                table_name = 'my_table'
                #print(df)
            
            elif file.endswith('.xlsx'):
                excel_flag = True
                workbook = xl.load_workbook(os.path.join(file))
                wbsheets = workbook.sheetnames
                sheet_list = []
                sheet_dict = {}
                i = 0
                
                for name in wbsheets:
                    df_name = f'sheet{i+1}' 
                    sheet_list.append(df_name)
                    sheet_dict[name] = df_name
                    globals()[df_name] = pd.read_excel(file, sheet_name = name)
                    globals()[df_name].columns = self.column_formatting(globals()[df_name].columns)
                    i = i + 1
                    globals()[df_name].to_sql(f'{df_name}', con = connection, if_exists='replace', index=False)
                
              #  print(sheet_dict)

                sheet_found = False
                sheet_match = ""
                # sheet_match_replacement = ""
                for sheet_name, sheet_table_name in sheet_dict.items():
                  #  print(sheet_name, sheet_table_name, user_q)
                    if str(sheet_name) in user_q:
                        df = globals()[sheet_table_name]
                        table_name = sheet_table_name

                        sheet_found = True
                        user_q = user_q.replace(sheet_name, sheet_table_name)
                        sheet_match = sheet_table_name
                        # print(user_q.replace(sheet_name, sheet_table_name))
                        # print(user_q, table_name)
                        break
                if not sheet_found:
                    return (f"Please specify sheetname from \n{list(sheet_dict.keys())}.", 0, user_q)

                # pattern = r'sheet\d+'
                # match = re.search(pattern, user_q.lower())
                # if match:
                # # Store the matched substring in a variable
                #     matched_string = match.group(0)
                #     df_name = matched_string
                #     print(matched_string)
                #     if df_name in sheet_list:
                #     # if df_name in sheet_dict.values:
                #         df = globals()[df_name]
                #         table_name = matched_string
                #         print(df_name, table_name)
                #     else: 
                #         return (f"""Please specify sheetname from {sheet_list} based on your question, Here's the reference for the sheet names :-
                #                 \n{sheet_dict} """, 0)
                # else:
                #     return (f"""Please specify sheetname from {sheet_list} based on your question, Here's the reference for the sheet names :-
                #             \n{sheet_dict}""", 0)


            #Extracting column level information 
            # columns_type = {}
            # for i in df.columns:
            #     values = {}
            #     unique_values = [] 
                
            #     if df[i].dtypes == "O":  
            #         values['date_type'] = "VARCHAR"
            #         unique_values = df[i].unique()
            #         if len(unique_values) < 20:
            #             values['unique_values'] = list(unique_values)
            #     else:
            #         values['date_type'] = "FLOAT"
            #     columns_type[i] = values
            # logging.info("--- Before column formatting-------")
            columns_type = {}
            max_unique_values = 10
            sql_type_mapping = {
                'int64': 'INTEGER',
                'float64': 'FLOAT',
                'object': "VARCHAR",
                'bool': "BOOLEAN",
                'datetime64[ns]': "TIMESTAMP"
            }

            for column_name, column_type in df.dtypes.items():
                values = {}
                values['date_type'] = sql_type_mapping.get(str(column_type), 'TEXT')
                if column_type == "object":
                    unique_values = df[column_name].unique()
                    values['unique_values'] = list(unique_values)[:max_unique_values]
                columns_type[column_name] = values
            # logging.info("---after column formatting-------")
            ## prompt content
            prompt = """
            You will be acting as an SQLite expert.
            Your goal is to give correct, executable SQL queries which can be directly executed in SQLite without any error.
            Don't include any words in the sql query like "Answers:", "Answer:", "Results:","sql" etc. 
            You just need to produce SQL queries do not produce any words other than SQL query as this query will be directly executed.
            Do not create column names of your own.
            you are given 12 rules below in the rules section that must be followed.
            You are given metadata and user question, the metadata is in <Metadata> tag.
            Based on the <Metadata> given and user Question asked; You should respond with a correct SQL query.
            Never use Top function while creating SQL query, instead always use limit function at end of query.
            Do not write MEDIAN function, use any other approach for median calcalution
            Only provide a single query in the response.
            

            <rules>
            0. Table name is {0}
            1. Never use LIMIT function while creating SQL query, instead always use top function at starting of query.
            2. You MUST NOT hallucinate about tables, data, columns and query.
            3. Don't create any query with CREATE, DROP, RENAME, ALTER, UPDATE, MERGE & DELETE statements.
            4. If encountered with CREATEDDATE column convert it to date (mm/dd/yyyy) format
            5. Name the selcted columns when using aggregate functions.
            6. ALWAYS INCLUDE from these SQLite inbuilt functions in SELECT STATEMENT : COUNT,AVG,SUM,CASE. Don't generate the query without these.
            7. Use 'DATENAME' function to show month. Output we receive must include name of the month rather tham number such that January is shown before February and February is shown above March such that IT DOESNT THROW ERROR.
            8. Use allias with heading in capital letter for each column. 
            9. If user asks for weekly data then week starts from friday to friday. in output give only week end date in dd/mm/yyyy format.
            10. Make sure to generate error free queries. Utilise the metadata for column level information
            11. Only provide a single query in the response.
            12. Dont use MEDIAN function, use any other approach for median calculation 
            </rules>

            <Metadata>
            Below is the information related to data, having information about column type. For categorical columns unique values are provided if they are less than 10 in number. 
            {1}


            Most Important : Make sure to not include any words in the sql query like "Answers:", "Answer:", "Results:" etc.

            """.format(table_name, columns_type)
           
            print("Column_type",column_type)
            #print("Prompt",prompt)
            # logging.info("----Before SQL Query Generation-------")
            openai.api_key =AZURE_OPENAI_API_KEY_2
            openai.api_type = "azure"
            openai.api_version="2023-12-01-preview"
            openai.api_base= openai_api_base_2
            response = openai.ChatCompletion.create(
                engine="gpt4turbo",
                # engine = "gpt4",
                # engine = "gptdemo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_q}
                ], 
                temperature = 0.2
                    )
            # logging.info("----After SQL Query Generation-------")
            openai.api_key =AZURE_OPENAI_API_KEY
            openai.api_type = "azure"
            openai.api_version="2024-02-01"
            openai.api_base= openai_api_base
            sql_query = response['choices'][0]['message']['content']
            print("Sql_Query",sql_query)
           # print(sql_query)

            # with engine.connect() as connection:
            #     output = pd.read_sql_query(sql_query, connection)
            # engine.dispose()

            output = pd.read_sql_query(sql_query, connection)
           # print("OUTPUT",output)
            # logging.info(output, response["usage"]["total_tokens"])
            if excel_flag:
                user_q = user_q.replace(sheet_match, "")
              #  print(user_q)
            return (output, response["usage"]["total_tokens"], user_q)
        except:
            output = """You might have asked something out of the context with the uploaded data, If not please be more specific in the input asked"""
            return(output, 0, user_q)



