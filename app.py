import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

from service.Data.data_frames import get_pos_data, get_stopwords, get_final_verb
from service.ML.sentence_identification import sentence_decom, get_sinhala_morphology, extract_tense, extract_gender_number

app = Flask(__name__)
CORS(app)

# Load POS data and stop words
postag_df = get_pos_data()
Stop_word = get_stopwords()
final_verbs = get_final_verb()

@app.route('/decompose_sentence', methods=['POST'])
def decompose_sentence():
    # Get the JSON data from the request
    request_data = request.get_json()

    # Extract the sentence from the JSON data
    sentence = request_data.get('sentence')

    # Perform sentence decomposition
    subject, s_object, verb = sentence_decom(sentence, postag_df)

    # Get the morphology of the verb
    verb_tag = get_sinhala_morphology(verb)
    verb_tag = pd.DataFrame(verb_tag)

    # Get the morphology of the subject
    subject_tag = get_sinhala_morphology(s_object)
    subject_tag = pd.DataFrame(subject_tag)

    # Extract information from the subject_tag DataFrame
    # Adjust this part based on the actual structure of the DataFrame
    if 'description' in subject_tag.columns:
        description = subject_tag['description']
        subject_tag[['gender', 'number']] = subject_tag['description'].apply(lambda x: pd.Series(extract_gender_number(x)))
        gender = subject_tag['gender'].iloc[0]  # Get the first element of the Series
        number = subject_tag['number'].iloc[0]  # Get the first element of the Series
    else:
        # If 'description' column is not found, set default values
        description = None
        gender = None
        number = None

    # Extract tense from the verb_tag DataFrame
    tense = extract_tense(verb_tag, Last_verb=final_verbs)

    # Construct decomposition dictionary
    decomposition_dict = {
        'object': s_object,
        'subject': subject,
        'verb': verb
    }

    # Construct identification dictionary
    identification_dict = {
        'gender': gender,
        'number': number,
        'tense': tense
    }

    # Combine decomposition and identification dictionaries
    result_dict = {
        'Sentence_decompose': [decomposition_dict],
        'Sentence_identification': [identification_dict]
    }

    # Return the decomposition result as JSON
    return jsonify(result_dict)



if __name__ == '__main__':
    app.run()
