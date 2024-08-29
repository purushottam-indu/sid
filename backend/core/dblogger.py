import aioodbc
import os
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

ENV_FILE = os.getenv("ENV_FILE") or ".env_local"
load_dotenv(ENV_FILE)

AZURE_LOGGING_DB=os.getenv("AZURE_LOGGING_DB")
AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME=os.getenv("AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME")
AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD=os.getenv("AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD")
AZURE_LOGGING_SERVERNAME=os.getenv("AZURE_LOGGING_SERVERNAME")
AZURE_LOGGING_DRIVER=os.getenv("AZURE_LOGGING_DRIVER")
AZURE_LOGGING_TABLE = os.getenv("AZURE_LOGGING_TABLE")

# print(AZURE_LOGGING_DB,'AZURE_LOGGING_DB',
#       AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME,'AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME',
#       AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD,'AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD',
#       AZURE_LOGGING_SERVERNAME,'AZURE_LOGGING_SERVERNAME',
#       AZURE_LOGGING_DRIVER,'AZURE_LOGGING_DRIVER',
#       AZURE_LOGGING_TABLE,'AZURE_LOGGING_TABLE'
#       )


async def log_api_response(user,input_timestamp, api,model_name,token):
    """
    Log request to the database
    """

    current_timestamp = datetime.now()
    resp_time = current_timestamp - input_timestamp
    logging_conn_string = f"DRIVER={AZURE_LOGGING_DRIVER};SERVER=tcp:{AZURE_LOGGING_SERVERNAME};DATABASE={AZURE_LOGGING_DB};UID={AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME};PWD={AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD};Authentication=ActiveDirectoryPassword"
    print(logging_conn_string, 'connection string values')
    query = f"""INSERT INTO LOGGING.{AZURE_LOGGING_TABLE} (APPLN, LOG_DT_TM, USR_NM, RESP_DT_TM, model_name, RESP_TM_SEC,NO_TOKENS) VALUES (?, ?, ?, ?, ?, ?,?) """
    params = (api, input_timestamp, user, current_timestamp, model_name, resp_time.total_seconds() ,token)
    try:
        conn = await aioodbc.connect(dsn=logging_conn_string)
        cursor = await conn.cursor()
        print("DB Connection Success")
        #print(query,params)
        await cursor.execute(query,params)
        await conn.commit()
        await cursor.close()
        await conn.close()
    except Exception as e:
        print(str(e))
        logging.exception("Exception in logging - ",str(e) )