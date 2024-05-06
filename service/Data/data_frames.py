import pandas as pd

def get_stopwords():
    # Define the file path for stop words
    stop_words_file_path = "service/Data/Data_sets/Sinhala-Stopword-list-master/stop words.txt"

    # Read stop words from the file
    with open(stop_words_file_path, 'r', encoding='utf-8') as file:
        stop_words_content = file.readlines()

    # Split each line by spaces and create a list of stop words
    stop_words_list = [line.strip() for line in stop_words_content]

    # Convert the list of stop words into a DataFrame
    Stop_word = pd.DataFrame(stop_words_list, columns=['Stop_words'])
    return Stop_word

def get_pos_data():
    # Define the file path for POS data
    pos_data_file_path = "service/Data/Data_sets/Sinhala-POS-Data-master/sinhala_pos_data.txt"

    # Read POS data from the file
    with open(pos_data_file_path, 'r', encoding='utf-8') as file:
        pos_data = file.readlines()

    # Initialize lists to store words and tags
    words = []
    tags = []

    # Process each line in the file
    for line in pos_data:
        # Split the line into words and tags
        line_data = line.strip().split()

        # Check if the line has both word and tag
        if len(line_data) == 2:
            words.append(line_data[0])
            tags.append(line_data[1])

    # Create a DataFrame for POS data
    postag_df = pd.DataFrame({'words': words, 'tags': tags})
    return postag_df

def get_final_verb():
    Last_verb = pd.read_csv('service/Data/Data_sets/Final_verb/Last_passive_verbs.csv')
    return Last_verb