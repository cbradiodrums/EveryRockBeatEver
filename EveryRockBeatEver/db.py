from flask import current_app
import os
import json
import boto3
import botocore
import logging
from copy import deepcopy


def get_s3(client: any = 'client'):
    """ Connect to the application's cloud database. Configure in dotenv. """

    if current_app.config["APP_CONTEXT"] != 'LOCAL':
        # Client Side
        if client == 'client':
            session = boto3.session.Session()
            s3 = session.client(
                's3', endpoint_url=current_app.config["CLOUD_SERVER"],
                config=botocore.config.Config(signature_version='s3v4'),
                region_name=current_app.config["CLOUD_REGION"],
                aws_access_key_id=current_app.config["CLOUD_SECRET_ID"],
                aws_secret_access_key=current_app.config["CLOUD_SECRET_KEY"]
            )
        # Resource Side
        else:
            s3 = boto3.resource(
                's3', endpoint_url=current_app.config["CLOUD_SERVER"],
                config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                region_name=current_app.config["CLOUD_REGION"],
                aws_access_key_id=current_app.config["CLOUD_SECRET_ID"],
                aws_secret_access_key=current_app.config["CLOUD_SECRET_KEY"]
            )
    else:
        s3 = None
    return s3


def legal_file(USER_PRESETS: dict = None, task: str = '', template_id: str = None,
               file_type: str = '', tmp_file: str = '', session_id: str = None,
               json_content: any = None):
    """ Manipulate a Legal File within parameters specified
        IN: (Parsed) USER_PRESETS, (Parsed) USER_TEMPLATE
            task (SAVE/LOAD), file_type (LOG/USER_PRESETS/MIDI)
        FUNCTION: task[SAVE/LOAD/LOG/DOWNLOAD] -> location(s) [LOCAL/CLOUD]
         OUT: SAVE (null), LOAD (FILE_OBJECT) """

    # Determine the USER -- current session / template
    # session_id, template_id = USER_PRESETS['session_id'], USER_PRESETS['template_id']
    USER_PRESETS_COPY = deepcopy(USER_PRESETS)
    if USER_PRESETS:
        if session_id:
            USER_PRESETS_COPY['session_id'] = session_id
        if template_id:
            USER_PRESETS_COPY['template_id'] = template_id

    # Determine the File Type and FILE / Directory Naming Scheme
    if file_type == 'LOG':
        ROOT, KEY, FILE = f'usr_{session_id}', 'logs', f'log_{session_id}.txt'

    elif file_type == 'USER_PRESETS':
        # template_id = USER+PRESETS_COPY['template_id']
        ROOT, KEY, FILE = f'usr_{session_id}', 'user_presets', f'preset_{template_id}.json'

    elif file_type == 'USER_TEMPLATE':
        # template_id = USER+PRESETS_COPY['template_id']
        ROOT, KEY, FILE = f'usr_{session_id}', 'user_presets', f'template_{template_id}.json'

    elif file_type == 'MIDI':
        USER_PRESETS_COPY['template_id'] = template_id
        ROOT, KEY, FILE = f'usr_{session_id}', 'MIDI_files', f'MIDI_{template_id}.mid'

    else:
        ROOT, KEY, FILE = None, None, None
    print(ROOT, KEY, FILE)

    # Local Instance -- If Cloud, SKIP
    if current_app.config["APP_CONTEXT"] != 'CLOUD' or file_type in ['LOG']:
        # print(f'\n{current_app.instance_path}/users/usr_{session_id}/{KEY}')
        # print(f'{current_app.instance_path}/users/{ROOT}/{KEY}/{FILE}\n')

        # Determine if the Directory needs to be created
        # print(os.listdir(f'{current_app.instance_path}'))
        if f'users' not in os.listdir(f'{current_app.instance_path}'):
            os.makedirs(f'{current_app.instance_path}/users/')
        # print(os.listdir(f'{current_app.instance_path}/users/'))
        if f'usr_{session_id}' not in os.listdir(f'{current_app.instance_path}/users/'):
            os.makedirs(f'{current_app.instance_path}/users/usr_{session_id}/')
        # print(os.listdir(f'{current_app.instance_path}/users/usr_{session_id}'))
        if KEY not in os.listdir(f'{current_app.instance_path}/users/usr_{session_id}'):
            os.makedirs(f'{current_app.instance_path}/users/usr_{session_id}/{KEY}')

        # Determine what to do with the File
        file_path = f'{current_app.instance_path}/users/{ROOT}/{KEY}/{FILE}'
        if task == 'SAVE':

            if FILE[-4:] == 'json':
                with open(file_path, 'w') as f:
                    json.dump(USER_PRESETS_COPY, f)

            elif FILE[-4:] == '.txt':
                print(f'Save log here: {file_path}')
                with open(file_path, 'a') as f:
                    f.write('{{{--- LOG FILE UPDATED **LOCALLY** (SAVED) ---}}}\n')

            elif FILE[-4:] == '.mid':
                with open(tmp_file, 'rb') as f:
                    tmp_MIDI = f.read()
                with open(file_path, 'wb') as f:
                    f.write(tmp_MIDI)

        elif task == 'LOAD':

            if FILE[-4:] == 'json':
                with open(file_path) as f:
                    FILE = json.load(f)
                return FILE

            elif FILE[-4:] == '.txt' or file_type == 'LOG':
                print(f'LOAD Log Object here: {file_path}')
                LOGGER = logging.getLogger(file_path)
                return LOGGER

        elif task == 'LOG':
            file_path = f'{current_app.instance_path}/users/{ROOT}/{KEY}/{FILE}'
            print(f'Instantiate Logging Object and Return Here: {file_path}')
            LOGGER = logging.getLogger(file_path)
            LOGGER.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler(file_path)
            fh.setFormatter(formatter)
            LOGGER.addHandler(fh)

            return LOGGER

    # Cloud Connection ( if applicable )
    client, resource = get_s3(), get_s3('resource')

    if client and resource:
        BUCKET = current_app.config["CLOUD_BUCKET"]
        file_path = f'users/{ROOT}/{KEY}/{FILE}'
        bucket_contents = resource.Bucket(BUCKET).objects.all()
        bucket_keys = [bk.key for bk in bucket_contents]
        # print(f'{bucket_contents}\n{bucket_keys}')

        # Determine what to do with the File
        if task == 'SAVE':
            print(FILE)
            if FILE[-4:] == '.txt':
                if file_path not in bucket_keys:
                    client.put_object(Body=b'Cloud Logfile Instantiated', Bucket=BUCKET, Key=file_path)

            elif FILE[-4:] == 'json':
                if file_type == 'USER_PRESETS':
                    client.put_object(Body=json.dumps(USER_PRESETS_COPY), Bucket=BUCKET, Key=file_path)

            elif FILE[-4:] == '.mid':
                MIDI_filepath = f'users/{ROOT}/temp_MIDI_File.mid'
                print(file_path)
                with open(tmp_file, 'rb') as f:
                    tmp_MIDI = f.read()
                client.put_object(Body=tmp_MIDI, Bucket=BUCKET, Key=file_path)

        elif task == 'LOAD':
            if FILE[-4:] == '.txt':
                ...
            elif file_type == 'USER_PRESETS':
                content_object = resource.Object(BUCKET, file_path)
                file_content = content_object.get()['Body'].read().decode('utf-8')
                json_content = json.loads(file_content)
            return json_content

        elif task == 'DOWNLOAD' and file_type != 'LOG':
            url = client.generate_presigned_url('get_object',
                                                Params={'Bucket': BUCKET, 'Key': file_path},
                                                ExpiresIn=60)
            return url

        elif task == 'LOG':
            ...
            # content_object = resource.Object(BUCKET, file_path)
            # print(content_object)
            # file_content = content_object.get()['Body'].read().decode('utf-8')
            # print(file_content)
            # LOGGER = logging.getLogger(f'{session_id}')
            # LOGGER.setLevel(logging.DEBUG)
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # fh = logging.FileHandler(f'{session_id}')
            # fh.setFormatter(formatter)
            # LOGGER.addHandler(fh)
            #
            # return LOGGER


def check_file_duplicates(UPLOAD_FOLDER_TYPE: str, UPLOAD_FOLDER: str, UPLOAD_FOLDER_KEY: str,
                          base_filename: str, file_type: str, client_resource: any):
    """ Function that checks for file duplicates """

    # If APP Deployed Online, else if it was Deployed Locally
    if UPLOAD_FOLDER_TYPE == 'CLOUD':
        bucket_keys = client_resource.Bucket(UPLOAD_FOLDER).objects.all()
        last_file = [lf.key for lf in bucket_keys]
    else:
        last_file = os.listdir(f'{UPLOAD_FOLDER}{UPLOAD_FOLDER_KEY}')

    # Search Filename in Last File List and change it until it is no longer a duplicate (if applicable)
    file_name, file_number = f"{base_filename}{file_type}", -1
    while file_name in last_file:
        file_number += 1  # Should eventually refactor to Regex if possible
        file_name = f"{base_filename}({file_number}){file_type}"

    # Bucket vs. Key Cloud Issues
    if UPLOAD_FOLDER_TYPE == 'CLOUD':
        file_path = file_name
    else:
        file_path = f'{UPLOAD_FOLDER}{UPLOAD_FOLDER_KEY}{file_name}'

    return file_path, file_type
