from flask import Blueprint
from flask import session, current_app
from flask import render_template, request, redirect, url_for, send_file
from EveryRockBeatEver.functions import generate_MIDI
from EveryRockBeatEver.db import legal_file
import json
import secrets
from pygame import mixer

bp = Blueprint("views", __name__)

# Instantiate ROCK Presets Template JSON
with open("./EveryRockBeatEver/_static/rock_presets_template.json") as f:
    USER_STOCK_JSON = json.load(f)


@bp.route('/', methods=['GET', 'POST'])
def quick_generate(LOGGER: any = None):
    """ DISPLAY: Bars, Tempo, and Write MIDI button
        IN: Bars, Tempo
        OUT: Write Pathos MIDI to MIDI_files folder """

    # Instantiate / Reference a session ID for the USER
    version = current_app.config["VERSION"]
    USER_STOCK_JSON['app_version'] = f'{version}'
    session_id = session.get('session_id')

    if not session_id and not LOGGER:
        session_id = secrets.token_urlsafe(16)
        session['session_id'] = session_id

        # Begin Session LOG from Session ID --
        legal_file(task='SAVE', file_type='LOG', session_id=session_id)
        LOGGER = legal_file(task='LOG', file_type='LOG', session_id=session_id)
        LOGGER.info(f"\n{'=' * 8} Begin Master Log | App Version: {version} {'=' * 8}\n"
                    f"___&&& Session ID: {session.get('session_id')} &&&___\n")
    else:
        LOGGER = legal_file(task='LOAD', file_type='LOG', session_id=session_id)

    # Retrieve USER Specific Session Information
    MIDI_file = request.args.get('MIDI_file')  # Generated File
    url = request.args.get('url')  # Download Path from S3 Bucket
    template_id = request.args.get('template_id')

    # If the USER submitted data
    if request.method == 'POST':

        # If the user clicked on the GENERATE CUSTOM MIDI button
        if request.form.get('quick_generate'):
            if 'Quick Generate' in request.form.get('quick_generate'):

                # Instantiate / Rewrite a template ID
                template_id = secrets.token_urlsafe(16)
                session['template_id'] = template_id
                LOGGER.info(f"\n{'*' * 6} Template Initialized!! {'*' * 6}\n"
                            f"+++[[[ Template ID: {session.get('template_id')} ]]]+++\n")

                # Instantiate USER PRESETS for the Template -- Cloud Upload (Production)
                legal_file(USER_PRESETS=USER_STOCK_JSON, file_type='USER_PRESETS', task='SAVE',
                           session_id=session_id, template_id=template_id)
                USER_TEMPLATE = legal_file(file_type='USER_PRESETS', task='LOAD',
                                           session_id=session_id, template_id=template_id)

                # Preserve USER TEMPLATE and Generate MIDI File (print_stmnt = True for console logs)
                MIDI_filepath = generate_MIDI(USER_PRESETS=USER_TEMPLATE, LOGGER=LOGGER)

                # Save MIDI File -- Overwrite Local Instance
                legal_file(USER_PRESETS=USER_TEMPLATE, task='SAVE',
                           session_id=session_id, template_id=template_id,
                           file_type='MIDI', tmp_file=MIDI_filepath)
                # Save LOG -- Overwrite Cloud
                legal_file(USER_PRESETS=USER_TEMPLATE, task='SAVE',
                           file_type='LOG', session_id=session_id)

                return redirect(url_for('views.quick_generate', MIDI_file=MIDI_filepath,
                                        template_id=template_id))

        # USER clicked on Download MIDI after Generate MIDI
        if request.form.get('download_midi') and MIDI_file:
            if 'Download MIDI' in request.form['download_midi']:
                USER_TEMPLATE = legal_file(file_type='USER_PRESETS', task='LOAD',
                                           session_id=session_id, template_id=template_id)

                if current_app.config["APP_CONTEXT"] != 'LOCAL':
                    url = legal_file(USER_PRESETS=USER_TEMPLATE, task='DOWNLOAD', file_type='MIDI',
                                     session_id=session_id, template_id=template_id)
                    return redirect(url)

                else:
                    return send_file('../' + MIDI_file, MIDI_file)

        # USER clicked on Playback MIDI after Generate MIDI (LOCAL ONLY)
        if (request.form.get('playback_midi') and MIDI_file and
                current_app.config["APP_CONTEXT"] == 'LOCAL'):

            if 'Playback MIDI' in request.form['playback_midi']:
                mixer.init()
                mixer.music.load(MIDI_file)
                mixer.music.play()

            if 'Stop MIDI' in request.form['playback_midi']:
                mixer.music.stop()

    return render_template('stepx_generate.html', title='ERBE - Generate MIDI File',
                           MIDI_file=MIDI_file, url=url, CONTEXT=current_app.config['APP_CONTEXT'],
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
