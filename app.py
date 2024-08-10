import pandas as pd
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from service.Data.data_frames import get_pos_data, get_stopwords, get_final_verb, get_pronun
from service.Modules.Grammar_checking_module.grammer_checker import check_subject, Check_oubject, check_verb
from service.Modules.Sentence_identification_module.sentence_identification import sentence_decom, get_sinhala_morphology, extract_tense, extract_gender_number, extract_person, ex_gender
from service.Modules.Suggesion_genaration.Suggesion_genaration import correct_sentence, correct_object

app = Flask(__name__)
CORS(app)

# Load POS data and stop words
postag_df = get_pos_data()
Stop_word = get_stopwords()
final_verbs = get_final_verb()
pronun = get_pronun()

@app.route('/decompose_sentence', methods=['POST'])
def decompose_sentence():
    request_data = request.get_json()
    sentence = request_data.get('sentence')
    keyword = "විසින්"

    if keyword in sentence:
        subject, s_object, verb = sentence_decom(sentence, postag_df)
        x = check_subject(subject, pronun)
        y = Check_oubject(s_object, pronun)

        verb_tag = get_sinhala_morphology(verb)
        verb_tag = pd.DataFrame(verb_tag)

        subject_tag = get_sinhala_morphology(s_object)
        subject_tag = pd.DataFrame(subject_tag)

        if 'description' in subject_tag.columns:
            description = subject_tag['description']
            subject_tag[['gender', 'number']] = subject_tag['description'].apply(
                lambda x: pd.Series(extract_gender_number(x)))
            gender = subject_tag['gender'].iloc[0]
            number = subject_tag['number'].iloc[0]
        else:
            description, gender, number = None, None, None

        tense = extract_tense(verb_tag, Last_verb=final_verbs)
        person = extract_person(s_object, pronun)
        gender = ex_gender(s_object, pronun)
        z = check_verb(verb, final_verbs, person, tense, number)
        a, b, c = correct_sentence(subject, s_object, verb_tag,tense,person,number,final_verbs, pronun,postag_df)


        decomposition_dict = {
            'object': s_object,
            'subject': subject,
            'verb': verb
        }

        identification_dict = {
            'gender': gender,
            'number': number,
            'tense': tense,
            'person': person
        }

        grammar_checker_dic = {
            'object': y,
            'sufix': "Correct",
            'subject': x,
            'verb': z
        }
        grammar_suggestion_dic = {
            'object': b,
            'subject': a,
            'verb': c
        }

        result_dict = {
            'Sentence_decompose': [decomposition_dict],
            'Sentence_identification': [identification_dict],
            'grammar_checker': [grammar_checker_dic],
            'grammar_suggestion':[grammar_suggestion_dic]
        }

        return jsonify(result_dict)
    else:
        return jsonify({'error': 'Keyword not found'}), 400

if __name__ == '__main__':
    app.run()
