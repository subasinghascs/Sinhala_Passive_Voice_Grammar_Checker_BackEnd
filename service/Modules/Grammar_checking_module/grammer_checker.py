from service.Modules.Sentence_identification_module.sinmorphic import get_sinhala_morphology


def Check_oubject(subject,pronun):
    correctness_status = "Incorrect"
    # Find the row in the DataFrame where the 'Noun' column matches the input noun
    row = pronun[pronun['Noun'] == subject]

    # Check if the noun was found in the DataFrame
    if not row.empty:
        # Get the 'Person' value from the matching row
        person_tag = row['active'].values[0]

        # Determine the string description based on the 'Person' value
        if person_tag == 0:
            correctness_status = "Incorrect"
        elif person_tag == 1:
            correctness_status = "Correct"
        elif person_tag == 3:
            correctness_status = "Correct"
        else:
            correctness_status = "Unknown Person"

        return correctness_status
    else:
        morphology_list = get_sinhala_morphology(subject)
        # Extract the description from the first element of morphology_list
        description = morphology_list[0]['description']

        # Split the description string based on the tab character ('\t')
        parts = description.split('\t')

        # Take the second part which contains the desired information
        desired_part = parts[1]
        if "NOM" in desired_part:
            correctness_status = "Correct"
        else:
            correctness_status = "Incorrect"
        return correctness_status


def check_subject(s_suject,pronun):
    correctness_status = 0
    # Find the row in the DataFrame where the 'Noun' column matches the input noun
    row = pronun[pronun['Noun'] == s_suject]

    # Check if the noun was found in the DataFrame
    if not row.empty:
        # Get the 'Person' value from the matching row
        person_tag = row['active'].values[0]

        # Determine the string description based on the 'Person' value
        if person_tag == 0:
            correctness_status = "Correct"
        elif person_tag == 1:
            correctness_status = "Incorrect"
        elif person_tag == 3:
            correctness_status = "Correct"
        else:
            correctness_status = "Unknown Person"

        return correctness_status
    else:
        morphology_list = get_sinhala_morphology(s_suject)
        # Extract the description from the first element of morphology_list
        description = morphology_list[0]['description']

        # Split the description string based on the tab character ('\t')
        parts = description.split('\t')

        # Take the second part which contains the desired information
        desired_part = parts[1]
        if "ACC" in desired_part:
            correctness_status = "Correct"
        else:
            correctness_status = "Incorrect"
        return correctness_status


def check_verb(verb, final_verbs, s_person, s_tense, s_singular):
    correctness_status = "null1"

    # Decompose the input verb into a list of words
    words = verb.split()

    # Initialize state variables
    p_state = 0
    t_state = 0
    s_state = 0

    # Flag to check if any word matches
    match_found = False

    for word in words:
        # Find the row in the DataFrame where the 'Veb' column matches the input word
        row = final_verbs[final_verbs['Veb'] == word]

        # Check if the word was found in the DataFrame
        if not row.empty:
            match_found = True

            # Get the 'Person', 'Tense', and 'P/S' values from the matching row
            person_tag = row['person'].values[0]
            tense_tag = row['tense'].values[0]
            S_tag = row['P/S'].values[0]

            # Check person
            if (person_tag == 1 and s_person == "First Person") or \
               (person_tag == 2 and s_person == "Second Person") or \
               (person_tag == 3 and s_person == "Third Person"):
                p_state = 1

            # Check tense
            if (tense_tag == "Presesnt" and s_tense == "Present or Future") or \
               (tense_tag == "Past" and s_tense == "Past"):
                t_state = 1

            # Check singular/plural
            if (S_tag == "P" and s_singular == "Plural") or \
               (S_tag == "S" and s_singular == "Singular"):
                s_state = 1

            # If all states are correct, return "Correct"
            if p_state == 1 and t_state == 1 and s_state == 1:
                correctness_status = "Correct"
                break
        else:
            # If no match is found, continue to the next word
            continue

    # If no word matches in the DataFrame, set status accordingly
    if not match_found:
        correctness_status = "Verb not found"
    elif correctness_status != "Correct":
        correctness_status = "Incorrect"

    return correctness_status
