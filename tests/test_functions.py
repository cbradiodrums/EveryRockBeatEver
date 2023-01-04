# import pytest

from EveryRockBeatEver.functions import parse_user_preset, generate_MIDI
from EveryRockBeatEver.views import HTML_FORM_FIELDS as HFF
from EveryRockBeatEver.views import USER_PRESETS_TEMPLATE as UPT
import itertools
import random
from copy import deepcopy
from pprint import pprint
from fractions import Fraction as Fr


# from EveryRockBeatEver.db import get_db


def test_parse_user_forms():
    """ IN: Every Submission Permutation
        OUT: Assert USER_PRESETS is preserved and accurate"""

    def build_assert_submit_form(scenario: str = '', exclude: list = None, feed_form: list = None,
                                 early_kill: int = 0, print_stmnt: bool = None):
        """ IN: Scenario (place holder), Exclude(list of values NOT submitted),
                early_kill ('0' ignores), print_stmnt(print any check values)
            OUT: Scenario, Batches, and Tests Conducted """
        # Build 'Form Submit' Permutations from Random Modifiers (randomize.html)
        form_master, form_keys, form_values = {}, [], []  # Instantiate Dictionary

        for key in HFF:
            form_keys = []
            for sub_key in HFF[key]:
                if sub_key not in exclude:
                    form_keys.append(sub_key)
                    form_list = []
                    for low_key in HFF[key][sub_key][0]['MODIFIERS']:
                        for value in HFF[key][sub_key][0]['MODIFIERS'][low_key]:
                            form_list.append(value)
                    form_values.append(form_list)
                form_master.update({key: form_keys})

        # Construct Every Permutation for List of Lists:
        form_permutations = [s for s in itertools.product(*form_values)]

        # Assemble 'Form Submit' Permutation Dictionaries (randomize.html)
        # Build Master Keys / Value List: { stepx[]|stepx_attribute|RandomModifier }
        form_submit = []
        for form_input in form_permutations:
            form_idx = 0
            while form_idx < len(form_input):
                form = []
                for master, key in form_master.items():
                    for sub_key in key:
                        form.append(f'{master}|{sub_key}|{form_input[form_idx]}')
                        form_idx += 1
                form_submit.append(form)

        # If there are particular custom test parameters:
        if feed_form:
            for form in feed_form:
                form_submit.append(form)

        # Feed Dictionary List; Assure USER PRESETS and SAVED USER PRESETS matches
        test_record, batch_record = [], []
        test, batch = 0, 0  # Early Kill { "0": Don't Kill, "X": Run X Tests > 0 }
        for form in form_submit:
            batch += 1
            if batch < early_kill or early_kill == 0:
                test = 0
                print(f'\n==== Scenario: {scenario}, Batch #{batch}, Total Test Forms: {len(form_submit)} ====\n'
                      f'Submit form: {form}')  # VERIFY!!
                UP_Parsed, UP_Saved = parse_user_preset(form_submit=form, print_stmnt=print_stmnt,
                                                        HFF=HFF, USER_PRESETS_UPLOAD=UPT)
                # Split the form into 3 callable lists:
                form_masters, form_keys, form_values = [], [], []
                for submit in form:
                    f_master, f_key, f_val = submit.split('|')[0], submit.split('|')[1], submit.split('|')[2]
                    form_masters.append(f_master)
                    form_keys.append(f_key)
                    form_values.append(f_val)

                # Preserve order of assertion. Assess **Random All** > Random Step > Custom Step
                if 'random_all' in form_keys:
                    rall_idx = form_keys.index('random_all')

                    # If Random All is 'ANY', anything can happen
                    if form_values[rall_idx] == 'ANY':
                        test += 2
                        assert UP_Saved['random_all[]']['random_all'] == form_values[rall_idx]
                        assert UP_Parsed['random_all[]']['random_all'] == form_values[rall_idx]

                        # Let's make certain the submitted 'ANY' values were actually parsed:
                        for key in form_keys:
                            if key[5:] == '_random':
                                test += 1
                                assert UP_Parsed[f'{key[:5]}[]'][key] != form_values[rall_idx]

                    # If Random All is any other Random Modifier
                    elif form_values[rall_idx] not in ['Custom', 'ANY']:
                        test += 2
                        assert UP_Saved['random_all[]']['random_all'] == form_values[rall_idx]
                        assert UP_Parsed['random_all[]']['random_all'] == form_values[rall_idx]

                        # Verify each random step was PARSED correctly
                        for key in form_keys:
                            if key[5:] == '_random':
                                test += 1
                                assert UP_Parsed[f'{key[:5]}[]'][key] == form_values[rall_idx]

                            # Verify each assignable step resides in its respective Modifier Bucket:
                            elif key not in ['random_all', 'step2_partial_map']:
                                test += 1
                                assert UP_Parsed[f'{key[:5]}[]'][key] in \
                                       HFF[f'{key[:5]}[]'][key][0][form_values[rall_idx]]

                    # If Random All was Custom, we will verify that and pursue at the random step level
                    elif form_values[rall_idx] == 'Custom':
                        test += 2
                        assert UP_Saved['random_all[]']['random_all'] == form_values[rall_idx]
                        assert UP_Parsed['random_all[]']['random_all'] == form_values[rall_idx]

                # If Random All wasn't submitted, verify it was left alone
                elif 'random_all' not in form_keys:
                    test += 2
                    assert UP_Saved['random_all[]']['random_all'] == 'None'
                    assert UP_Parsed['random_all[]']['random_all'] == 'None'

                    # Preserve order of assertion. Assess Random All > **Random Step** > Custom Step
                    for key in form_keys:
                        if key[5:] == '_random':
                            rstep_idx = form_keys.index(key)
                            master = f'{key[:5]}'
                            test += 2
                            assert UP_Saved[f'{key[:5]}[]'][key] == form_values[rstep_idx]
                            assert UP_Parsed[f'{key[:5]}[]'][key] == form_values[rstep_idx]

                            # If Random Step is 'ANY', anything can happen
                            if form_values[rstep_idx] == 'ANY':
                                test += 2
                                assert UP_Saved[f'{master}[]'][key] == form_values[rstep_idx]
                                assert UP_Parsed[f'{master}[]'][key] == form_values[rstep_idx]

                                # Let's make certain the submitted 'ANY' values were actually parsed:
                                for sub_key in form_keys:
                                    if sub_key[:5] == master and sub_key != f'{master}_random':
                                        rstep_idx = form_keys.index(sub_key)
                                        test += 1
                                        assert UP_Parsed[f'{master}[]'][sub_key] != form_values[rstep_idx]

                            # If Random Step is any other Random Modifier
                            elif form_values[rstep_idx] not in ['Custom', 'ANY']:
                                test += 2
                                assert UP_Saved[f'{master}[]'][key] == form_values[rstep_idx]
                                assert UP_Parsed[f'{master}[]'][key] == form_values[rstep_idx]

                                # Verify each random step was PARSED correctly
                                for sub_key in form_keys:
                                    if sub_key[:5] == master and sub_key != f'{master}_random':
                                        test += 1
                                        print(f'master: {master} form_values[rstep_idx]: {form_values[rstep_idx]}')
                                        assert UP_Parsed[f'{master}[]'][sub_key] in \
                                               HFF[f'{master}[]'][sub_key][0][form_values[rstep_idx]]

                            # If Random Step was Custom, we will verify that and pursue that and check the form data
                            elif form_values[rstep_idx] in ['Custom', 'None']:
                                test += 2
                                assert UP_Saved[f'{master}[]'][key] == form_values[rstep_idx]
                                assert UP_Parsed[f'{master}[]'][key] == form_values[rstep_idx]

                # Keep track of how many Tests were conducted per Batch
                test_record.append(test)

        print(f'-- Passed {test} tests -- ')

        # FUNCTION(Scenario, Exclude list, early_kill, print)

        # Final Test Result
        batch_record.append(batch)
        print(f'\n\n___&&& PARSE_USER_PRESET [TESTS SUCCESSFULLY PASSED: {sum(test_record)}'
              f' -- OF {sum(batch_record)} BATCHES, IN SCENARIO: {scenario} --] &&&___')
        return sum(test_record), sum(batch_record), scenario

    # Preserve Order of a Submitted Form -> Random All > Random Step > Custom Steps
    all_testing, all_batch, all_test = {}, [], []

    # === Scenario 1: (randomize.html) = Random All + Step1, Step2 Random Modifiers =======================
    exclude = [f'step{step}_random' for step in [1, 3, 4, 5]] + \
              ['step1_partial_palette', 'step2_partial_map']
    tests, batches, scenario = build_assert_submit_form(scenario='1', exclude=exclude,
                                                        early_kill=0, print_stmnt=False)
    # Scenario 1 Stats
    all_testing[scenario] = {'Batches': batches, 'Tests': tests}
    all_batch.append(batches)
    all_test.append(tests)

    # === Scenario 2: (step1.html) = Step1 Custom & Random Modifiers =======================
    exclude = [f'step{step}_random' for step in [2, 3, 4, 5]] + \
              ['step1_partial_palette', 'step2_partial_map', 'random_all']
    tests, batches, scenario = build_assert_submit_form(scenario='2', exclude=exclude,
                                                        early_kill=0, print_stmnt=False)
    # Scenario 2 Stats
    all_testing[scenario] = {'Batches': batches, 'Tests': tests}
    all_batch.append(batches)
    all_test.append(tests)

    # (((*** Testing Summation ***)))
    print(f'\n\n(((*** PARSE_USER_PRESET [TESTS SUCCESSFULLY PASSED: {sum(all_test)}'
          f' -- OF {sum(all_batch)} BATCHES, IN {scenario} SCENARIOS --] ***)))\n{all_testing}\n')


def test_generate_MIDI():
    """ IN: Every Submission Permutation
        OUT: Assert MIDI File Completes """

    # Some following tests have insane permutations; if you want to try the full library, set beefy_computer to True
    beefy_computer = False  # Change at your own risk

    # Build 'USER PRESET' Permutations from Every Possible Category (NO RANDOM MODIFIERS)
    UP_master_step1, UP_keys_step1, UP_values_step1 = {}, [], []  # Instantiate Dictionary
    exclude = [f'step{step}_random' for step in [1, 2, 3, 4, 5]] + \
              ['step1_partial_palette', 'step2_partial_map', 'random_all']

    # Assemble Step 1 Permutations
    for key in HFF:
        UP_keys_step1 = []
        if key[:5] == 'step1':
            for sub_key in HFF[key]:
                if sub_key not in exclude:
                    UP_keys_step1.append(sub_key)
                    value_list = []
                    for low_key in HFF[key][sub_key][0]:
                        if low_key != 'MODIFIERS':
                            for value in HFF[key][sub_key][0][low_key]:
                                value_list.append(f'{key}|{sub_key}|{value}')
                    UP_values_step1.append(value_list)
                UP_master_step1.update({key: UP_keys_step1})

    # Construct Every Permutation for List of Lists:
    step1_permutations = [s for s in itertools.product(*UP_values_step1)]

    # Assemble Step 2 (Full) Permutations 4.92e^53... Just shy of One Septendecillion
    if beefy_computer:
        # First, Assemble the Weight Permutations
        UP_step2_wgts, UP_step2_brks = [], []
        for key in HFF:
            if key[:5] == 'step2':
                for sub_key in HFF[key]:
                    if sub_key == 'step2_partial_map':
                        for deep_key in HFF[key][sub_key][0]['Extreme']:
                            for low_key in HFF[key][sub_key][0]['Extreme'][deep_key]:
                                if low_key == 'WGT':
                                    UP_step2_wgts.append([0, 1])  # Boolean Condition (True / False)

        # Construct Every Permutation for List of Lists:
        step2_wgts_permutations = [s for s in itertools.product(*UP_step2_wgts)]
        print(f'{len(step2_wgts_permutations)} Permutations of Partial Weights')

        # Second, use each Weight Permutations Tuple to construct a new list with Breakabilities
        # **NOTE**: My PC Resources cannot handle this function. Set GigaChad_PC to True to Continue
        GigaChad_PC = False  # Change at your own Risk
        UP_step2_perms = []
        for wgt_perm in step2_wgts_permutations[4:5]:
            temp_perm_list = []
            print(wgt_perm)
            for wgt_item in wgt_perm:
                for key in HFF:
                    if key[:5] == 'step2':
                        for sub_key in HFF[key]:
                            if sub_key == 'step2_partial_map':
                                for deep_key in HFF[key][sub_key][0]['Extreme']:
                                    for low_key in HFF[key][sub_key][0]['Extreme'][deep_key]:
                                        if low_key == 'WGT':
                                            temp_perm_list.append([f'wgt_item: {wgt_item}'])
                                        if low_key == 'BRK':
                                            for brk in HFF[key][sub_key][0]['Extreme'][deep_key][low_key]:
                                                if wgt_item == 0:
                                                    temp_perm_list.append([0])
                                                else:
                                                    temp_perm_list.append([0, 1])
            print(f'temp_perm_list: {temp_perm_list}\n')
            if beefy_computer and GigaChad_PC:
                wgt_brk_perm = [s for s in itertools.product(*temp_perm_list)]
                UP_step2_perms.append(wgt_brk_perm)
        print(len(UP_step2_perms))

    # Assemble Step 2 (Mini) Permutations - Set a limit to determine how many random submissions
    step2_random_submissions = 20  # Partial Map Variations -- 20 yields 110,880 permutations.

    # Collect all step2_partial_map modifier possibilities
    modifier_bucket, modifier_exclude = [], ['ANY']
    for deep_key in HFF['step2[]']['step2_partial_map'][0]['MODIFIERS']:
        for modifier in HFF['step2[]']['step2_partial_map'][0]['MODIFIERS'][deep_key]:
            if modifier not in modifier_exclude:
                modifier_bucket.append(modifier)

    # Randomize the Partial Map Modifier,
    step2_permutations = []
    for pm_mod in range(step2_random_submissions):
        randomization = modifier_bucket[random.randint(0, len(modifier_bucket) - 1)]
        UP_step2_pmap = []
        for note in HFF['step2[]']['step2_partial_map'][0][randomization]:

            # Randomize the Weights to see if we should randomize the Breakabilities
            wgt_random = random.randint(0, 5)
            if wgt_random > 0:

                # If the Partial is typically included in the Step 2 Partial Map Modifier
                # **NOTE** If a Partial WGT > 0 == BRK, that partial would be skipped entirely.
                if HFF['step2[]']['step2_partial_map'][0][randomization][note]['WGT'] == 'True':
                    UP_step2_pmap.append(f'step2[]|step2_partial_map|{note}|WGT|{wgt_random}')
                    for brk in HFF['step2[]']['step2_partial_map'][0][randomization][note]['BRK']:
                        brk_random = random.randint(0, 5)  # Randomize per Breakability

                        # If the Breakability is typically included in the Step 2 Partial Map Modifier
                        if HFF['step2[]']['step2_partial_map'][0][randomization][note]['BRK'][brk] == 'True':
                            UP_step2_pmap.append(f'step2[]|step2_partial_map|{note}|BRK|{brk}|{brk_random}')
        step2_permutations.append(UP_step2_pmap)

    # FINAL: Amalgamate All Step Permutations
    custom_step_permutations = []
    for s2p in step2_permutations:
        for s1p in step1_permutations:
            custom_step_permutations.append(s1p + tuple(s2p))

    print(f"+++[[[ Current test_generate_MIDI Load: {len(custom_step_permutations)} lists ]]]+++")
