import pandas as pd
import logging

from service.Modules.Sentence_identification_module.sentence_identification import extract_gender_number, extract_person
from service.Modules.Sentence_identification_module.sinmorphic import get_sinhala_morphology

sinhala_sounds_active = ["වෝ", "යෝ", "හු"]
sinhala_sounds_pasive = ["යන්", "ඉන්", "අන්", "වන්", "න්"]

def correct_sentence(s_subject, s_object, verb_tag, tense, person, number, x, pronun, postag_df):
    # Correct the subject and object using provided functions
    subject = correct_subject(s_subject, pronun, postag_df)
    object_out = correct_object(s_object, pronun, postag_df)

    # Initialize verb_out
    verb_out = None

    # Extract the verb part from the description
    if 'description' in verb_tag.columns:
        descriptions = verb_tag['description']
        for description in descriptions:
            verb_out = extract_verb_part(description)
            if verb_out:
                break  # Exit the loop if a valid verb part is found
    else:
        print("'description' column does not exist")

    # Ensure verb_out is valid
    if verb_out is None:
        print("verb_out is None")
        return subject, object_out, None

    # Ensure required columns exist
    required_columns = ['tense', 'person', 'P/S']
    if not all(col in x.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in x.columns]
        logging.error(f"Missing columns in DataFrame x: {missing_cols}")
        return subject, object_out, None

    tense = set_tense(tense)
    person = set_person(person)
    number = set_number(number)

    # Find matching rows in the DataFrame `x`
    matches = x[
        (x['tense'] == tense) &
        (x['person'] == person) &
        (x['P/S'] == number)
    ]

    # Create the Y string with values combined by "/"
    if not matches.empty:
        y_string = "/".join(matches['Veb'])
    else:
        y_string = "No match found"

    # Combine the verb_out with "නු " and append the Y string
    final_verb_out = f"{verb_out}නු {y_string}"

    return subject, object_out, final_verb_out

def set_tense(tense):
    if tense == "Past":
        return 'Past'
    elif tense == "Presesnt":
        return "Presesnt"
    elif tense == "Present or Future":
        return "Presesnt"

def set_number(number):
    if number == "Singular":
        return 'S'
    elif number == "Plural":
        return "P"

def set_person(person):
    if person == "First Person":
        return 1
    elif person == "Second Person":
        return 2
    elif person == "Third Person":
        return 3

def correct_subject(s_subject, pronun, postag_df):
    # Get the morphology of the subject
    subject_tag = get_sinhala_morphology(s_subject)
    subject_tag = pd.DataFrame(subject_tag)

    # Extract information from the subject_tag DataFrame
    if 'description' in subject_tag.columns:
        subject_tag[['gender', 'number']] = subject_tag['description'].apply(
            lambda x: pd.Series(extract_gender_number(x)))
        gender = subject_tag['gender'].iloc[0]  # Get the first element of the Series
        number = subject_tag['number'].iloc[0]  # Get the first element of the Series
    else:
        # If 'description' column is not found, set default values
        gender = None
        number = None

    person = extract_person(s_subject, pronun)
    row = pronun[pronun['Noun'] == s_subject]
    if not row.empty:
        # Determine the string description based on the 'Person' value
        if person == "First Person":
            if number == "Singular":
                return "මා"
            elif number == "Plural":
                return "අප"
        elif person == "Second Person":
            if number == "Singular":
                return "තොප"
            elif number == "Plural":
                return "තොපි/නුඹලා"
        elif person == "Third Person":
            if number == "Singular":
                if gender == "Masculine":
                    return "ඔහු"
                elif gender == "Feminine":
                    return "ඇය"
            elif number == "Plural":
                return "ඔවුන්"
        else:
            return "Unknown Subject"
    else:
        if 'description' in subject_tag.columns:
            for description in subject_tag['description']:
                sub_out = third_person_sub_correct(s_subject,description, postag_df)
                if sub_out:
                    return sub_out
        else:
            print("'description' column does not exist")

def correct_object(s_subject, pronun, postag_df):
    # Get the morphology of the subject
    subject_tag = get_sinhala_morphology(s_subject)
    subject_tag = pd.DataFrame(subject_tag)

    # Extract information from the subject_tag DataFrame
    if 'description' in subject_tag.columns:
        subject_tag[['gender', 'number']] = subject_tag['description'].apply(
            lambda x: pd.Series(extract_gender_number(x)))
        gender = subject_tag['gender'].iloc[0]  # Get the first element of the Series
        number = subject_tag['number'].iloc[0]  # Get the first element of the Series
    else:
        # If 'description' column is not found, set default values
        gender = None
        number = None

    person = extract_person(s_subject, pronun)
    row = pronun[pronun['Noun'] == s_subject]
    if not row.empty:
        # Determine the string description based on the 'Person' value
        if person == "First Person":
            if number == "Singular":
                return "මම"
            elif number == "Plural":
                return "අපි"
        elif person == "Second Person":
            if number == "Singular":
                return "තෝ/තී"
            elif number == "Plural":
                return "තොපි/නුඹලා"
        elif person == "Third Person":
            if number == "Singular":
                if gender == "Masculine":
                    return "ඔහු/හේ/හෙතෙම"
                elif gender == "Feminine":
                    return "ඇය/ඈ"
            elif number == "Plural":
                return "ඔවුහු"
        else:
            return "Unknown Subject"
    else:
        if 'description' in subject_tag.columns:
            for description in subject_tag['description']:
                ob_out = third_person_ob_correct(s_subject,description, postag_df)
                if ob_out:
                    return ob_out
        else:
            print("'description' column does not exist")

logging.basicConfig(level=logging.DEBUG)

def extract_verb_part(description):
    try:
        # Split the string by tab to separate the parts
        parts = description.split('\t')

        # Ensure there are at least two parts before proceeding
        if len(parts) < 2:
            logging.error(f"Invalid description format: {description}")
            return None

        # Get the part before the first '+'
        verb_part = parts[1].split('+')[0]
        return verb_part
    except Exception as e:
        logging.exception("Error extracting verb part")
        return None

def third_person_ob_correct(s_subject,description, postag_df):
    try:
        # Split the string by tab to separate the parts
        parts = description.split('\t')

        # Ensure there are at least two parts before proceeding
        if len(parts) < 2:
            logging.error(f"Invalid description format: {description}")
            return None

        # Get the part before the first '+'
        ob_part = parts[1].split('+')[0]
        morphology_list = get_sinhala_morphology(ob_part)

        # Loop through all descriptions in morphology_list
        for morphology in morphology_list:
            description = morphology['description']

            # Split the description string based on the tab character ('\t')
            parts = description.split('\t')
            # Check if the word is in the 'words' column
            # Take the second part which contains the desired information
            desired_part = parts[2]
            if "ACC" in desired_part:
                return ob_part

        # Create new combinations of ob_part with sinhala_sounds_active elements
        new_combinations = [ob_part + sound for sound in sinhala_sounds_active]

        # Check if any new combination is in the 'words' column
        for combination in new_combinations:
            is_in_df = combination in postag_df['words'].values
            if is_in_df:
                return combination

    except Exception as e:
        logging.exception("Error extracting verb part")
        return s_subject

def third_person_sub_correct(s_subject,description, postag_df):
    try:
        # Split the string by tab to separate the parts
        parts = description.split('\t')

        # Ensure there are at least two parts before proceeding
        if len(parts) < 2:
            logging.error(f"Invalid description format: {description}")
            return None

        # Get the part before the first '+'
        sb_part = parts[1].split('+')[0]
        morphology_list = get_sinhala_morphology(sb_part)

        # Loop through all descriptions in morphology_list
        for morphology in morphology_list:
            description = morphology['description']

            # Split the description string based on the tab character ('\t')
            parts = description.split('\t')
            # Check if the word is in the 'words' column
            # Take the second part which contains the desired information
            desired_part = parts[1]
            if "NOM" in desired_part:
                return sb_part

        # Create new combinations of sb_part with sinhala_sounds_pasive elements
        new_combinations = [sb_part + sound for sound in sinhala_sounds_pasive]

        # Check if any new combination is in the 'words' column
        for combination in new_combinations:
            is_in_df = combination in postag_df['words'].values
            if is_in_df:
                return combination

    except Exception as e:
        logging.exception("Error extracting verb part")
        return s_subject
