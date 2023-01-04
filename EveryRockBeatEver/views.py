from flask import Blueprint
from flask import session, current_app
from flask import Flask, render_template, request, redirect, url_for
from EveryRockBeatEver.functions import generate_MIDI, parse_user_preset
from EveryRockBeatEver.db import legal_file
import json
import secrets

bp = Blueprint("views", __name__)

# Instantiate HTML Form Fields JSON & USER Presets Template JSON
with open("./EveryRockBeatEver/_static/html_form_fields.json") as f:
    HTML_FORM_FIELDS = json.load(f)
with open("./EveryRockBeatEver/_static/user_presets_template.json") as f:
    USER_STOCK_JSON = json.load(f)


@bp.route('/', methods=['GET', 'POST'])
def index(LOGGER: any = None):
    """ DISPLAY: Index Page and Links, IN: Session Key Initialization, OUT: Session Key """

    # Instantiate / Reference a session ID for the USER
    version = current_app.config["VERSION"]
    USER_STOCK_JSON['app_version'] = f'{version}'
    session_id = USER_STOCK_JSON['session_id']
    if session_id == 'None' and not LOGGER:
        session_id = secrets.token_urlsafe(16)
        USER_STOCK_JSON['session_id'] = f'{session_id}'
        session['session_id'] = session_id

        # Begin Master LOG from Session ID
        LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')
        LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOG', file_type='LOG')
        LOGGER.info(f"\n{'=' * 8} Begin Master Log | App Version: {version} {'=' * 8}\n"
                    f"___&&& Session ID: {USER_STOCK_JSON['session_id']} &&&___\n")

    # Instantiate / Rewrite a template ID
    template_id = secrets.token_urlsafe(16)
    USER_STOCK_JSON['template_id'] = f'{template_id}'
    session['template_id'] = template_id
    if not LOGGER:
        LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='LOG')
    LOGGER.info(f"\n{'*' * 6} Template Initialized!! {'*' * 6}\n"
                f"+++[[[ Template ID: {USER_STOCK_JSON['template_id']} ]]]+++\n")

    # Instantiate / SAVE a Session ID File Folder w/ USER PRESETS, USER_TEMPLATE, & LOGGER OBJECT
    USER_TEMPLATE = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='USER_TEMPLATE')
    USER_PRESETS = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='USER_PRESETS')
    LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')

    return render_template('index.html', title='Main', session_id=session_id,
                           template_id=template_id, version=version)


@bp.route('/about')
def about():
    """ -- About Section -- """
    return render_template('about.html', title='About')


@bp.route('/tutorial')
def tutorial():
    """ -- Tutorials Section -- """
    return render_template('tutorial.html', title='Tutorial')


@bp.route('/randomize', methods=['GET', 'POST'])
def randomize():
    """ DISPLAY: Step1, Step2, Step3, Step4 Dropdowns
        IN: Step1, Step2, Step3, Step4 Random Parameters
        OUT: Parsed USER_PRESETS -> Page Transfer: Generate MIDI """

    # Load LOGGER
    LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='LOG')

    # If the User submits the form -> redirect w/ variables, else return page
    if request.method == 'POST':
        form_submit = request.form.getlist('randomize[]')

        # Parse USER Data into USER PRESET JSON -- step1[] + step2_random UPDATE (LOG)
        if form_submit:
            LOGGER.info(f'Randomize form submit: {form_submit}\n')
            USER_PRESETS, USER_TEMPLATE = parse_user_preset(
                HFF=HTML_FORM_FIELDS, USER_PRESETS_UPLOAD=USER_STOCK_JSON,
                form_submit=form_submit, LOGGER=LOGGER)

            # SAVE Presets and LOG before transfer
            USER_TEMPLATE = legal_file(USER_PRESETS=USER_TEMPLATE, task='SAVE', file_type='USER_TEMPLATE')
            USER_PRESETS = legal_file(USER_PRESETS=USER_PRESETS, task='SAVE', file_type='USER_PRESETS')
            LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')

            return redirect(url_for('views.generate_midi'))

    return render_template('randomize.html', title='Step #1', HFF=HTML_FORM_FIELDS,
                           session_id=f"{session.get('session_id')}", template_id=f"{session.get('template_id')}")


@bp.route('/step1', methods=['GET', 'POST'])
def collect_step1(HFF=None):
    """ DISPLAY: STEP1 Attributes: # of BARS, TIME_SIGNATURE, RANDOM_SEED & PARTIAL_PALETTE
        OUT: Parsed USER PRESETS -> Page Transfer: Step 2"""

    # Load LOGGER
    LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='LOG')
    if not HFF:
        HFF = HTML_FORM_FIELDS  # RELOAD as shorter variable

    # If the User submits the form -> redirect w/ variables, else return page
    if request.method == 'POST':
        form_submit = request.form.getlist('step1[]')
        # print(form_submit)

        # Parse USER Data into USER PRESET JSON -- Step 1 UPDATE
        if form_submit:
            USER_PRESETS, USER_TEMPLATE = parse_user_preset(
                HFF=HTML_FORM_FIELDS, USER_PRESETS_UPLOAD=USER_STOCK_JSON,
                form_submit=form_submit, LOGGER=LOGGER)

            # SAVE Presets and LOG before transfer
            USER_TEMPLATE = legal_file(USER_PRESETS=USER_TEMPLATE, task='SAVE', file_type='USER_TEMPLATE')
            USER_PRESETS = legal_file(USER_PRESETS=USER_PRESETS, task='SAVE', file_type='USER_PRESETS')
            LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')

            return redirect(url_for('views.collect_step2'))

    return render_template('step1.html', title='Step #1', HFF=HTML_FORM_FIELDS)


@bp.route('/step2', methods=['GET', 'POST'])
def collect_step2():
    """ DISPLAY: STEP2 Attributes: Partial Palette
        OUT: Parsed USER PRESETS -> Page Transfer: Generate MIDI"""

    # Retrieve all USER submitted DATA
    LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='LOG')
    USER_PRESETS = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='USER_PRESETS')
    USER_TEMPLATE = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='USER_PRESETS')
    step2_partial_map = USER_PRESETS['step2[]']['step2_partial_map']

    # When the user submits the form
    if request.method == 'POST':
        form_submit = request.form.getlist('step2[]')

        # Parse USER Data into USER PRESET JSON -- Step 2 UPDATE
        if form_submit:
            USER_PRESETS, USER_TEMPLATE = parse_user_preset(
                HFF=HTML_FORM_FIELDS, USER_PRESETS_UPLOAD=USER_PRESETS,
                form_submit=form_submit, LOGGER=LOGGER)

            # SAVE Presets and LOG before transfer
            USER_TEMPLATE = legal_file(USER_PRESETS=USER_TEMPLATE, task='SAVE', file_type='USER_TEMPLATE')
            USER_PRESETS = legal_file(USER_PRESETS=USER_PRESETS, task='SAVE', file_type='USER_PRESETS')
            LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')

            return redirect(url_for('views.generate_midi'))

    return render_template('step2.html', title='Step #1', HFF=HTML_FORM_FIELDS,
                           step2_partial_map=step2_partial_map, USER_PRESETS=USER_PRESETS,
                           USER_TEMPLATE=USER_TEMPLATE)


@bp.route('/generate_midi', methods=['GET', 'POST'])
def generate_midi():
    """ DISPLAY: Bars, Tempo, and Write MIDI button
        IN: Bars, Tempo
        OUT: Write Pathos MIDI to MIDI_files folder """

    # Retrieve all USER submitted DATA
    USER_PRESETS = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='USER_PRESETS')
    USER_TEMPLATE = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='USER_PRESETS')
    LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='LOAD', file_type='LOG')
    MIDI_file = request.args.get('MIDI_file')  # Generated File
    url = request.args.get('url')  # Download Path from S3 Bucket

    # If the USER submitted data
    if request.method == 'POST':
        print(request.form, MIDI_file)
        for i in request.form:
            print(i, request.form[i])

        # If the user clicked on the LOAD PRESET button
        # if 'load_preset' in request.form:
        #     # Return USER PRESET to User
        #     # MIDI_file = generate_MIDI(bars, tempo,
        #     #                           UPLOAD_FOLDER_TYPE, UPLOAD_FOLDER,
        #     #                           UPLOAD_FOLDER_KEY, client_resource, client,
        #     #                          )
        #     return redirect(url_for("views.generate_midi", MIDI_file=MIDI_file))

        # If the user clicked on the GENERATE CUSTOM MIDI button
        if request.form.get('generate_midi'):
            if 'Generate Custom MIDI' in request.form.get('generate_midi'):

                # Preserve USER TEMPLATE and Generate MIDI File
                MIDI_file = generate_MIDI(USER_PRESETS=USER_PRESETS, LOGGER=LOGGER)
                print(f'\n MIDI File: {MIDI_file}\n')

                # Save MIDI File -- Overwrite Local Instance
                MIDI_save = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE',
                                       file_type='MIDI', tmp_file=MIDI_file)
                # Save LOG
                LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')

                return redirect(url_for('views.generate_midi', MIDI_file=MIDI_file))

        # If the USER clicked on the QUICK GENERATE BUTTON
        if request.form.get('quick_generate'):
            # Generate MIDI File Based on QUICK GENERATE
            ...

            return redirect(url_for("generate_midi", MIDI_file=MIDI_file))

        # USER clicked on Download MIDI after Generate MIDI
        if request.form.get('download_midi') and MIDI_file:
            print(MIDI_file, request.form.get('download_midi'))
            if 'Download MIDI' in request.form['download_midi']:
                url = legal_file(USER_PRESETS=USER_PRESETS, task='DOWNLOAD', file_type='MIDI')
                print(url)
                return redirect(url)

    # SAVE LOG before transfer
    LOGGER = legal_file(USER_PRESETS=USER_STOCK_JSON, task='SAVE', file_type='LOG')
    print(f'\n MIDI File: {MIDI_file}\n')

    return render_template('stepx_generate.html', title='Pathos - Generate MIDI File',
                           MIDI_file=MIDI_file, url=url, USER_PRESETS=USER_PRESETS,
                           USER_TEMPLATE=USER_TEMPLATE, session_id=f"{session.get('session_id')}",
                           template_id=f"{session.get('template_id')}")
