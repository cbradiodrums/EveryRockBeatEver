from flask import current_app
from flask import g
import os
import json
import boto3
import botocore
import logging


def get_s3(client: any = 'client'):
    """ Connect to the application's cloud database. Configure in dotenv. """

    if current_app.config["CLOUD_SERVER"] is not None:
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


def legal_file(USER_PRESETS: dict = None, task: str = '',
               file_type: str = '', tmp_file: str = ''):
    """ Manipulate a Legal File within parameters specified
        IN: (Parsed) USER_PRESETS, (Parsed) USER_TEMPLATE
            task (SAVE/LOAD), file_type (LOG/USER_PRESETS/MIDI)
        FUNCTION: task[SAVE/LOAD/LOG/DOWNLOAD] -> location(s) [LOCAL/CLOUD]
         OUT: SAVE (null), LOAD (FILE_OBJECT) """

    # Determine the USER -- current session / template
    session_id, template_id = USER_PRESETS['session_id'], USER_PRESETS['template_id']

    # Determine the File Type:
    if file_type == 'LOG':
        ROOT, KEY, FILE = f'usr_{session_id}', 'logs', f'log_{session_id}.txt'

        if task == 'LOG':
            file_path = f'{current_app.instance_path}/users/{ROOT}/{KEY}/{FILE}'
            LOGGER = logging.getLogger(file_path)
            LOGGER.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler(file_path)
            fh.setFormatter(formatter)
            LOGGER.addHandler(fh)

            return LOGGER

    elif file_type == 'USER_PRESETS':
        template_id = USER_PRESETS['template_id']
        ROOT, KEY, FILE = f'usr_{session_id}', 'user_presets', f'preset_{template_id}.json'

    elif file_type == 'USER_TEMPLATE':
        template_id = USER_PRESETS['template_id']
        ROOT, KEY, FILE = f'usr_{session_id}', 'user_presets', f'template_{template_id}.json'

    elif file_type == 'MIDI':
        template_id = USER_PRESETS['template_id']
        ROOT, KEY, FILE = f'usr_{session_id}', 'MIDI_files', f'MIDI_{template_id}.mid'

    else:
        ROOT, KEY, FILE = None, None, None

    # Local Instance
    if current_app.config["APP_CONTEXT"] != 'CLOUD':
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
                    json.dump(USER_PRESETS, f)

            elif FILE[-4:] == '.txt':
                with open(file_path, 'a') as f:
                    f.write('{{{--- LOG FILE SAVED TO CLOUD ---}}}\n')

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

            elif FILE[-4:] == '.txt':
                LOGGER = logging.getLogger(file_path)
                return LOGGER

    # Cloud Connection ( if applicable )
    client, resource = get_s3(), get_s3('resource')

    if client and resource:
        BUCKET = current_app.config["CLOUD_BUCKET"]
        file_path = f'users/{ROOT}/{KEY}/{FILE}'

        # Determine what to do with the File
        if task == 'SAVE':
            with open(f'{current_app.instance_path}/{file_path}', "rb") as f:
                client.upload_fileobj(f, BUCKET, file_path)

        elif task == 'DOWNLOAD' and file_type != 'LOG':
            url = client.generate_presigned_url('get_object',
                                                Params={'Bucket': BUCKET, 'Key': file_path},
                                                ExpiresIn=60)
            return url


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    s3 = g.pop("s3", None)

    # if s3 is not None:
    #     s3.close()


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    current_app.app_context()


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
