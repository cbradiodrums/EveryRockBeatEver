from flask import Blueprint
from flask import session, current_app
from flask import Flask, render_template, request, redirect, url_for
from EveryRockBeatEver.functions import generate_MIDI, parse_user_preset
from EveryRockBeatEver.db import legal_file
import json
import secrets
import pygame

bp = Blueprint("views", __name__)

# Instantiate ROCK Presets Template JSON
with open("./EveryRockBeatEver/_static/rock_presets_template.json") as f:
    USER_STOCK_JSON = json.load(f)


@bp.route('/', methods=['GET', 'POST'])
def quick_generate(LOGGER: any = None, MIDI_sheet: any = None):
    """ DISPLAY: Bars, Tempo, and Write MIDI button
        IN: Bars, Tempo
        OUT: Write Pathos MIDI to MIDI_files folder """

    # Instantiate / Reference a session ID for the USER
    version = current_app.config["VERSION"]
    USER_STOCK_JSON['app_version'] = f'{version}'
    session_id = session.get('session_id')
    if not session_id and not LOGGER:
        session_id = secrets.token_urlsafe(16)
        USER_STOCK_JSON['session_id'] = f'{session_id}'
        session['session_id'] = session_id

        # Begin Master LOG from Session ID
        LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')
        LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOG', file_type='LOG')
        LOGGER.info(f"\n{'=' * 8} Begin Master Log | App Version: {version} {'=' * 8}\n"
                    f"___&&& Session ID: {USER_STOCK_JSON['session_id']} &&&___\n")
    else:
        LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='LOG')

    MIDI_file = request.args.get('MIDI_file')  # Generated File
    url = request.args.get('url')  # Download Path from S3 Bucket

    # If the USER submitted data
    if request.method == 'POST':
        print(request.form, MIDI_file)
        for i in request.form:
            print(i, request.form[i])

        # If the user clicked on the GENERATE CUSTOM MIDI button
        if request.form.get('quick_generate'):
            if 'Quick Generate' in request.form.get('quick_generate'):

                # Instantiate / Rewrite a template ID
                template_id = secrets.token_urlsafe(16)
                USER_STOCK_JSON['template_id'] = f'{template_id}'
                session['template_id'] = template_id
                LOGGER.info(f"\n{'*' * 6} Template Initialized!! {'*' * 6}\n"
                            f"+++[[[ Template ID: {USER_STOCK_JSON['template_id']} ]]]+++\n")

                # Preserve USER TEMPLATE and Generate MIDI File
                MIDI_file = generate_MIDI(USER_PRESETS=USER_STOCK_JSON, LOGGER=LOGGER)
                print(f'\n MIDI File: {MIDI_file}\n')

                # Save MIDI File -- Overwrite Local Instance
                MIDI_save = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE',
                                       file_type='MIDI', tmp_file=MIDI_file)
                # Save LOG
                LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')

                return redirect(url_for('views.quick_generate', MIDI_file=MIDI_file))

        # USER clicked on Download MIDI after Generate MIDI
        if request.form.get('download_midi') and MIDI_file:
            print(MIDI_file, request.form.get('download_midi'))
            if 'Download MIDI' in request.form['download_midi']:
                url = legal_file(USER_PRESETS=USER_STOCK_JSON, task='DOWNLOAD', file_type='MIDI')
                print(url)
                return redirect(url)

        # USER clicked on Playback MIDI after Generate MIDI
        if request.form.get('playback_midi') and MIDI_file:
            print(MIDI_file, request.form.get('playback_midi'))
            if 'Playback MIDI' in request.form['playback_midi']:
                pygame.init()
                pygame.mixer.music.load("temp_MIDI_File.mid")
                pygame.mixer.music.play()

    # SAVE LOG before transfer
    # LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')
    print(f'\n MIDI File: {MIDI_file}\n')

    return render_template('stepx_generate.html', title='ERBE - Generate MIDI File',
                           MIDI_file=MIDI_file, url=url,
                           # USER_PRESETS=USER_PRESETS,
                           # USER_TEMPLATE=USER_TEMPLATE,
                           session_id=f"{session.get('session_id')}",
                           template_id=f"{session.get('template_id')}")


@bp.route('/about')
def about():
    """ -- About Section -- """
    return render_template('about.html', title='About')


@bp.route('/tutorial')
def tutorial():
    """ -- Tutorials Section -- """
    return render_template('tutorial.html', title='Tutorial')

