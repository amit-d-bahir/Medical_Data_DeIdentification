import pickle

import en_core_web_sm
import spacy
from spacy.tokenizer import Tokenizer

from deidentification.text_deidentifier import text_deidentifier


# ** Creating our EMR/EHR data extractor function that manages de-identification function by taking inputs **
#   -> String
#   -> Choices(2)
#       -> 1. To remove dates completely from the EMR/EHR. todo: explore if this is required
#       -> 2. [DEFAULT CHOICE ]To shift dates present in the EMR/EHR to have a time domain for research purposes

def data_extractor(input_string):
    # ** We've used 2 pickle files as a lookup table to reduce error **
    #    -> Containing all the medical fields
    #    -> Containing names of cities and states of India

    with open('medical_fields.pkl', 'rb') as file:
        medical_field_data = pickle.load(file)

    with open('city_state_of_india.pkl', 'rb') as file:
        city_state_list_data = pickle.load(file)

    # ** Loading spacy's pre trained model **
    nlp_trained_model = en_core_web_sm.load()

    # ** Now loading an en_core_web_sm model
    #    It is a re-trained spacy language model on medical data **
    nlp_re_trained_model = spacy.load('trained_spacy_model')
    # nlp_re_trained_model = spacy.load('last_modified_model')

    # ** Loading a blank spacy model **
    nlp_blank_model = spacy.blank('en')

    choice = 2
    # Calling the de-identifier function
    processed_string, dictionary, date_shift = text_deidentifier(input_string,
                                                                 nlp_trained_model,
                                                                 nlp_blank_model,
                                                                 choice)

    # Now to extract names of PERSON & ORG from the processed_string we use our
    # re-trained spacy model on medical data and along with we de-identify them too

    nlp_tokenizer = Tokenizer(nlp_blank_model.vocab)
    doc = nlp_re_trained_model(processed_string)
    person_org_list = []

    for entities in doc.ents:
        if str(entities.text).count('X') < 2:
            tokens = nlp_tokenizer(str(entities.text))
            if sum([True if str(i).lower() in medical_field_data or '\n' in str(i) or
                    str(i).lower() in city_state_list_data else False for i in tokens]) != len(tokens):
                pre_list_for_p_org = [entities.text, entities.start_char, entities.end_char]
                person_org_list.append(pre_list_for_p_org)

    # dictionary = {}
    dictionary['person_&_org'] = person_org_list

    # Now de-identifying it by 'X'
    for a in person_org_list:
        processed_string = processed_string[:a[1]] + 'X' * (a[2] - a[1]) + processed_string[a[2]:]

    # ** Returning processed_string, dictionary and date_shift **
    return processed_string
