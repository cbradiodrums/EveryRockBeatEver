# -- Every Drumbeat Ever Function File --
# END PRODUCT: A USER downloads MIDI data of finished drum beat; specified by USER parameters
# RHYTHM SPACE: User-selected / Randomized generated rhythmic framework via musical rests
# VOICINGS: User-selected / Randomized assignment of drumset voicings. [MODE: Linear / Beat]
# DYNAMICS: User-selected / Randomized assignment of dynamics.
# TIMBRE: Assignment of TIMBRES
# TEMPO / PLAYBACK: Playback tool
# SAVE FUNCTION: Submits Data to see user's favorite save states for ML
# EXPORT MIDI: Exports drum riff via GM MAP MIDI Notes
# CUSTOM EXPORT: Exports drum riffs via custom MIDI MAP
from midiutil import MIDIFile
from fractions import Fraction as Fr
import random
from copy import deepcopy

from flask import Blueprint, current_app

bp = Blueprint("functions", __name__)


def parse_user_preset(HFF: dict = None, USER_PRESETS_UPLOAD: dict = None, form_submit: list = None,
                      print_stmnt: bool = True, step1_forms: bool = None, step2_custom: bool = None,
                      LOGGER: any = None):
    """ IN:
            FORM SUBMIT FORMAT: [MASTER|KEY|SUB_KEY|DEEP_KEY|LOW_KEY|VALUE]
            HFF: HTML_FORM_FIELD, USER_PRESETS: (If None: USER_PRESETS_TEMPLATE) (else: loaded USER_PRESETS)
            STEP1: step1[Bars, Time Signature, Random Seed, Random? Partial Palette] || random_step1 || random_all
            STEP2: step2[Weights, Breakability] || random_step1 / step1[2]
            STEP3: step3[Voicing, Weight] || random_step2 / step3[] Voicing Palette
            STEP4: step4[Dynamic, Weight] || random_step3 / step4[] Dynamic Palette
            STEP5: step5[Timbre, Weight] || random_step4 / step5[] Timbre Palette
        OUT:
            JSONs: (USER SAVED PRESETS, UPDATED USER PRESETS)  """

    # DeepCopy Templates so they aren't Overwritten on constant iterations:
    USER_PRESETS, HFF = deepcopy(USER_PRESETS_UPLOAD), deepcopy(HFF)

    # RANDOM HIERARCHY: Custom Steps < Random Step < Random All [ '<' == OVERWRITTEN BY ]
    # NOTE: DICTIONARY MAY CHANGE SIZE DURING PROCESS; MAY NEED DEEP COPY...
    # FORM Parse; Assign any global parameters USER submitted in FORMS
    # 0-1a) If USER submitted forms (form_submit), COPY TEMPLATE, THEN, OVERWRITE USER PRESETS

    if print_stmnt:
        print('USER PRESETS TEMPLATE:', USER_PRESETS, '\n')
    if LOGGER:
        LOGGER.info(f'USER PRESETS TEMPLATE: {USER_PRESETS} \n')

    if form_submit:
        def assign_form(form_str: str = None, sep: str = '|'):
            """ IN: Form(Str), Seperator(str), OUT: Assign Form to USER PRESETS"""

            k = form_str.split(sep)
            if print_stmnt:
                print(f"test0 UP', {USER_PRESETS['step2[]']['step2_partial_map']}, \ntest0 HFF: "
                      f"{HFF['step2[]']['step2_partial_map'][0]}, \nk:, {k}, \n")
            if LOGGER:
                LOGGER.info(f"test0 UP', {USER_PRESETS['step2[]']['step2_partial_map']}, \ntest0 HFF: "
                            f"{HFF['step2[]']['step2_partial_map'][0]}, \nk:, {k}, \n")
            if 'step2_partial_map' not in k:
                USER_PRESETS[k[0]][k[1]] = k[2]
            if 'WGT' in k:
                USER_PRESETS[k[0]][k[1]][k[2]][k[3]] = k[4]
            if 'BRK' in k:
                USER_PRESETS[k[0]][k[1]][k[2]][k[3]][k[4]] = k[5]

            return k

        # Unpack Forms and Update USER PRESETS one at a time
        for form in form_submit:
            fs = assign_form(form_str=form)

            # If custom step values were submitted; avoid overwriting and randomization
            if 'step1[]' in fs:
                step1_forms = True
            if 'step2_partial_palette' in fs:
                step2_custom = True

    # 0-1b) Save the USER PRESETS before Parsing to offer as Download later...
    USER_TEMPLATE = deepcopy(USER_PRESETS)
    if print_stmnt:
        print(f'SAVED USER PRESETS after PARSE: {USER_TEMPLATE}')  # VERIFY!!
    if LOGGER:
        LOGGER.info(f'SAVED USER PRESETS after PARSE: {USER_TEMPLATE}')

    # USER PRESETS Parse; Assign any global parameters USER submitted in FORMS
    # 0-2a) Assess USER PRESETS Random Steps (this may be OVERWRITTEN)
    for key in USER_PRESETS:
        if key[:4] == 'step':
            if USER_PRESETS[key][f'{key[:5]}_random'] not in ['Custom', 'None']:
                for sub_key in USER_PRESETS[key]:
                    USER_PRESETS[key][sub_key] = USER_PRESETS[key][f'{key[:5]}_random']

    # 0-2b) Assess USER PRESETS Random All, Overwrite Random Steps if USED
    if USER_PRESETS['random_all[]']['random_all'] not in ['Custom', 'None']:
        for key in USER_PRESETS:
            if key[:4] == 'step':
                for sub_key in USER_PRESETS[key]:
                    USER_PRESETS[key][sub_key] = USER_PRESETS['random_all[]']['random_all']

    # All Global Random Attributes have been sorted.
    # 1) Parse Step 1 -- Determine if the step is a random attribute.
    sub_key_exclude = [f'step{s}_random' for s in [1, 2, 3, 4, 5]]
    deep_key_exclude = ['NONE', 'SHUFFLE']
    step1_exclude = sub_key_exclude + ['step1_partial_palette']
    if step1_forms:
        for sub_key in USER_PRESETS['step1[]']:

            randomization = USER_PRESETS['step1[]'][sub_key]
            if sub_key not in step1_exclude:  # Not Overwriting / Parsing Random Steps..
                random_mods = []
                # If the parsed value is random; parse the random bucket
                for deep_key, value_list in HFF['step1[]'][sub_key][0]['MODIFIERS'].items():
                    if deep_key not in deep_key_exclude:
                        for value in value_list:
                            random_mods.append(value)
                if randomization in random_mods + ['ANY']:
                    if print_stmnt:
                        print(f"**Random Modifier**\nrandomization: {randomization}, Sub_Key: {sub_key}, "
                              f"Random Mods: {random_mods}, RS Submit: {sub_key_exclude}")
                    if LOGGER:
                        LOGGER.info(f"**Random Modifier**\nrandomization: {randomization}, Sub_Key: {sub_key}, "
                                    f"Random Mods: {random_mods}, RS Submit: {sub_key_exclude}")
                    # If the random value is ANY; shuffle into a legal Random Modifier
                    if randomization == 'ANY':
                        shuffle_bowl = random_mods.copy()
                        shuffle_pick = shuffle_bowl[random.randint(0, len(shuffle_bowl) - 1)]
                        USER_PRESETS['step1[]'][sub_key] = shuffle_pick  # Overwrite USER PRESETS Value
                        randomization = USER_PRESETS['step1[]'][sub_key]  # reload variable

                    # Then, assign the USER PRESET a value from the legal random modifier bucket
                    shuffle_bowl = HFF['step1[]'][sub_key][0][randomization].copy()
                    shuffle_pick = shuffle_bowl[random.randint(0, len(shuffle_bowl) - 1)]
                    USER_PRESETS['step1[]'][sub_key] = shuffle_pick
                    if print_stmnt:
                        print(f'sub_key: {sub_key}, shuffle_bowl: {shuffle_bowl}, shuffle_pick: {shuffle_pick}')
                    if LOGGER:
                        LOGGER.info(f'sub_key: {sub_key}, shuffle_bowl: {shuffle_bowl}, shuffle_pick: {shuffle_pick}')

            # Parsing Step 1 Partial Palette for Step 2 Display -- Referencing Time Signature
            elif sub_key == 'step1_partial_palette' and step2_custom is not True:
                if print_stmnt:
                    print(f'\nShould NOT be here on Custom Step 2: Parse Step 1 Partial Palette\n')
                if LOGGER:
                    LOGGER.info(f'\nShould NOT be here on Custom Step 2: Parse Step 1 Partial Palette\n')

                randomization = USER_PRESETS['step1[]'][sub_key]
                random_mods = []
                # If the parsed value is random; parse the random bucket
                for deep_key, value_list in HFF['step1[]'][sub_key][0]['MODIFIERS'].items():
                    if deep_key not in deep_key_exclude:
                        for value in value_list:
                            random_mods.append(value)
                if randomization in random_mods + ['ANY']:
                    if print_stmnt:
                        print(f"**Random Modifier**\nrandomization: {randomization}, Sub_Key: {sub_key}, "
                              f"Random Mods: {random_mods}, RS Submit: {sub_key_exclude}")
                    if LOGGER:
                        LOGGER.info(f"**Random Modifier**\nrandomization: {randomization}, Sub_Key: {sub_key}, "
                                    f"Random Mods: {random_mods}, RS Submit: {sub_key_exclude}")
                    # If the random value is ANY; shuffle into a legal Random Modifier
                    if randomization == 'ANY':
                        shuffle_bowl = random_mods.copy()
                        shuffle_pick = shuffle_bowl[random.randint(0, len(shuffle_bowl) - 1)]
                        USER_PRESETS['step1[]'][sub_key] = shuffle_pick  # Overwrite USER PRESETS Value
                        randomization = USER_PRESETS['step1[]'][sub_key]  # reload variable
                        if print_stmnt:
                            print(f'shuffle_pick: {shuffle_pick}, randomization: {randomization}')  # VERIFY!!
                        if LOGGER:
                            LOGGER.info(f'shuffle_pick: {shuffle_pick}, randomization: {randomization}')

                    # Then, assign the USER PRESET a value from the legal random modifier bucket
                    # MODIFIERS of step1 partial palette == step 2 partial map
                    # Overwrite step2_partial_map
                    USER_PRESETS['step2[]']['step2_partial_map'] = HFF['step2[]']['step2_partial_map'][0][randomization]

                    # Reference Time Signature Value
                    time_signature = USER_PRESETS['step1[]']['step1_time_signature']
                    ts_length = Fr(time_signature) * 4

                    # Iterate through the assigned step2 partial map and falsify illegal values
                    for note in USER_PRESETS['step2[]']['step2_partial_map']:
                        if USER_PRESETS['step2[]']['step2_partial_map'][note]['WGT'] == "True":
                            part_val = Fr(USER_PRESETS['step2[]']['step2_partial_map'][note]['VAL'])
                            brk_ct = 0
                            for brk in USER_PRESETS['step2[]']['step2_partial_map'][note]['BRK']:
                                if USER_PRESETS['step2[]']['step2_partial_map'][note]['BRK'][brk] != 'False':
                                    brk_num = Fr(brk, _normalize=False).numerator
                                    if brk_num * part_val <= ts_length:
                                        USER_PRESETS['step2[]']['step2_partial_map'][note]['BRK'][brk] = "True"
                                        brk_ct += 1
                            if brk_ct == 0:
                                USER_PRESETS['step2[]']['step2_partial_map'][note]['WGT'] = "False"

    # 2) Parse Step 2 -- Determine IF the step is a random attribute, Else Pass
    if USER_PRESETS['step2[]']['step2_random'] not in ['Custom', 'None']:
        if print_stmnt:
            print(f'\nShould NOT be here on Custom Step 2: Parse Step 2\n')
        if LOGGER:
            LOGGER.info(f'\nShould NOT be here on Custom Step 2: Parse Step 2\n')

        # Reference Time Signature to Avoid Illegal Assignments
        time_signature = Fr(USER_PRESETS['step1[]']['step1_time_signature'])
        randomization = USER_PRESETS['step2[]']['step2_random']
        if randomization == 'ANY':
            shuffle_bowl = []
            for low_key in HFF['step2[]']['step2_partial_map'][0]['MODIFIERS']:
                for value in HFF['step2[]']['step2_partial_map'][0]['MODIFIERS'][low_key]:
                    if value != 'ANY':
                        shuffle_bowl.append(value)
            shuffle_pick = shuffle_bowl[random.randint(0, len(shuffle_bowl) - 1)]
            USER_PRESETS['step2[]']['step2_random'] = shuffle_pick
            randomization = USER_PRESETS['step2[]']['step2_random']

        # Fill Step 2 -- Assemble According to Random Step 2
        USER_PRESETS['step2[]']['step2_partial_map'] = deepcopy(HFF['step2[]']['step2_partial_map'][0][randomization])
        # Depending on the Partial Palette, Randomly Generate the Partial Map
        HFF2 = deepcopy(HFF)
        for note in HFF2['step2[]']['step2_partial_map'][0][randomization]:
            for sub_key in HFF2['step2[]']['step2_partial_map'][0][randomization][note]:

                # Assign Weights
                if sub_key == "WGT":
                    if HFF2['step2[]']['step2_partial_map'][0][randomization][note][sub_key] != "False":

                        # Preserve the Spirit of the Partial Palette before Assignment
                        if randomization == 'Extreme':
                            shuffle = str(random.randint(0, 5))
                        else:
                            shuffle = str(random.randint(1, 5))
                        USER_PRESETS['step2[]']['step2_partial_map'][note][sub_key] = shuffle

                # Assign Breakability
                elif sub_key == "BRK":
                    for brk in HFF2['step2[]']['step2_partial_map'][0][randomization][note][sub_key]:
                        if HFF2['step2[]']['step2_partial_map'][0][randomization][note][sub_key][brk] != "False":

                            # Preserve the Spirit of the Partial Palette before Assignment
                            if randomization == 'Extreme':
                                shuffle = str(random.randint(0, 5))
                            else:
                                shuffle = str(random.randint(1, 5))
                            USER_PRESETS['step2[]']['step2_partial_map'][note][sub_key][brk] = shuffle

    if print_stmnt:
        print(f'\nUSER_PRESETS: {USER_PRESETS}')  # VERIFY!!

    return USER_PRESETS, USER_TEMPLATE


def generate_MIDI(USER_PRESETS: dict = None, LOGGER: any = None):

    def build_rhythm_space(USER_PRESETS: dict = None, print_stmnt: bool = True, LOGGER: any = None):
        """ IN: USER parsed BARS, TEMPO, & PARTIAL DICTIONARY
            OUT: MIDI FILE Write Schematic """

        # DeepCopy USER_PRESETS to Avoid Errors
        UP = deepcopy(USER_PRESETS)

        # Assign USER_PRESETS to variables for Generation;
        bars = int(USER_PRESETS['step1[]']['step1_bars'])
        time_signature = USER_PRESETS['step1[]']['step1_time_signature']
        partial_map = USER_PRESETS['step2[]']['step2_partial_map']
        if print_stmnt:
            print(f'bars: {bars}, time_signature: {time_signature}\n partial_map: {partial_map}\n')
        if LOGGER:
            LOGGER.info(f'bars: {bars}, time_signature: {time_signature}\n partial_map: {partial_map}\n')

        # Partial Map Note Randomizer / Weight Shuffler:
        partial_bowl = []
        for note in partial_map:
            p_wgt = partial_map[note]['WGT']
            if p_wgt not in ['False', 'None', '0']:
                for part in range(int(p_wgt)):
                    partial_bowl.append(note)
        legal_partial_bowl = partial_bowl.copy()
        if print_stmnt:
            print(f'partial bowl: {partial_bowl}\n partial_bowl_set: {set(partial_bowl)}')
        if LOGGER:
            LOGGER.info(f'partial bowl: {partial_bowl}\n partial_bowl_set: {set(partial_bowl)}')

        # Determine which bar we are working on / Instantiate Rhythm Space
        rhythm_space = []
        for bar in range(bars):
            print(f"\nBar Number: # {bar + 1} / {bars}, Time Signature: {time_signature}\n")  # VERIFY!!
            if LOGGER:
                LOGGER.info(f"\nBar Number: # {bar + 1} / {bars}, Time Signature: {time_signature}\n")

            # Instantiate the Available Bar Length, Rhythm Map, and (initial) PARTIAL BOWL
            bar_rhythm_map, bar_space = [], Fr(time_signature) * 4

            # Subtract from the rhythm space until it reaches 0
            while bar_space > 0:

                # LEGALIZE SET(BOWL) to REMOVE Unbreakable PARTIALS. (Prevents LOOP of PARTIAL BREAKABILITY > BAR_SPACE)
                for note in set(legal_partial_bowl):
                    legal_ct = 0
                    for brk in USER_PRESETS['step2[]']['step2_partial_map'][note]['BRK']:
                        if Fr(brk) <= bar_space:
                            legal_ct += 1
                    if legal_ct == 0:
                        legal_partial_bowl = [i for i in legal_partial_bowl if i != note]

                # Choose a RANDOM LEGAL PARTIAL in the LEGAL set (by Partial Fractional Value):
                partial = legal_partial_bowl[random.randint(0, len(legal_partial_bowl) - 1)]
                if print_stmnt:
                    print(f'Stripped legal_partial_bowl: {set(legal_partial_bowl)}\n '
                          f'PARTIAL Selected: {partial}')  # VERIFY!!
                if LOGGER:
                    LOGGER.info(f'Stripped legal_partial_bowl: {set(legal_partial_bowl)}\n '
                                f'PARTIAL Selected: {partial}')

                # The ABOVE LEGAL Conditions ensured that there is enough space for the partial.
                # Now we must consider its Breakability Weight to use...
                # Partial Map Breakability Randomizer / Weight Shuffler:
                brk_bowl, part_space = [], Fr(partial_map[partial]['VAL'])
                for brk in partial_map[partial]['BRK']:
                    brk_wgt = partial_map[partial]['BRK'][brk]

                    # Ensure the breakability can fit in the bar space and is desired
                    brk_space = Fr(brk, _normalize=False).numerator * part_space
                    if brk_wgt not in ['False', 'None', '0'] and brk_space <= bar_space:
                        for part in range(int(brk_wgt)):
                            brk_bowl.append(brk)
                if print_stmnt:
                    print(f'breakability bowl: {brk_bowl}\n brk_bowl_set: {set(brk_bowl)}')
                if LOGGER:
                    LOGGER.info(f'breakability bowl: {brk_bowl}\n brk_bowl_set: {set(brk_bowl)}')

                # If the breakability bowl is empty; the user selected weights and zero breakability...
                if not brk_bowl:

                    # Remove partial from bowl because there is nothing legal left...
                    legal_partial_bowl = [i for i in legal_partial_bowl if i != partial]

                else:
                    # Choose a RANDOM LEGAL PARTIAL BREAKABILITY:
                    breakability = Fr(brk_bowl[random.randint(0, len(brk_bowl) - 1)], _normalize=False)
                    print('BREAKABILITY Selected:', breakability)

                    # RANDOMLY Select the BREAKABILITY or its INVERSE (if < Bar Space and > 0):
                    if 0 < (1 - breakability) <= bar_space:
                        shuffle = random.randint(1, 4)
                        if shuffle >= 3:
                            breakability = Fr(breakability.denominator - breakability.numerator,
                                              breakability.denominator, _normalize=False)
                            print('Inverse Selected:', breakability)  # VERIFY!!
                        else:
                            print('Standard Select:', breakability)  # VERIFY!!
                    else:
                        print('Standard Select:', breakability)  # VERIFY!!

                    # Partial Space in range(BREAKABILITY (NUMERATOR)) = NOTE BLOCK to Append!
                    note_block = []
                    for i in range(breakability.numerator):
                        note_block.append(part_space)
                    bar_rhythm_map.append(note_block)

                    # Subtract the NOTE BLOCK from the BAR SPACE:
                    bar_space -= sum(note_block)
                    print(f'===\nBAR RHYTHM MAP:, {bar_rhythm_map}\nBAR SPACE Remaining: {bar_space}'
                          f'\nNOTE BLOCK selected:, {note_block}\n===')  # VERIFY!!
                    if LOGGER:
                        LOGGER.info(f'===\nBAR RHYTHM MAP:, {bar_rhythm_map}\nBAR SPACE Remaining: {bar_space}'
                                    f'\nNOTE BLOCK selected:, {note_block}\n===')

            # Tally the PARTIAL BREAKABILITY Assignments to Finish the BAR
            rhythm_space.append(bar_rhythm_map)
            print(f'***RHYTHM SPACE ( Bar # {bar + 1} / {bars} Time Signature: {time_signature} ):'
                  f'\n {rhythm_space}\n')
            if LOGGER:
                LOGGER.info(f'***RHYTHM SPACE ( Bar # {bar + 1} / {bars} Time Signature: {time_signature} ):'
                  f'\n {rhythm_space}\n')
        print('\n---&&&___RHYTHM SPACE FILLED___&&&---\n')
        if LOGGER:
            LOGGER.info('\n---&&&___RHYTHM SPACE FILLED___&&&---\n')
        return rhythm_space, time_signature

    def rock_MIDI(rhythm_space: list, tempo: float = 120, time_signature: str = '4/4', 
                   LOGGER: any = None):
        """ IN: Rhythm Space MIDI Map / Partial Breakability (Step 2)
            OUT: MIDI File for USER to download OR regenerate (FUTURE: Playback)"""

        track, channel = 0, 9  # Channel 9 is the percussion channel
        degrees_list = [36, 38]  # FUTURE TIMBRE MAP (i.e. 36 = Kick #1, 38 = Snare #2)
        volume = 100  # FUTURE DYNAMICS MAP [0 - 127]
        time = 0  # Where the Note is Placed (i.e. Count #1 = 0, Count #2 = 1)
        duration = 0  # How long the Note is held (i.e. Quarter = 1.0, 8th = 0.5)
        bpm = tempo  # In BPM

        # Parse Time Signature -- Must exist in the power of 2**
        ts_power2 = [str(2**i) for i in range(0, 7)]
        ts_num, ts_den = time_signature.split('/')[0], str(ts_power2.index(time_signature.split('/')[1]))

        MyMIDI = MIDIFile(1, file_format=1)  # One track, defaults to format 1 (tempo track created)
        MyMIDI.addTempo(track=1, time=0, tempo=bpm)
        bar_ct = 0

        # Rock Specific Rules:
        # timbre =

        for bar in rhythm_space:
            bar_ct += 1
            print(f"\n+++ BAR #{bar_ct} / {len(rhythm_space)}, Time Signature: {ts_num}/{ts_den} +++\n")
            if LOGGER:
                LOGGER.info(f"\n+++ BAR #{bar_ct} / {len(rhythm_space)}, Time Signature: {ts_num}/{ts_den} +++\n")
            MyMIDI.addTimeSignature(track=1, time=time, numerator=int(ts_num), denominator=int(ts_den),
                                    clocks_per_tick=24)
            for note_group in bar:
                for partial in note_group:
                    degrees = degrees_list[random.randint(0, len(degrees_list) - 1)]
                    duration = partial
                    print(f'Insert Time: {time}, Partial / Duration: {partial}, Pitch: {degrees}')
                    if LOGGER:
                        LOGGER.info(f'Insert Time: {time}, Partial / Duration: {partial}, Pitch: {degrees}')
                    MyMIDI.addNote(track, channel, degrees, time, duration, volume)
                    time += duration
                    print(f'Duration Added to Time!: {time}')
                    if LOGGER:
                        LOGGER.info(f'Duration Added to Time!: {time}')

        # Reset time to overwrite with hi hats test
        time = 0

        for bar in rhythm_space:
            print(f"\n[[[ Just Adding Hi Hats ]]]\n")

            for i in range(8):
                degrees = 42
                duration = 0.5
                MyMIDI.addNote(track, channel, degrees, time, duration, volume)
                time += duration

        return MyMIDI

    # -- Testing / FUNCTION Drivers --

    # Build MIDI File
    rhythm_space, time_signature = build_rhythm_space(USER_PRESETS=USER_PRESETS, LOGGER=LOGGER)
    MIDI_file = rock_MIDI(rhythm_space=rhythm_space, time_signature=time_signature, LOGGER=LOGGER)

    # Temp MIDI File Overwrites.
    file_path = 'temp_MIDI_File.mid'

    # Write the MIDI File if the directory exists
    with open(file_path, 'wb') as f:
        MIDI_file.writeFile(f)

    return file_path
