# #import io
# import json
# import logging
# # import mimetypes
# import os
# from typing import AsyncGenerator
# import aiohttp
# from aiohttp import web
# import openai
# import requests
# import aioodbc
# from datetime import datetime, timedelta
# import time
# import time
# import asyncio
# # from azure.identity.aio import DefaultAzureCredential
# from azure.monitor.opentelemetry import configure_azure_monitor
# # from azure.search.documents.aio import SearchClient
# # from azure.storage.blob.aio import BlobServiceClient
# from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
# import shutil
# import shutil
# # from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
# from quart import (
#     Blueprint,
#     Quart,
#     redirect,
#     url_for,
#     current_app,
#     jsonify,
#     make_response,
#     request,
#     send_from_directory,
#     session,
#     render_template
# )
# from msal import ConfidentialClientApplication 
# import tempfile
# from dotenv import load_dotenv

# #from approaches.chatreadretrieveread import ChatReadRetrieveReadApproach
# from approaches.generalAssistant import GeneralAssistant
# from approaches.documentQnA import DocumentQnA
# from core.vector_store import create_vectorstore
# from core.token_count import token_counter
# from approaches.documentQnA import DocumentQnA
# from core.vector_store import create_vectorstore
# from core.token_count import token_counter

# #Load environment file
# # ENV_FILE = os.getenv("ENV_FILE") or ".env_local"
# # load_dotenv(ENV_FILE)


# # CONFIG_SSO = "azure_sso"
# # CONFIG_CHAT_APPROACHES = "chat_approaches"
# # CONFIG_LOGGING = "logging_config"
# # #CONFIG_BLOB_CONTAINER_CLIENT = "blob_container_client"

# bp = Blueprint("routes", __name__, static_folder="static")

# vector_db = {}
# vector_db = {}

# @bp.route("/")
# @bp.route("/<path:path>")
# async def index():
#     """
#     Serve the 'index.html' file as a static resource.
#     """
#     return await bp.send_static_file("index.html")
#     if is_auth():
#         if is_kumo_auth():
#             return await bp.send_static_file("index.html")
#         else:
#             return await render_template('401.html')
#     elif 'code' in request.args:
#         code = request.args.get('code')
#         pca = current_app.config[CONFIG_SSO]['pca']
#         auth_code = pca.acquire_token_by_authorization_code(code,scopes=current_app.config[CONFIG_SSO]['scope'],redirect_uri=current_app.config[CONFIG_SSO]['redirect_uri'])
#         if 'error' in auth_code:
#             # Handle error case
#             return 'Error: ' + auth_code['error']
        
#         user_name = auth_code['id_token_claims']['preferred_username']
#         #user_name = 'gnosti@dsi.com'
#         #user_name = 'gnosti@dsi.com'
#         name = auth_code['id_token_claims']['name']
#         session['access_token'] = auth_code['access_token']
#         session['refresh_token'] = auth_code['refresh_token']
#         session['expire_time'] = datetime.now() + timedelta(seconds=auth_code['expires_in'])
#         #session['expire_time'] = datetime.now() + timedelta(seconds=60)
#         session['user_name'] = user_name
#         # session['user_name'] = "akurapa@dsi.com"
#         logging.debug(f"this is auth_code for: {session['user_name']}; {auth_code}")
#         #print(session['user_name'], "user_name")
#         response = redirect(url_for('routes.index'))
#         response.set_cookie('username', name)
#         return response
#     else:
#         pca = current_app.config[CONFIG_SSO]['pca']
#         auth_url = pca.get_authorization_request_url(
#         scopes=current_app.config[CONFIG_SSO]['scope'],
#         redirect_uri=current_app.config[CONFIG_SSO]['redirect_uri'],
#         prompt='select_account',  # Forces the user to select their account on each login attempt
#         state='random_state'  # Add a random state value to mitigate CSRF attacks
#     )
#         return redirect(auth_url)
#     return "Some Error Occured"
    


# @bp.route("/favicon.ico")
# async def favicon():
#     """
#     Serve the app icon file as a static resource.
#     """
#     return await bp.send_static_file("favicon.ico")


# @bp.route("/assets/<path:path>")
# async def assets(path):
#     """
#     Serve the static javscript assest file as a static resource.
#     """
#     return await send_from_directory("static/assets", path)


# @bp.route("/chat", methods=["POST"])
# async def chat():
#     return jsonify({"hi , I am a dummy"}), 500
#     if not request.is_json:
#         return jsonify({"error": "request must be json"}), 415
#     request_json = await request.get_json()
#     approach = request_json["approach"]
#     #session['user_name'] = 'gnosti@dsi.com'
#    # user_name = 'gnosti@dsi.com'
#     #session['user_name'] = 'gnosti@dsi.com'
#    # user_name = 'gnosti@dsi.com'
#     try:
#         impl = current_app.config[CONFIG_CHAT_APPROACHES].get(approach)
#         if not impl:
#             return jsonify({"error": "unknown approach"}), 400
#         # Workaround for: https://github.com/openai/openai-python/issues/371
#         async with aiohttp.ClientSession() as s:
#             openai.aiosession.set(s)
#             r = await impl.run_without_streaming(request_json["history"], request_json.get("overrides", {}), user_name= session['user_name'])
#             #r = await impl.run_without_streaming(request_json["history"], request_json.get("overrides", {}))
#             #print("run_without_streaming in app.py", r)
#         return jsonify(r)
#     except Exception as e:
#         logging.exception("Exception in /chat")
#         return jsonify({"error": str(e)}), 500



# async def format_as_ndjson(r: AsyncGenerator[dict, None]) -> AsyncGenerator[str, None]:
#     """
#     Format a stream of dictionaries as NDJSON (Newline-Delimited JSON).

#     This function takes an asynchronous generator of dictionaries as input and yields
#     NDJSON strings. Each dictionary is converted to a JSON string and terminated with
#     a newline character. This is used for streaming.
#     """
#     async for event in r:
#         yield json.dumps(event, ensure_ascii=False) + "\n"


# @bp.route("/chat_stream", methods=["POST"])
# async def chat_stream():
#     return jsonify({"hi , I am a dummy"}), 500
#     if is_auth():
#         if not request.is_json:
#             return jsonify({"error": "request must be json"}), 415
#         request_json = await request.get_json()
#         approach = request_json["approach"]
#       #  session['user_name'] = 'gnosti@dsi.com'
#       #  user_name = 'gnosti@dsi.com'
#       #  session['user_name'] = 'gnosti@dsi.com'
#       #  user_name = 'gnosti@dsi.com'
#         request_timestamp = datetime.now()
#         try:
#             impl = current_app.config[CONFIG_CHAT_APPROACHES].get(approach)
#             if not impl:
#                 return jsonify({"error": "unknown approach"}), 400
#             #print(vector_db[session["user_name"]])
#             response_generator = impl.run_with_streaming(request_json["history"], request_json.get("overrides", {}), user_name= session['user_name'])
#             #response_generator = impl.run_with_streaming(request_json["history"], request_json.get("overrides", {}),session['user_name'])
#             response = await make_response(format_as_ndjson(response_generator))
#             response.timeout = None  # type: ignore
#             # # await log_api_response(input_timestamp=request_timestamp,api='ai-gen',approach=approach )
#             return response
#         except Exception as e:
#             logging.exception("Exception in /chat")
#             return jsonify({"error": str(e)}), 500
#     else:
#         #print("Error unauth")
#         return jsonify({"error": str("Unauthorized or session has expired. Please refresh the page to login again.")}), 401

  

  

# # @bp.before_request
# # async def ensure_openai_token():
# #     if openai.api_type != "azure_ad":
# #         return
# #     openai_token = current_app.config[CONFIG_OPENAI_TOKEN]
# #     if openai_token.expires_on < time.time() + 60:
# #         openai_token = await current_app.config[CONFIG_CREDENTIAL].get_token(
# #             "https://cognitiveservices.azure.com/.default"
# #         )
# #         current_app.config[CONFIG_OPENAI_TOKEN] = openai_token
# #         openai.api_key = openai_token.token

# # async def log_api_response(input_timestamp, api,approach):
# #     """
# #     Log request to the database
# #     """
# #     config = current_app.config[CONFIG_LOGGING]
# #     user = session['user_name']
# #     current_timestamp = datetime.now()
# #     resp_time = current_timestamp - input_timestamp
# #     model_name = "gpt-3.5"
# #     logging_conn_string = f"DRIVER={config['driver']};SERVER=tcp:{config['server']};DATABASE={config['db']};UID={config['username']};PWD={config['password']};Authentication=ActiveDirectoryPassword"
# #     query = f"""INSERT INTO LOGGING.{config['table']} (APPLN, LOG_DT_TM, USR_NM, RESP_DT_TM, model_name, RESP_TM_SEC) VALUES (?, ?, ?, ?, ?, ?) """
# #     params = (api, input_timestamp, user, current_timestamp, model_name, resp_time.seconds)
# #     try:
# #         conn = await aioodbc.connect(dsn=logging_conn_string)
# #         cursor = await conn.cursor()
# #         print("DB Connection Success")
# #         await cursor.execute(query,params)
# #         await conn.commit()
# #         await cursor.close()
# #         await conn.close()
# #     except Exception as e:
# #         print(str(e))
# #         logging.exception("Exception in logging - ",str(e) )


# async def token_c(response):
#     print(await response.get_data())


# def is_auth() -> bool:
#     """
#     Checks if user is authenticated and session data exists in Quart Session
#     """
#     return True
#     if 'access_token' in session:
#         return True
#     else:
#         return False

# def token_refresh():
#     if datetime.now() > session['expire_time']:
#         pca = current_app.config[CONFIG_SSO]['pca']
#         refresh_token = session['refresh_token']
#         scope = current_app.config[CONFIG_SSO]['scope']
#         new_token = pca.acquire_token_by_refresh_token(refresh_token, scopes=scope)
#         session['access_token'] = new_token['access_token']
#         session['refresh_token'] = new_token['refresh_token']
#         session['expire_time'] = datetime.now() + timedelta(seconds=new_token['expires_in'])
#         #session['expire_time'] = datetime.now() + timedelta(seconds=60)


# def is_kumo_auth():
#     """
#     Check if the user is authorized to access the access the ChatDSI.
#     """
#     token_refresh()
#     # headers = {  
#     # 'Authorization': 'Bearer ' + session['access_token'],  
#     # 'Content-Type': 'application/json'  
#     # }
#     # response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq 'e457b5c3-6590-4374-9f92-49a75eba03e4'", headers=headers)  
#     # response2 = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq '312b0f8e-15a5-4a99-9252-78d8eaa49a02'", headers=headers)  
#     # if response.status_code == 200 or response2.status_code == 200: 
#     #     ##print('success')
#     #     return True
#     # else:
#     #     return False

# # CODE ADDED FOR NESTED AD GROUPS AUTHORIZATION --started

#     tenant_id = os.getenv("AZURE_AUTH_TENNANT_ID")
#     client_id = os.getenv("AZURE_AUTH_CLIENT_ID")
#     client_secret = os.getenv("AZURE_AUTH_CLIENT_SECRET")
#     parent_group_id = "e457b5c3-6590-4374-9f92-49a75eba03e4"


#     #Acquire Access Token to read groups
#     token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
#     token_data = {
#         "grant_type": "client_credentials",
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "scope": "https://graph.microsoft.com/.default"
#     }

#     token_response = requests.post(token_url, data=token_data)
#     token_response.raise_for_status()
#     access_token2 = token_response.json().get("access_token")

#     headers = {  
#     'Authorization': 'Bearer ' + access_token2,  
#     'Content-Type': 'application/json'  
#     }

#     all_group_ids = [parent_group_id]
#     # all_group_ids.append("312b0f8e-15a5-4a99-9252-78d8eaa49a02")       #comment before release
#     all_group_ids.extend(get_nested_group_ids(parent_group_id, headers)) #uncomment before release
#     #print("all_group_ids: ",all_group_ids)

#     headers = {  
#      'Authorization': 'Bearer ' + session['access_token'],  
#      'Content-Type': 'application/json'  
#      }

#     # response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$top=999", headers=headers)
#     # logging.debug(f"this is response for {session['user_name']}: {response.json()}")
#     # if response.status_code == 200:
#     #     user_groups = response.json().get('value', [])
#     #     user_group_ids = [group["id"] for group in user_groups]

#     flag_group = False
#     for all_group_id in all_group_ids:
#         response = requests.get(f"https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq '{all_group_id}'", headers=headers)
#         logging.debug(f"This is response for: {session['user_name']}, {response.json()}")
#         if response.status_code ==200:
#             flag_group=True
#             break
#     if flag_group:
#        logging.debug(f"This user is a member: {session['user_name']}")
#        return True
#     else:
#         logging.debug(f"This user is not a member: {session['user_name']}")
#         return False


#        # user_group_ids = [''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30)) for _ in range(167)]
#       #  user_group_ids.append('e457b5c3-6590-4374-9f92-49a75eba03e4')
#       #  user_group_ids.append('312b0f8e-15a5-4a99-9252-78d8eaa49a02')
#         # print("these are user groups", user_groups)
#         # #print("------------------------------------------------------")
#         # logging.debug("these are user_group_ids", session['user_name'], user_group_ids)
#         # logging.debug(f"These are user_group_ids for {session['user_name']}: {user_group_ids}")
#         # Check if any of the user's groups are in the all_group_ids list
#        # all_group_ids.remove('312b0f8e-15a5-4a99-9252-78d8eaa49a02')
#     #     is_member = any(user_group_id in all_group_ids for user_group_id in user_group_ids)
#     #     #print("------------------------------------------------------")
#     #     logging.debug("these are all_group_ids", all_group_ids)
    
        
#     #     if is_member:
#     #         #print("User is a member of the parent group or one of its nested groups.")
#     #         logging.debug(f"This user is member: {session['user_name']}")
#     #         logging.debug(f"This user is member: {session['user_name']}")
#     #         return True
#     #     else:
#     #         #print("User is not a member of the parent group or any of its nested groups.")
#     #         logging.debug(f"This user is not member: {session['user_name']}")
#     #         logging.debug(f"This user is not member: {session['user_name']}")
#     #         return False
#     # else:
#     #     #print(f"Failed to retrieve user's groups: {response.text}")
#     #     logging.debug(f"This user is not a member of any group: {session['user_name']}")
    
            
        
#     #     logging.debug(f"This user is not a member of any group: {session['user_name']}")
    
            
        

# def get_group_members(group_id, headers):
#     #print('inside get_group_members')
#     # logging.debug(f'inside get_group_members: {group_id} and {headers}')
#     response = requests.get(
#         f"https://graph.microsoft.com/v1.0/groups/{group_id}/members", headers=headers)
    
#     if response.status_code == 200:
#         # logging.debug('inside get_group_members response as 200')
#         return response.json().get('value', [])
#     else:
#         # logging.debug('inside get_group_members no response')
#         ##print(f"Failed to retrieve members of group {group_id}: {response.text}")
#         return []

# def get_nested_group_ids(group_id, headers):
#   #  #print('inside get_nested_group_ids')
#     # logging.debug('inside get_nested_group_ids')
#     group_members = get_group_members(group_id, headers)
#     # logging.debug(f'inside get_nested_group_ids and group_members: {group_members}')
#     nested_group_ids = []

#     for member in group_members:
#       #  #print('inside for loop in get_nested_group_ids')
#         # logging.debug('inside for loop in get_nested_group_ids')
#         if member["@odata.type"] == "#microsoft.graph.group":
#             nested_group_id = member["id"]
#             nested_group_ids.append(nested_group_id)
#             nested_group_ids.extend(get_nested_group_ids(nested_group_id, headers))
#           #  #print('inside for loop in get_nested_group_ids', nested_group_ids)
#             # logging.debug(f'inside for loop in get_nested_group_ids: {nested_group_ids}')
#     return nested_group_ids
# # CODE ADDED FOR NESTED AD GROUPS AUTHORIZATION --ended 

# def is_mod_auth():
#     """
#     Check if the user is authorized to access the access the ChatDSI.
#     """
#     token_refresh()

#     tenant_id = os.getenv("AZURE_AUTH_TENNANT_ID")
#     client_id = os.getenv("AZURE_AUTH_CLIENT_ID")
#     client_secret = os.getenv("AZURE_AUTH_CLIENT_SECRET")

#     # Step 1: Acquire Access Token
#     token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
#     token_data = {
#         "grant_type": "client_credentials",
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "scope": "https://graph.microsoft.com/.default"
#     }

#     token_response = requests.post(token_url, data=token_data)
#     token_response.raise_for_status()
#     access_token2 = token_response.json().get("access_token")

#     headers = {  
#     'Authorization': 'Bearer ' + access_token2,  
#     'Content-Type': 'application/json'  
#     }


#     toggle_parent_group_id = 'cbecfcea-7f1b-4a7f-ad1f-28349e65c397'
#     toggle_all_group_ids = [toggle_parent_group_id]
#     # toggle_all_group_ids.append("312b0f8e-15a5-4a99-9252-78d8eaa49a02","e457b5c3-6590-4374-9f92-49a75eba03e4") #Comment before release
#     # toggle_all_group_ids.append("e457b5c3-6590-4374-9f92-49a75eba03e4")
#     toggle_all_group_ids.extend(get_nested_group_ids(toggle_parent_group_id, headers))                           #Uncomment before release

#     #print(toggle_all_group_ids)

#         #  group AOAI_KUMOAI_PowerUsers - cbecfcea-7f1b-4a7f-ad1f-28349e65c397 added 
#     # response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq 'cbecfcea-7f1b-4a7f-ad1f-28349e65c397'", headers=headers)  
#     # if response.status_code == 200: 
#     #     #print('success')
#     #     return True
#     # else:
#     #     return False

#     headers = {  
#      'Authorization': 'Bearer ' + session['access_token'],  
#      'Content-Type': 'application/json'  
#      }

#     flag_group = False
#     for toggle_all_group_id in toggle_all_group_ids:
#         response = requests.get(f"https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq '{toggle_all_group_id}'", headers=headers)
#         logging.debug(f"This is response for: {session['user_name']}, {response.json()}")
#         if response.status_code ==200:
#             flag_group=True
#             break
#     if flag_group:
#        logging.debug(f"This user is a member of power group: {session['user_name']}")
#        return True
#     else:
#         logging.debug(f"This user is not a member of power group: {session['user_name']}")
#         return False

#     # response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf", headers=headers)

#     # if response.status_code == 200:
#     #     user_groups = response.json().get('value', [])
#     #     user_group_ids = [group["id"] for group in user_groups]

#     #     # Check if any of the user's groups are in the all_group_ids list
#     #     is_member = any(user_group_id in toggle_all_group_ids for user_group_id in user_group_ids)

#     #     if is_member:
#     #         print("User is a member power users group")
#     #         return True
#     #     else:
#     #         print("User is not a member of the power users groups.")
#     #         return False
#     # else:
#     #     print(f"Failed to retrieve user's groups: {response.text}")

# # def mod_auth_list()->list:
# #     return []

# @bp.route('/api/auth',methods=['GET'])
# def isModAuth():
#     return jsonify({"hi , I am a dummy"}), 500
#     if is_auth():
#         if is_mod_auth():
#             return jsonify({"hasModAccess":True}),200
#         return jsonify({"hasModAccess":False}),200
#     return jsonify({"error": str("Unauthorized or session has expired. Please refresh the page to login again.")}), 401


#     # else:
#     #     return jsonify({"hasChatAccess":False,"hasDBAccess":False}),200
    
# # this is used to check powerusers for fileupload access
# # def isFileUploadAuth():
# #     if is_auth():
# #         if is_mod_auth():
# #             return jsonify({"hasFileUploadAccess":True}),200
# #         return jsonify({"hasFileUploadAccess":False}),200
# #     return jsonify({"error": str("Unauthorized or session has expired. Please refresh the page to login again.")}), 401

# # ADD error handling below
# @bp.route('/upload', methods=['POST'])
# async def upload():
#     return jsonify({"hi , I am a dummy"}), 500
#     try:
#     #     if "file" not in (await request.files):
#     #         print("no file")
#     #         return (jsonify({"error": "No file uploaded"})),400
#         files = await request.files
#         # Define a temporary directory to save the uploaded files
#         tempdir = "./tempfile"
#         # Ensure the temporary directory exists, create it if not
#         os.makedirs(os.path.join(tempdir, session['user_name']), exist_ok=True)

#         ## check if there is already csv/excel uploaded.
#         csv_excel_file_count = 0
#         folder_files = os.listdir(os.path.join(tempdir, session['user_name'])) 
#         # print(folder_files)
#         for file_name in folder_files:
#             # print(file_name)
#             if file_name.endswith(".csv") or file_name.endswith(".xlsx"):
#                 csv_excel_file_count += 1
#                 # print("here-------")
#                 return jsonify({"status" : 'delete csv_excel', "error" : "CSV/Excel already uploaded, Clear it to proceed"}), 250
#         # print(f'csv_excel_file_count : {csv_excel_file_count}')

#         file_count = 0
#         csv_excel_flag = False
#         for file in files:
#             # Print information about each file
#             file_count += 1
#             # print("file created", file)
#             # print(files[file].filename)
#             if (files[file].filename.endswith(".csv")) or (files[file].filename.endswith(".xlsx")):
#                 csv_excel_flag = True
#             if (csv_excel_flag == True) and (file_count > 1):
#                 if os.path.exists(os.path.join(tempdir, session['user_name'])):
#                     # print("removed directory if created")
#                     shutil.rmtree(os.path.join(tempdir, session['user_name']))
#                 return jsonify({"status" :'csv_excel_error', 'error' : "Upload single CSV/Excel file"}), 400
#             # print("directory_check")
#             # print(os.path.exists(os.path.join('vector_stored', session['user_name'])), "-------")
#             if (csv_excel_flag == True) and os.path.exists(os.path.join('vector_stored', session['user_name'])):
#                 return jsonify({"status" :"csv_excel_error", 'error' : "Delete already uploaded files, and try uploading."}), 260

#             tempath = os.path.join(tempdir, session['user_name'], files[file].filename)
#             # print("tempath created", tempath)
#             # print("File Saved", tempath)
#             await files[file].save(tempath)

#         # print(csv_excel_flag, "excel_csv_flag")
#         if not csv_excel_flag:
#             file_path_list = []
#             token_limit_crossed = False
#             max_token_limit = 100000
#             total_tokens = 0
#             files = os.listdir(os.path.join(tempdir, session['user_name']))           

#             for file_name in files:
#                 file_path = os.path.join(os.path.join(tempdir, session['user_name']), file_name)
#                 file_path_list.append(file_path)
#                 total_tokens = total_tokens + token_counter(file_path)
#                 # print("file_name", file_name, file_path, token_counter(file_path))
#                 if total_tokens > max_token_limit:
#                     token_limit_crossed = True
#                     # print("total_tokens_crossed_limit", total_tokens)
#                     shutil.rmtree(os.path.join(tempdir, session['user_name']))
#                     return jsonify({"status" :'file_limit_exceeds', 'error' : "Upload small size files, or try with few number of files"}), 500
            
#             # print(token_limit_crossed)
#             # print("total tokens", total_tokens)
#             if not token_limit_crossed:
#                 for i in file_path_list:
#                     vector_store = await create_vectorstore(file = i, user_name = session['user_name'])
#                     if os.path.exists(i):
#                         os.remove(i)
#                         # print("file_path deleted", i)
        
#         return jsonify({"status": "success"}), 200
#     except Exception as e:
#         return jsonify(status='try_after_some_time', error=str(e)), 600

# @bp.route('/delete-folder', methods=['DELETE'])  
# async def delete_folder():  
#     return jsonify({"hi , I am a dummy"}), 500
#     folder = "vector_stored"
#     folder_path = os.path.join(folder, session['user_name'])
#     # print('this is user_name:',  session['user_name'])
#     # print('thi is folder_path:', folder_path)
  
#     try:  
#         # Check if the folder is in use or locked 

#         if os.path.exists(os.path.join("tempfile", session['user_name'])):
#             await asyncio.get_event_loop().run_in_executor(None, shutil.rmtree, os.path.join("tempfile", session['user_name']))
        
#         if os.path.exists(os.path.join("temp_database", session['user_name'])):
#             # print("yes database folder")
#             await asyncio.get_event_loop().run_in_executor(None, shutil.rmtree, os.path.join("temp_database", session['user_name']))
#         else:
#             print("")

#         if not os.path.isdir(folder_path):  
#             return 'Folder does not exist', 404  
          
#         # Attempt to delete the folder asynchronously  
#         await asyncio.get_event_loop().run_in_executor(None, shutil.rmtree, folder_path)  
#         # print('folder deleted successfully')
#         return 'Folder deleted successfully', 200  
#     except Exception as e:  
#         # print(f"An error occurred: {e}")  
#         return 'An error occurred while deleting the folder', 500  
    


# @bp.route('/api/logout', methods=['POST'])  
# async def logout():  

#     # print(session['access_token'], 'session access token and ', session['user_name'], ' user name ')
#     return jsonify({"hi , I am a dummy"}), 500
#     if is_auth():
#         if is_kumo_auth():
#             # session.pop(session['user_name'], '')
#             session.clear()
#             pca = current_app.config[CONFIG_SSO]['pca']
#             auth_url = pca.get_authorization_request_url(
#             scopes=current_app.config[CONFIG_SSO]['scope'],
#             redirect_uri=current_app.config[CONFIG_SSO]['redirect_uri'],
#             prompt='select_account',  # Forces the user to select their account on each login attempt
#             state='random_state'  # Add a random state value to mitigate CSRF attacks
#             )
#             # session.pop(session['access_token'], None)
#             # print(session,'session access token present and ', ' user name cleared ')
               
#             return jsonify({"auth_url": auth_url}), 200
#         # render_template('401.html')
#     else:
#         return jsonify({"error": str("Unauthorized or session has expired. Please refresh the page to login again.")}), 401
        

# @bp.before_app_serving
# async def setup_clients():
#     return jsonify({"hi , I am a dummy"}), 500

#     #Azure OpenAI ENV Settings
#     AZURE_OPENAI_SERVICE = os.getenv("AZURE_OPENAI_SERVICE")
#     AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT")
#     AZURE_OPENAI_GPT4_DEPLOYMENT = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT")
#     AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

#     #Azure SSO ENV Settings
#     AZURE_AUTH_CLIENT_SECRET = os.getenv("AZURE_AUTH_CLIENT_SECRET")
#     AZURE_AUTH_TENNANT_ID = os.getenv("AZURE_AUTH_TENNANT_ID")
#     AZURE_AUTH_CLIENT_ID = os.getenv("AZURE_AUTH_CLIENT_ID")
#     AZURE_AUTH_REDIRECT_URI = os.getenv("AZURE_AUTH_REDIRECT_URI")
#     AZURE_AUTH_SCOPE = ["User.Read"]
#     AZURE_AUTH_AUTHORITY = 'https://login.microsoftonline.com/' + AZURE_AUTH_TENNANT_ID
#     AZURE_LOGGING_TABLE = os.getenv("AZURE_LOGGING_TABLE")
    
#     #Azure DB
#     AZURE_LOGGING_DB=os.getenv("AZURE_LOGGING_DB")
#     AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME=os.getenv("AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME")
#     AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD=os.getenv("AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD")
#     AZURE_LOGGING_SERVERNAME=os.getenv("AZURE_LOGGING_SERVERNAME")
#     AZURE_LOGGING_DRIVER=os.getenv("AZURE_LOGGING_DRIVER")

#     openai.api_type = "azure"
#     openai.api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com"
#     openai.api_version = "2024-02-01"
#     # openai_api_version = "2023-12-01-preview" 
#     openai.api_key = AZURE_OPENAI_API_KEY

#     current_app.config[CONFIG_SSO] = {
#         "pca": ConfidentialClientApplication(client_id=AZURE_AUTH_CLIENT_ID, authority=AZURE_AUTH_AUTHORITY,client_credential=AZURE_AUTH_CLIENT_SECRET),
#         "scope": AZURE_AUTH_SCOPE,
#         "redirect_uri":  AZURE_AUTH_REDIRECT_URI
#         }


#     current_app.config[CONFIG_CHAT_APPROACHES] = {
#         "general": GeneralAssistant(
#             AZURE_OPENAI_CHATGPT_DEPLOYMENT,
#             AZURE_OPENAI_GPT4_DEPLOYMENT
#         ),
       
#         "docqna": DocumentQnA(AZURE_OPENAI_CHATGPT_DEPLOYMENT,
#             AZURE_OPENAI_GPT4_DEPLOYMENT)
#     }

#     current_app.config[CONFIG_LOGGING] = {
#         "db": AZURE_LOGGING_DB,
#         "server": AZURE_LOGGING_SERVERNAME,
#         "username": AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME,
#         "password": AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD,
#         "driver": AZURE_LOGGING_DRIVER,
#         "table": AZURE_LOGGING_TABLE
#     }


# def create_app():
#     if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
#         configure_azure_monitor()
#         AioHttpClientInstrumentor().instrument()
    
#     APP_SECREAT_KEY = os.getenv("APP_SECREAT_KEY")
#     app = Quart(__name__)
#     app.secret_key = APP_SECREAT_KEY
#     app.permanent_session_lifetime = timedelta(minutes=720)
#     app.register_blueprint(bp)
#     #app.asgi_app = OpenTelemetryMiddleware(app.asgi_app)
#     # Level should be one of https://docs.python.org/3/library/logging.html#logging-levels
#     logging.basicConfig(level=os.getenv("APP_LOG_LEVEL", "DEBUG"))
#     #logging.basicConfig(level=os.getenv("APP_LOG_LEVEL", "DEBUG"))
#     return app
#import io
import json
import logging
# import mimetypes
import os
from typing import AsyncGenerator
import aiohttp
from aiohttp import web
import openai
import requests
import aioodbc
from datetime import datetime, timedelta
import time
import time
import asyncio
# from azure.identity.aio import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
# from azure.search.documents.aio import SearchClient
# from azure.storage.blob.aio import BlobServiceClient
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
import shutil
import shutil
# from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from quart import (
    Blueprint,
    Quart,
    redirect,
    url_for,
    current_app,
    jsonify,
    make_response,
    request,
    send_from_directory,
    session,
    render_template
)
from msal import ConfidentialClientApplication 
import tempfile
from dotenv import load_dotenv

#from approaches.chatreadretrieveread import ChatReadRetrieveReadApproach
from approaches.generalAssistant import GeneralAssistant
from approaches.documentQnA import DocumentQnA
from core.vector_store import create_vectorstore
from core.token_count import token_counter
from approaches.documentQnA import DocumentQnA
from core.vector_store import create_vectorstore
from core.token_count import token_counter

#Load environment file
ENV_FILE = os.getenv("ENV_FILE") or ".env_local"
load_dotenv(ENV_FILE)


CONFIG_SSO = "azure_sso"
CONFIG_CHAT_APPROACHES = "chat_approaches"
CONFIG_LOGGING = "logging_config"
#CONFIG_BLOB_CONTAINER_CLIENT = "blob_container_client"

bp = Blueprint("routes", __name__, static_folder="static")

vector_db = {}
vector_db = {}

@bp.route("/")
@bp.route("/<path:path>")
async def index():
    """
    Serve the 'index.html' file as a static resource.
    """
    
    if is_auth():
        if is_kumo_auth():
            return await bp.send_static_file("index.html")
        else:
            return await render_template('401.html')
    elif 'code' in request.args:
        code = request.args.get('code')
        pca = current_app.config[CONFIG_SSO]['pca']
        auth_code = pca.acquire_token_by_authorization_code(code,scopes=current_app.config[CONFIG_SSO]['scope'],redirect_uri=current_app.config[CONFIG_SSO]['redirect_uri'])
        if 'error' in auth_code:
            # Handle error case
            return 'Error: ' + auth_code['error']
        
        user_name = auth_code['id_token_claims']['preferred_username']
        #user_name = 'gnosti@dsi.com'
        #user_name = 'gnosti@dsi.com'
        name = auth_code['id_token_claims']['name']
        session['access_token'] = auth_code['access_token']
        session['refresh_token'] = auth_code['refresh_token']
        session['expire_time'] = datetime.now() + timedelta(seconds=auth_code['expires_in'])
        #session['expire_time'] = datetime.now() + timedelta(seconds=60)
        session['user_name'] = user_name
        # session['user_name'] = "akurapa@dsi.com"
        logging.debug(f"this is auth_code for: {session['user_name']}; {auth_code}")
        #print(session['user_name'], "user_name")
        response = redirect(url_for('routes.index'))
        response.set_cookie('username', name)
        return response
    else:
        pca = current_app.config[CONFIG_SSO]['pca']
        auth_url = pca.get_authorization_request_url(
        scopes=current_app.config[CONFIG_SSO]['scope'],
        redirect_uri=current_app.config[CONFIG_SSO]['redirect_uri'],
        prompt='select_account',  # Forces the user to select their account on each login attempt
        state='random_state'  # Add a random state value to mitigate CSRF attacks
    )
        return redirect(auth_url)
    
    return "Some Error Occured"
    


@bp.route("/favicon.ico")
async def favicon():
    """
    Serve the app icon file as a static resource.
    """
    return await bp.send_static_file("favicon.ico")


@bp.route("/assets/<path:path>")
async def assets(path):
    """
    Serve the static javscript assest file as a static resource.
    """
    return await send_from_directory("static/assets", path)


@bp.route("/chat", methods=["POST"])
async def chat():
    if not request.is_json:
        return jsonify({"error": "request must be json"}), 415
    request_json = await request.get_json()
    approach = request_json["approach"]
    #session['user_name'] = 'gnosti@dsi.com'
   # user_name = 'gnosti@dsi.com'
    #session['user_name'] = 'gnosti@dsi.com'
   # user_name = 'gnosti@dsi.com'
    try:
        impl = current_app.config[CONFIG_CHAT_APPROACHES].get(approach)
        if not impl:
            return jsonify({"error": "unknown approach"}), 400
        # Workaround for: https://github.com/openai/openai-python/issues/371
        async with aiohttp.ClientSession() as s:
            openai.aiosession.set(s)
            r = await impl.run_without_streaming(request_json["history"], request_json.get("overrides", {}), user_name= session['user_name'])
            #r = await impl.run_without_streaming(request_json["history"], request_json.get("overrides", {}))
            #print("run_without_streaming in app.py", r)
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /chat")
        return jsonify({"error": str(e)}), 500


async def format_as_ndjson(r: AsyncGenerator[dict, None]) -> AsyncGenerator[str, None]:
    """
    Format a stream of dictionaries as NDJSON (Newline-Delimited JSON).

    This function takes an asynchronous generator of dictionaries as input and yields
    NDJSON strings. Each dictionary is converted to a JSON string and terminated with
    a newline character. This is used for streaming.
    """
    async for event in r:
        yield json.dumps(event, ensure_ascii=False) + "\n"


@bp.route("/chat_stream", methods=["POST"])
async def chat_stream():
    if is_auth():
        if not request.is_json:
            return jsonify({"error": "request must be json"}), 415
        request_json = await request.get_json()
        approach = request_json["approach"]
      #  session['user_name'] = 'gnosti@dsi.com'
      #  user_name = 'gnosti@dsi.com'
      #  session['user_name'] = 'gnosti@dsi.com'
      #  user_name = 'gnosti@dsi.com'
        request_timestamp = datetime.now()
        try:
            impl = current_app.config[CONFIG_CHAT_APPROACHES].get(approach)
            if not impl:
                return jsonify({"error": "unknown approach"}), 400
            #print(vector_db[session["user_name"]])
            response_generator = impl.run_with_streaming(request_json["history"], request_json.get("overrides", {}), user_name= session['user_name'])
            #response_generator = impl.run_with_streaming(request_json["history"], request_json.get("overrides", {}),session['user_name'])
            response = await make_response(format_as_ndjson(response_generator))
            response.timeout = None  # type: ignore
            # # await log_api_response(input_timestamp=request_timestamp,api='ai-gen',approach=approach )
            return response
        except Exception as e:
            logging.exception("Exception in /chat")
            return jsonify({"error": str(e)}), 500
    else:
        #print("Error unauth")
        return jsonify({"error": str("Unauthorized or session has expired. Please refresh the page to login again.")}), 401

  

  

# @bp.before_request
# async def ensure_openai_token():
#     if openai.api_type != "azure_ad":
#         return
#     openai_token = current_app.config[CONFIG_OPENAI_TOKEN]
#     if openai_token.expires_on < time.time() + 60:
#         openai_token = await current_app.config[CONFIG_CREDENTIAL].get_token(
#             "https://cognitiveservices.azure.com/.default"
#         )
#         current_app.config[CONFIG_OPENAI_TOKEN] = openai_token
#         openai.api_key = openai_token.token

# async def log_api_response(input_timestamp, api,approach):
#     """
#     Log request to the database
#     """
#     config = current_app.config[CONFIG_LOGGING]
#     user = session['user_name']
#     current_timestamp = datetime.now()
#     resp_time = current_timestamp - input_timestamp
#     model_name = "gpt-3.5"
#     logging_conn_string = f"DRIVER={config['driver']};SERVER=tcp:{config['server']};DATABASE={config['db']};UID={config['username']};PWD={config['password']};Authentication=ActiveDirectoryPassword"
#     query = f"""INSERT INTO LOGGING.{config['table']} (APPLN, LOG_DT_TM, USR_NM, RESP_DT_TM, model_name, RESP_TM_SEC) VALUES (?, ?, ?, ?, ?, ?) """
#     params = (api, input_timestamp, user, current_timestamp, model_name, resp_time.seconds)
#     try:
#         conn = await aioodbc.connect(dsn=logging_conn_string)
#         cursor = await conn.cursor()
#         print("DB Connection Success")
#         await cursor.execute(query,params)
#         await conn.commit()
#         await cursor.close()
#         await conn.close()
#     except Exception as e:
#         print(str(e))
#         logging.exception("Exception in logging - ",str(e) )


async def token_c(response):
    print(await response.get_data())


def is_auth() -> bool:
    """
    Checks if user is authenticated and session data exists in Quart Session
    """
    if 'access_token' in session:
        return True
    else:
        return False

def token_refresh():
    if datetime.now() > session['expire_time']:
        pca = current_app.config[CONFIG_SSO]['pca']
        refresh_token = session['refresh_token']
        scope = current_app.config[CONFIG_SSO]['scope']
        new_token = pca.acquire_token_by_refresh_token(refresh_token, scopes=scope)
        session['access_token'] = new_token['access_token']
        session['refresh_token'] = new_token['refresh_token']
        session['expire_time'] = datetime.now() + timedelta(seconds=new_token['expires_in'])
        #session['expire_time'] = datetime.now() + timedelta(seconds=60)


def is_kumo_auth():
    """
    Check if the user is authorized to access the access the ChatDSI.
    """
    token_refresh()
    # headers = {  
    # 'Authorization': 'Bearer ' + session['access_token'],  
    # 'Content-Type': 'application/json'  
    # }
    # response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq 'e457b5c3-6590-4374-9f92-49a75eba03e4'", headers=headers)  
    # response2 = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq '312b0f8e-15a5-4a99-9252-78d8eaa49a02'", headers=headers)  
    # if response.status_code == 200 or response2.status_code == 200: 
    #     ##print('success')
    #     return True
    # else:
    #     return False

# CODE ADDED FOR NESTED AD GROUPS AUTHORIZATION --started

    tenant_id = os.getenv("AZURE_AUTH_TENNANT_ID")
    client_id = os.getenv("AZURE_AUTH_CLIENT_ID")
    client_secret = os.getenv("AZURE_AUTH_CLIENT_SECRET")
    parent_group_id = "e457b5c3-6590-4374-9f92-49a75eba03e4"


    #Acquire Access Token to read groups
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }

    token_response = requests.post(token_url, data=token_data)
    token_response.raise_for_status()
    access_token2 = token_response.json().get("access_token")

    headers = {  
    'Authorization': 'Bearer ' + access_token2,  
    'Content-Type': 'application/json'  
    }

    all_group_ids = [parent_group_id]
    # all_group_ids.append("312b0f8e-15a5-4a99-9252-78d8eaa49a02")       #comment before release
    all_group_ids.extend(get_nested_group_ids(parent_group_id, headers)) #uncomment before release
    #print("all_group_ids: ",all_group_ids)

    headers = {  
     'Authorization': 'Bearer ' + session['access_token'],  
     'Content-Type': 'application/json'  
     }

    # response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$top=999", headers=headers)
    # logging.debug(f"this is response for {session['user_name']}: {response.json()}")
    # if response.status_code == 200:
    #     user_groups = response.json().get('value', [])
    #     user_group_ids = [group["id"] for group in user_groups]

    flag_group = False
    for all_group_id in all_group_ids:
        response = requests.get(f"https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq '{all_group_id}'", headers=headers)
        logging.debug(f"This is response for: {session['user_name']}, {response.json()}")
        if response.status_code ==200:
            flag_group=True
            break
    if flag_group:
       logging.debug(f"This user is a member: {session['user_name']}")
       return True
    else:
        logging.debug(f"This user is not a member: {session['user_name']}")
        return False


       # user_group_ids = [''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30)) for _ in range(167)]
      #  user_group_ids.append('e457b5c3-6590-4374-9f92-49a75eba03e4')
      #  user_group_ids.append('312b0f8e-15a5-4a99-9252-78d8eaa49a02')
        # print("these are user groups", user_groups)
        # #print("------------------------------------------------------")
        # logging.debug("these are user_group_ids", session['user_name'], user_group_ids)
        # logging.debug(f"These are user_group_ids for {session['user_name']}: {user_group_ids}")
        # Check if any of the user's groups are in the all_group_ids list
       # all_group_ids.remove('312b0f8e-15a5-4a99-9252-78d8eaa49a02')
    #     is_member = any(user_group_id in all_group_ids for user_group_id in user_group_ids)
    #     #print("------------------------------------------------------")
    #     logging.debug("these are all_group_ids", all_group_ids)
    
        
    #     if is_member:
    #         #print("User is a member of the parent group or one of its nested groups.")
    #         logging.debug(f"This user is member: {session['user_name']}")
    #         logging.debug(f"This user is member: {session['user_name']}")
    #         return True
    #     else:
    #         #print("User is not a member of the parent group or any of its nested groups.")
    #         logging.debug(f"This user is not member: {session['user_name']}")
    #         logging.debug(f"This user is not member: {session['user_name']}")
    #         return False
    # else:
    #     #print(f"Failed to retrieve user's groups: {response.text}")
    #     logging.debug(f"This user is not a member of any group: {session['user_name']}")
    
            
        
    #     logging.debug(f"This user is not a member of any group: {session['user_name']}")
    
            
        

def get_group_members(group_id, headers):
    #print('inside get_group_members')
    # logging.debug(f'inside get_group_members: {group_id} and {headers}')
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/groups/{group_id}/members", headers=headers)
    
    if response.status_code == 200:
        # logging.debug('inside get_group_members response as 200')
        return response.json().get('value', [])
    else:
        # logging.debug('inside get_group_members no response')
        ##print(f"Failed to retrieve members of group {group_id}: {response.text}")
        return []

def get_nested_group_ids(group_id, headers):
  #  #print('inside get_nested_group_ids')
    # logging.debug('inside get_nested_group_ids')
    group_members = get_group_members(group_id, headers)
    # logging.debug(f'inside get_nested_group_ids and group_members: {group_members}')
    nested_group_ids = []

    for member in group_members:
      #  #print('inside for loop in get_nested_group_ids')
        # logging.debug('inside for loop in get_nested_group_ids')
        if member["@odata.type"] == "#microsoft.graph.group":
            nested_group_id = member["id"]
            nested_group_ids.append(nested_group_id)
            nested_group_ids.extend(get_nested_group_ids(nested_group_id, headers))
          #  #print('inside for loop in get_nested_group_ids', nested_group_ids)
            # logging.debug(f'inside for loop in get_nested_group_ids: {nested_group_ids}')
    return nested_group_ids
# CODE ADDED FOR NESTED AD GROUPS AUTHORIZATION --ended 

def is_mod_auth():
    """
    Check if the user is authorized to access the access the ChatDSI.
    """
    token_refresh()

    tenant_id = os.getenv("AZURE_AUTH_TENNANT_ID")
    client_id = os.getenv("AZURE_AUTH_CLIENT_ID")
    client_secret = os.getenv("AZURE_AUTH_CLIENT_SECRET")

    # Step 1: Acquire Access Token
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }

    token_response = requests.post(token_url, data=token_data)
    token_response.raise_for_status()
    access_token2 = token_response.json().get("access_token")

    headers = {  
    'Authorization': 'Bearer ' + access_token2,  
    'Content-Type': 'application/json'  
    }


    toggle_parent_group_id = 'cbecfcea-7f1b-4a7f-ad1f-28349e65c397'
    toggle_all_group_ids = [toggle_parent_group_id]
    # toggle_all_group_ids.append("312b0f8e-15a5-4a99-9252-78d8eaa49a02","e457b5c3-6590-4374-9f92-49a75eba03e4") #Comment before release
    # toggle_all_group_ids.append("e457b5c3-6590-4374-9f92-49a75eba03e4")
    toggle_all_group_ids.extend(get_nested_group_ids(toggle_parent_group_id, headers))                           #Uncomment before release

    #print(toggle_all_group_ids)

        #  group AOAI_KUMOAI_PowerUsers - cbecfcea-7f1b-4a7f-ad1f-28349e65c397 added 
    # response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq 'cbecfcea-7f1b-4a7f-ad1f-28349e65c397'", headers=headers)  
    # if response.status_code == 200: 
    #     #print('success')
    #     return True
    # else:
    #     return False

    headers = {  
     'Authorization': 'Bearer ' + session['access_token'],  
     'Content-Type': 'application/json'  
     }

    flag_group = False
    for toggle_all_group_id in toggle_all_group_ids:
        response = requests.get(f"https://graph.microsoft.com/v1.0/me/memberOf?$filter=id eq '{toggle_all_group_id}'", headers=headers)
        logging.debug(f"This is response for: {session['user_name']}, {response.json()}")
        if response.status_code ==200:
            flag_group=True
            break
    if flag_group:
       logging.debug(f"This user is a member of power group: {session['user_name']}")
       return True
    else:
        logging.debug(f"This user is not a member of power group: {session['user_name']}")
        return False

    # response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf", headers=headers)

    # if response.status_code == 200:
    #     user_groups = response.json().get('value', [])
    #     user_group_ids = [group["id"] for group in user_groups]

    #     # Check if any of the user's groups are in the all_group_ids list
    #     is_member = any(user_group_id in toggle_all_group_ids for user_group_id in user_group_ids)

    #     if is_member:
    #         print("User is a member power users group")
    #         return True
    #     else:
    #         print("User is not a member of the power users groups.")
    #         return False
    # else:
    #     print(f"Failed to retrieve user's groups: {response.text}")

# def mod_auth_list()->list:
#     return []

@bp.route('/api/auth',methods=['GET'])
def isModAuth():
    if is_auth():
        if is_mod_auth():
            return jsonify({"hasModAccess":True}),200
        return jsonify({"hasModAccess":False}),200
    return jsonify({"error": str("Unauthorized or session has expired. Please refresh the page to login again.")}), 401


    # else:
    #     return jsonify({"hasChatAccess":False,"hasDBAccess":False}),200
    
# this is used to check powerusers for fileupload access
# def isFileUploadAuth():
#     if is_auth():
#         if is_mod_auth():
#             return jsonify({"hasFileUploadAccess":True}),200
#         return jsonify({"hasFileUploadAccess":False}),200
#     return jsonify({"error": str("Unauthorized or session has expired. Please refresh the page to login again.")}), 401

# ADD error handling below
@bp.route('/upload', methods=['POST'])
async def upload():
    try:
    #     if "file" not in (await request.files):
    #         print("no file")
    #         return (jsonify({"error": "No file uploaded"})),400
        files = await request.files
        # Define a temporary directory to save the uploaded files
        tempdir = "./tempfile"
        # Ensure the temporary directory exists, create it if not
        os.makedirs(os.path.join(tempdir, session['user_name']), exist_ok=True)

        ## check if there is already csv/excel uploaded.
        csv_excel_file_count = 0
        folder_files = os.listdir(os.path.join(tempdir, session['user_name'])) 
        # print(folder_files)
        for file_name in folder_files:
            # print(file_name)
            if file_name.endswith(".csv") or file_name.endswith(".xlsx"):
                csv_excel_file_count += 1
                # print("here-------")
                return jsonify({"status" : 'delete csv_excel', "error" : "CSV/Excel already uploaded, Clear it to proceed"}), 250
        # print(f'csv_excel_file_count : {csv_excel_file_count}')

        file_count = 0
        csv_excel_flag = False
        for file in files:
            # Print information about each file
            file_count += 1
            # print("file created", file)
            # print(files[file].filename)
            if (files[file].filename.endswith(".csv")) or (files[file].filename.endswith(".xlsx")):
                csv_excel_flag = True
            if (csv_excel_flag == True) and (file_count > 1):
                if os.path.exists(os.path.join(tempdir, session['user_name'])):
                    # print("removed directory if created")
                    shutil.rmtree(os.path.join(tempdir, session['user_name']))
                return jsonify({"status" :'csv_excel_error', 'error' : "Upload single CSV/Excel file"}), 400
            # print("directory_check")
            # print(os.path.exists(os.path.join('vector_stored', session['user_name'])), "-------")
            if (csv_excel_flag == True) and os.path.exists(os.path.join('vector_stored', session['user_name'])):
                return jsonify({"status" :"csv_excel_error", 'error' : "Delete already uploaded files, and try uploading."}), 260

            tempath = os.path.join(tempdir, session['user_name'], files[file].filename)
            # print("tempath created", tempath)
            # print("File Saved", tempath)
            await files[file].save(tempath)

        # print(csv_excel_flag, "excel_csv_flag")
        if not csv_excel_flag:
            file_path_list = []
            token_limit_crossed = False
            max_token_limit = 100000
            total_tokens = 0
            files = os.listdir(os.path.join(tempdir, session['user_name']))           

            for file_name in files:
                file_path = os.path.join(os.path.join(tempdir, session['user_name']), file_name)
                file_path_list.append(file_path)
                total_tokens = total_tokens + token_counter(file_path)
                # print("file_name", file_name, file_path, token_counter(file_path))
                if total_tokens > max_token_limit:
                    token_limit_crossed = True
                    # print("total_tokens_crossed_limit", total_tokens)
                    shutil.rmtree(os.path.join(tempdir, session['user_name']))
                    return jsonify({"status" :'file_limit_exceeds', 'error' : "Upload small size files, or try with few number of files"}), 500
            
            # print(token_limit_crossed)
            # print("total tokens", total_tokens)
            if not token_limit_crossed:
                for i in file_path_list:
                    vector_store = await create_vectorstore(file = i, user_name = session['user_name'])
                    if os.path.exists(i):
                        os.remove(i)
                        # print("file_path deleted", i)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify(status='try_after_some_time', error=str(e)), 600

@bp.route('/delete-folder', methods=['DELETE'])  
async def delete_folder():  
    folder = "vector_stored"
    folder_path = os.path.join(folder, session['user_name'])
    # print('this is user_name:',  session['user_name'])
    # print('thi is folder_path:', folder_path)
  
    try:  
        # Check if the folder is in use or locked 

        if os.path.exists(os.path.join("tempfile", session['user_name'])):
            await asyncio.get_event_loop().run_in_executor(None, shutil.rmtree, os.path.join("tempfile", session['user_name']))
        
        if os.path.exists(os.path.join("temp_database", session['user_name'])):
            # print("yes database folder")
            await asyncio.get_event_loop().run_in_executor(None, shutil.rmtree, os.path.join("temp_database", session['user_name']))
        else:
            print("")

        if not os.path.isdir(folder_path):  
            return 'Folder does not exist', 404  
          
        # Attempt to delete the folder asynchronously  
        await asyncio.get_event_loop().run_in_executor(None, shutil.rmtree, folder_path)  
        # print('folder deleted successfully')
        return 'Folder deleted successfully', 200  
    except Exception as e:  
        # print(f"An error occurred: {e}")  
        return 'An error occurred while deleting the folder', 500  
    


@bp.route('/api/logout', methods=['POST'])  
async def logout():  

    # print(session['access_token'], 'session access token and ', session['user_name'], ' user name ')

    if is_auth():
        if is_kumo_auth():
            # session.pop(session['user_name'], '')
            session.clear()
            pca = current_app.config[CONFIG_SSO]['pca']
            auth_url = pca.get_authorization_request_url(
            scopes=current_app.config[CONFIG_SSO]['scope'],
            redirect_uri=current_app.config[CONFIG_SSO]['redirect_uri'],
            prompt='select_account',  # Forces the user to select their account on each login attempt
            state='random_state'  # Add a random state value to mitigate CSRF attacks
            )
            # session.pop(session['access_token'], None)
            # print(session,'session access token present and ', ' user name cleared ')
               
            return jsonify({"auth_url": auth_url}), 200
        # render_template('401.html')
    else:
        return jsonify({"error": str("Unauthorized or session has expired. Please refresh the page to login again.")}), 401
        

@bp.before_app_serving
async def setup_clients():

    #Azure OpenAI ENV Settings
    AZURE_OPENAI_SERVICE = os.getenv("AZURE_OPENAI_SERVICE")
    AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT")
    AZURE_OPENAI_GPT4_DEPLOYMENT = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

    #Azure SSO ENV Settings
    AZURE_AUTH_CLIENT_SECRET = os.getenv("AZURE_AUTH_CLIENT_SECRET")
    AZURE_AUTH_TENNANT_ID = os.getenv("AZURE_AUTH_TENNANT_ID")
    AZURE_AUTH_CLIENT_ID = os.getenv("AZURE_AUTH_CLIENT_ID")
    AZURE_AUTH_REDIRECT_URI = os.getenv("AZURE_AUTH_REDIRECT_URI")
    AZURE_AUTH_SCOPE = ["User.Read"]
    AZURE_AUTH_AUTHORITY = 'https://login.microsoftonline.com/' + AZURE_AUTH_TENNANT_ID
    AZURE_LOGGING_TABLE = os.getenv("AZURE_LOGGING_TABLE")
    
    #Azure DB
    AZURE_LOGGING_DB=os.getenv("AZURE_LOGGING_DB")
    AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME=os.getenv("AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME")
    AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD=os.getenv("AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD")
    AZURE_LOGGING_SERVERNAME=os.getenv("AZURE_LOGGING_SERVERNAME")
    AZURE_LOGGING_DRIVER=os.getenv("AZURE_LOGGING_DRIVER")

    openai.api_type = "azure"
    openai.api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com"
    openai.api_version = "2024-02-01"
    # openai_api_version = "2023-12-01-preview" 
    openai.api_key = AZURE_OPENAI_API_KEY

    current_app.config[CONFIG_SSO] = {
        "pca": ConfidentialClientApplication(client_id=AZURE_AUTH_CLIENT_ID, authority=AZURE_AUTH_AUTHORITY,client_credential=AZURE_AUTH_CLIENT_SECRET),
        "scope": AZURE_AUTH_SCOPE,
        "redirect_uri":  AZURE_AUTH_REDIRECT_URI
        }


    current_app.config[CONFIG_CHAT_APPROACHES] = {
        "general": GeneralAssistant(
            AZURE_OPENAI_CHATGPT_DEPLOYMENT,
            AZURE_OPENAI_GPT4_DEPLOYMENT
        ),
       
        "docqna": DocumentQnA(AZURE_OPENAI_CHATGPT_DEPLOYMENT,
            AZURE_OPENAI_GPT4_DEPLOYMENT)
    }

    current_app.config[CONFIG_LOGGING] = {
        "db": AZURE_LOGGING_DB,
        "server": AZURE_LOGGING_SERVERNAME,
        "username": AZURE_LOGGING_SERVICE_ACCOUNT_USERNAME,
        "password": AZURE_LOGGING_SERVICE_ACCOUNT_PASSWORD,
        "driver": AZURE_LOGGING_DRIVER,
        "table": AZURE_LOGGING_TABLE
    }


def create_app():
    if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        configure_azure_monitor()
        AioHttpClientInstrumentor().instrument()
    
    APP_SECREAT_KEY = os.getenv("APP_SECREAT_KEY")
    app = Quart(__name__)
    app.secret_key = APP_SECREAT_KEY
    app.permanent_session_lifetime = timedelta(minutes=720)
    app.register_blueprint(bp)
    #app.asgi_app = OpenTelemetryMiddleware(app.asgi_app)
    # Level should be one of https://docs.python.org/3/library/logging.html#logging-levels
    logging.basicConfig(level=os.getenv("APP_LOG_LEVEL", "DEBUG"))
    #logging.basicConfig(level=os.getenv("APP_LOG_LEVEL", "DEBUG"))
    return app
