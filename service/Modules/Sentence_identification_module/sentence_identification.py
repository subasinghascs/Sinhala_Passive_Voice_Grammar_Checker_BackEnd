from service.Modules.Sentence_identification_module.sinmorphic import get_sinhala_morphology
import pandas as pd
from service.Data.data_frames import get_stopwords,get_pos_data
from typing import Optional

# Load POS data and stop words
postag_df = get_pos_data()
Stop_word = get_stopwords()

def combine_consecutive_nouns(df):
    status = 1
    current_noun = None
    for index, row in df.iterrows():
        if status != 1:
            break  # Exit the loop if status is not 1
        word = row['word']
        word_type = row['type']
        if (word_type == 'NOUN' or word_type == 'PRONOUN') and status == 1:
            if current_noun is None:
                current_noun = word
            else:
                current_noun += ' ' + word
        else:
            status = 0
    return current_noun

def combine_consecutive_verb(df):
    status = 1
    current_verb = None
    for index, row in df.iterrows():
        word = row['word']
        word_type = row['type']
        # Check if the word is marked as a verb with "+V"
        if word_type == 'Verb' or '+V+' in row['description']:
            if current_verb is None:
                current_verb = word
                status = 1
            else:
                current_verb += ' ' + word
                status = 1
        else:
            if current_verb is None:
                status = 1
            else:
                current_verb += ' ' + word
                status = 1

    return current_verb


def remove_stop_words(sentence: Optional[str]) -> Optional[str]:
    if sentence is None:
        return None
    words = sentence.split()
    words = [word for word in words if word.lower() not in Stop_word]
    return ' '.join(words)

def split_sentence(sentence):
    keyword = "විසින්"
    if keyword in sentence:
        before_keyword, after_keyword = sentence.split(keyword, 1)
        return before_keyword.strip(), after_keyword.strip(), 1
    else:
        return sentence.strip(), "", 0

def get_tag_for_word(word):
    # Search for the word in the DataFrame
    postag_df =get_pos_data()
    word_row = postag_df[postag_df['words'] == word]

    # If the word is found, return its corresponding tag
    if not word_row.empty:
        return word_row.iloc[0]['tags']
    else:
        return f"No tag found for the word '{word}'."

def extract_nouns(sentence):
    if sentence:
        # Tokenize the sentence into words
        words = sentence.split()

        # Initialize an empty list to store nouns
        nouns = []

        # Iterate through each word in the sentence
        for word in words:
            # Get the tag for the word
            tag = get_tag_for_word(word)

            # If the tag is 'NN' (noun), add the word to the list of nouns
            if tag == 'NNP' or tag =='NNC':
                nouns.append(word)

        # Join the remaining words to form the cleaned sentence
        cleaned_sentence = ' '.join(nouns)

        return cleaned_sentence
    else:
        return None




def sentence_decom(sentence, postag_df):
    try:
        before, after, status = split_sentence(sentence)
        if status == 1:
            before_list = get_sinhala_morphology(before)
            before_df = pd.DataFrame(before_list)
            after_list = get_sinhala_morphology(after)
            after_df = pd.DataFrame(after_list)
            subject = combine_consecutive_nouns(before_df)
            # subject = extract_nouns(subject)
            s_object = combine_consecutive_nouns(after_df)
            s_object = remove_stop_words(s_object)
            verb = combine_consecutive_verb(after_df)
            return subject, s_object, verb
    except IndexError:
        print("Error: List index out of range. Check the data for incomplete or missing rows.")
    return None, None, None


def extract_gender_number(description):
    gender = None
    number = None

    # Check for gender tags
    if '+M' in description:
        gender = 'Masculine'
    elif '+F' in description:
        gender = 'Feminine'
    elif '+N' in description:
        gender = 'Neuter'

    # Check for number tags
    if '+SG' in description:
        number = 'Singular'
    elif '+PL' in description:
        number = 'Plural'

    return gender, number

def extract_tense(verb_tag, Last_verb):
    # Check if the verb in verb_tag is present in Last_verb dataset
    for index, row in verb_tag.iterrows():
        verb = row['word']
        if verb in Last_verb['Veb'].values:
            # Get the tense from Last_verb dataset
            tense = Last_verb[Last_verb['Veb'] == verb]['tense'].iloc[0]
            return tense

    # If verb not found in Last_verb dataset, check description for tense
    for index, row in verb_tag.iterrows():
        description = row['description']
        word_type = row['type']
        if word_type == 'Verb':
            # Check for tense tags in description
            if '+PRS' in description or '+NPST' in description:
                tense = 'Present or Future'
            elif '+PST' in description:
                tense = 'Past'
            elif '+FUT' in description:
                tense = 'Present or Future'
            else:
                # Default to None if tense not found
                tense = None
            return tense

    # Default to None if no verb found
    return None




def extract_person(subject,pronun):
    # Find the row in the DataFrame where the 'Noun' column matches the input noun
    row = pronun[pronun['Noun'] == subject]

    # Check if the noun was found in the DataFrame
    if not row.empty:
        # Get the 'Person' value from the matching row
        person_tag = row['Person'].values[0]

        # Determine the string description based on the 'Person' value
        if person_tag == 1:
            s_person = "First Person"
        elif person_tag == 2:
            s_person = "Second Person"
        elif person_tag == 3:
            s_person = "Third Person"
        else:
            s_person = "Unknown Person"

        return s_person
    else:
        # Return None or a suitable default value if the noun is not found
        return "Third Person"