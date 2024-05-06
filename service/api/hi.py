from flask import request, jsonify

from service.ML.sentence_identification import sentence_decom
def hello():  # put application's code here
    return 'Hello World!'

def decompose_sentence(postag_df):
    # Get the JSON data from the request
    request_data = request.get_json()

    # Extract the sentence from the JSON data
    sentence = request_data.get('sentence')

    # Perform sentence decomposition
    subject, s_object, verb = sentence_decom(sentence,postag_df)

    # Return the decomposition result as JSON
    return jsonify({
        'subject': subject,
        'object': s_object,
        'verb': verb
    })


def decompose_seence(postag_df):
    # Get the JSON data from the request
    request_data = request.get_json()

    # Extract the sentence from the JSON data
    sentence = request_data.get('sentence')

    # Perform sentence decomposition
    subject, s_object, verb = sentence_decom(sentence,postag_df)

    # Return the decomposition result as JSON
    return jsonify({
        'subject': subject,
        'object': s_object,
        'verb': verb
    })