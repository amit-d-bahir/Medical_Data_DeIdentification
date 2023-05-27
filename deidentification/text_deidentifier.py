from datetime import timedelta
from random import randint

import pandas as pd
from spacy.matcher.phrasematcher import PhraseMatcher

from deidentification.utils import extract_regex


# ** Inputs **
#    -> Input string i.e Original String
#    -> Trained en_core_web_sm spacy model
#    -> Blank spacy model
#    -> Choices(2)
#       -> 1. To remove dates completely from the EHR
#       -> 2. To shift dates present in the EHR to have a time domain for research purposes

def text_deidentifier(input_string, nlp_trained_model, nlp_blank_model, choice):
    # doc = nlp_trained_model((open(input_string)).read())
    doc = nlp_trained_model(input_string)
    # original_string = open((input_string)).read()
    original_string = input_string

    # ** Calling extract_regex function to get list of all the matched regex pattern **
    date_list = extract_regex(r"\D([0-9]{4}|[0-9]{1,2})(\/|-)[0-9]{1,2}(\/|-)([0-9]{1,2}|[0-9]{4})\D",
                              doc, original_string)

    for i in range(len(date_list)):
        date_list[i][1] = date_list[i][1] + 1
        date_list[i][2] = date_list[i][2] - 1
        date_list[i][0] = original_string[date_list[i][1]: date_list[i][2]]

    # ** For choice 1 **
    """if(choice == 1):
        for a in date_list:
            count = 0
            for i in range(a[1], a[1] + 4):
                if(original_string[i].isnumeric()):
                    count = count + 1
            if(count == 4):
                original_string=original_string[:a[1]+4]+''*(a[2]-a[1]-4)+original_string[a[2]:]
            else:
                count = 0
                for j in range(a[2], a[2]-5, -1):
                    if(original_string[j].isnumeric()):
                        count = count + 1
                if(count == 4):
                    original_string=original_string[:a[1]]+''*(a[2]-a[1]-4)+original_string[a[2]-4:]
                elif(count == 3):
                    original_string=original_string[:a[1]]+''*(a[2]-a[1]-2)+original_string[a[2]-2:]
                else:
                    original_string=original_string[:a[1]]+''*(a[2]-a[1])+original_string[a[2]:]

    """
    # ** For Choice 2 **
    date_shift = []
    temp_1 = 0
    temp_2 = 0
    random_value = randint(0, 90)
    if choice == 2:
        for temp in range(len(date_list)):
            temp_list = []
            text = date_list[temp][0]
            start = date_list[temp][1] + temp_2
            end = date_list[temp][2] + temp_2
            # Converting dates to pandas datetime so as to use timedelta function
            pandas_date = pd.to_datetime(text, errors='ignore')
            if type(pandas_date) != str:
                pandas_date = pandas_date + timedelta(days=random_value)
                original_string = original_string[:start] + str(pandas_date)[:-9] + original_string[end:]
                temp_2 = temp_2 + (len(str(pandas_date)[:-9]) - len(text))
                temp_list.append(str(pandas_date)[:-9])
                temp_list.append(start)
                temp_list.append(start + len(str(pandas_date)[:-9]))
                date_shift.append(temp_list)

    # ** Extracting all various identifiers using regex pattern **
    # dob_list = extract_regex(r"^(0[1-9]|1[012])[-/.](0[1-9]|[12][0-9]|3[01])[-/.](19|20)\\d\\d$",
    #                         doc, original_string)

    aadhar_list = extract_regex(r"(\d{4}(\s|\-)\d{4}(\s|\-)\d{4})", doc, original_string)

    ssn_list = extract_regex(r"^\d{9}$", doc, original_string)

    mail_list = extract_regex(
        r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|(?:["
        r"\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:["
        r"a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}("
        r"?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:["
        r"\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
        doc, original_string)

    ip_list = extract_regex(r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
                            doc, original_string)

    # ** Now de-identifying them **
    # for a in dob_list:
    #    original_string = original_string[:a[1]]+'X'*(a[2]-a[1])+original_string[a[2]:]

    for a in aadhar_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    for a in ssn_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    for a in mail_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    for a in ip_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    # ** Now to extract urls and licence plate numbers from last updated original_string
    #    and then deidentifying them too **
    doc = nlp_trained_model(original_string)
    url_list = extract_regex(
        r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,"
        r"5})?(\/.*)?",
        doc, original_string)

    license_plate_list = extract_regex(r"[A-Z]{2}[ -][0-9]{1,2}(?: [A-Z])?(?: [A-Z]*)? [0-9]{4}",
                                       doc, original_string)

    for a in ip_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    for a in ip_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    # ** Now to extract contact details i.e phone numbers and fax numbers from last updated
    #    original_string and then deidentifying them too **
    doc = nlp_trained_model(original_string)
    # indian_ph_no = extract_regex(r"((\+*)((0[ -]+)*|(91 )*)(\d{12}+|\d{10}+))|\d{5}([- ]*)\d{6}",
    #                               doc, original_string)

    usa_ph_no = extract_regex(r"^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$",
                              doc, original_string)

    phone_fax_list1 = extract_regex(
        r"(?:(?:(?:(\+)((?:[\s.,-]*[0-9]*)*)(?:\()?\s?((?:[\s.,-]*[0-9]*)+)(?:\))?)|(?:(?:\()?(\+)\s?((?:[\s.,"
        r"-]*[0-9]*)+)(?:\))?))((?:[\s.,-]*[0-9]+)+))",
        doc, original_string)

    phone_fax_list2 = extract_regex(r"\D(\+91[\-\s]?)?[0]?(91)?[789]\d{9}\D",
                                    doc, original_string)

    for i in range(len(phone_fax_list2)):
        phone_fax_list2[i][1] = phone_fax_list2[i][1] + 1
        phone_fax_list2[i][2] = phone_fax_list2[i][2] - 1
        phone_fax_list2[i][0] = original_string[phone_fax_list2[i][1]:phone_fax_list2[i][2]]

    phone_fax_list = []
    for a in phone_fax_list1:
        phone_fax_list.append(a)
    for a in phone_fax_list2:
        phone_fax_list.append(a)

    for a in phone_fax_list1:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    for a in phone_fax_list2:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    # for a in indian_ph_no:
    #    original_string = original_string[:a[1]]+'X'*(a[2]-a[1])+original_string[a[2]:]

    for a in usa_ph_no:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    # ** Extracting account details and other identification details and deidentifying them**
    doc = nlp_trained_model(original_string)

    pan_list = extract_regex(r"[A-Z]{5}\d{4}[A-Z]{1}", doc, original_string)

    passport_list = extract_regex(r"[A-Z]{1}\d{7}", doc, original_string)

    account_and_serial_list = extract_regex(r"\d{9,18}", doc, original_string)

    credit_card_list = extract_regex(r"\d{5}(\s|\-)\d{5}(\s|\-)\d{5}|\d{4}(\s|\-)\d{4}(\s|\-)\d{4}(\s|\-)\d{4}",
                                     doc, original_string)

    for a in pan_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    for a in passport_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    for a in account_and_serial_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    for a in credit_card_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    # ** Extracting MRN(Medical Report Number) if present and assumning it to be 7 digit**
    doc = nlp_trained_model(original_string)
    mrn_list = extract_regex(r"\d{7}", doc, original_string)

    for a in mrn_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    # Now we've deidentified all the details except address

    # ** For extracting address we use a list of address_identifiers for addresses smaller
    #    than street names and match them with every element in spacy doc object.
    #    Matched object are then added to our address_list **

    address_identifier = ['st', 'niwas', 'aawas', 'palace', 'road', 'block', 'gali', 'sector',
                          'flr', 'floor', 'path', 'near', 'oppo', 'bazar', 'house', 'nagar',
                          'bypass', 'bhawan', 'street', 'rd', 'sq', 'flat', 'lane', 'gali',
                          'circle', 'bldg', 'ave', 'mandal', 'avenue', 'tower', 'nagar', 'marg',
                          'chowraha', 'lane', 'heights', 'plaza', 'park', 'garden', 'gate', 'villa',
                          'market', 'apartment', 'chowk']

    doc = nlp_trained_model(original_string)
    address_list = []

    for i in doc:
        if len(i) > 1 and '\n' not in str(i):
            if str(i).lower() in address_identifier:
                address_list.append(i)

    # ** Now to remove the identified addresses after getting their position in og_string
    address_index = []
    temp_2 = 0
    length = len(original_string)
    for i in address_list:
        while 1:
            index = original_string.find(str(i), temp_2, length)
            if index == -1:
                break
            if index != 0 and index != length:
                if ((original_string[index - 1].isalpha() or
                     original_string[index + len(str(i))].isalpha())):
                    temp_2 = index + len(str(i))
                else:
                    break
        address_index.append(index)
        temp_2 = index + len(str(i))

    temp_1 = 0
    new_address_list = []
    if address_index:
        temp_1 = address_index[0]
        a = []
        for b in address_index:
            if b - temp_1 < 20:
                a.append(b)
                temp_1 = b
            else:
                new_address_list.append(a)
                a = [b]
                temp_1 = b
        new_address_list.append(a)

    # ** Removing the complete word in which the addres_identifier was used **
    addr_list = []
    for a in new_address_list:
        flag = []
        j = a[0]
        while j != -1 and original_string[j] not in [',', '\n', '.', ';']:
            j = j - 1
        startt = j
        index_1 = startt
        count = 8
        while count and j != -1 and original_string[j] != '\n':
            if original_string[j].isdigit():
                startt = j
            j = j - 1
            count = count - 1
        j = a[-1]
        # print(j)
        while j != -1 and original_string[j] not in [',', '\n', '.', ';']:
            j = j + 1
        endd = j
        index_2 = endd
        count = 7
        while count and j != length and original_string[j] != '\n':
            if original_string[j].isdigit():
                endd = j
            j = j + 1
            count = count - 1

        if (original_string[index_1] != '.' or original_string[index_2] != '.') and (index_2 - index_1) < 50:
            if original_string[startt] == '\n':
                startt = startt + 1
            if original_string[endd] == '\n':
                endd = endd - 1
            flag.append(original_string[startt:endd + 1])
            flag.append(startt)
            flag.append(endd)
            addr_list.append(flag)

    for a in addr_list:
        original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    # ** After deidentifying all these details we are now left with only names, dates, age
    #    which cannot be identified by regular expression **

    # To extract dates we use spacy's pre-trained en_core_web_sm model along with
    # some modifications to the default model according to our requirements

    time_identifier = ['YEAR', 'YEARS', 'AGE', 'AGES', 'MONTH', 'MONTHS', 'DECADE',
                       'CENTURY', 'WEEK', 'DAILY', 'DAY', 'DAYS', 'NIGHT',
                       'NIGHTS', 'WEEKLY', 'MONTHLY', 'YEARLY']

    doc_1 = nlp_trained_model(original_string)
    new_date_list = []
    for entities in doc_1.ents:
        if str(entities.text).count('X') < 2:
            date = []
            if (entities.label_ == 'DATE' and
                    (sum([True if i not in
                                  original_string[entities.start_char:entities.end_char].upper()
                          else False for i in time_identifier]) == len(time_identifier)) and
                    (entities.end_char - entities.start_char) > 4 and
                    sum(c.isdigit() for c in original_string[entities.start_char:entities.end_char]) >= 1 and
                    sum(c.isalpha() for c in original_string[entities.start_char:entities.end_char]) >= 1):
                date.append(entities.text)
                date.append(entities.start_char)
                date.append(entities.end_char)
                new_date_list.append(date)

    for a in new_date_list:
        count = 0
        for i in range(a[1], a[1] + 4):
            if original_string[i].isnumeric():
                count = count + 1
        if count == 4:
            original_string = original_string[:a[1] + 4] + 'X' * (a[2] - a[1] - 4) + original_string[a[2]:]
        else:
            count = 0
            for j in range(a[2], a[2] - 5, -1):
                if original_string[j].isnumeric():
                    count = count + 1
                if count == 4:
                    original_string = original_string[:a[1]] + 'X' * (a[2] - a[1] - 4) + original_string[a[2] - 4:]
                elif count == 3:
                    original_string = original_string[:a[1]] + 'X' * (a[2] - a[1] - 2) + original_string[a[2] - 2:]
                else:
                    original_string = original_string[:a[1]] + 'X' * (a[2] - a[1]) + original_string[a[2]:]

    final_date_list = []
    if choice == 1:
        for a in new_date_list:
            final_date_list.append(a)
        for a in new_date_list:
            final_date_list.append(a)

    # final_date_list contains all the dates we extracted including regex and spacy model

    # ** Now going for age part, we use the spacy's phrasematcher
    #    which takes input as patterns we want to match and
    #    outputs the start and end index of matched pattern **

    age_list = []
    try:
        matcher = PhraseMatcher(nlp_trained_model.vocab, attr="SHAPE")
        age_identifier = ['YEAR', 'YEARS', 'Y/O', 'AGES', 'AGE', 'Y.O', 'Y.O.', 'AGED', 'AGE IS']

        # Process phrases using the trained SpaCy model (nlp)
        phrases = [
            "76 year old", "aged 58", "aged 123", "54 y/o", "age is 59", "123 y/o", "ages 35", "age 45",
            "ages 123", "age 123", "54 years old", "124 years old", "41 y.o.", "123 y.o.", "113 year old"
        ]
        phrase_docs = [nlp_blank_model(phrase) for phrase in phrases]
        # Add phrases to the PhraseMatcher
        for phrase_doc in phrase_docs:
            matcher.add("age", None, phrase_doc)

        doc = nlp_blank_model(original_string)
        for match_id, start, end in matcher(doc):
            if (sum([True if i in str(doc[start:end]).upper()
                     else False for i in age_identifier]) >= 1):
                a = []
                for i in range(start, end):
                    if str(doc[i:i + 1]).isnumeric() and int(str(doc[i:i + 1])) > 89:
                        result = str.find(str(doc[start:end]))
                        count = 0
                        for j in range(result, result.len(str(doc[start:end]))):
                            if original_string[j:j + 1].isnumeric() and count == 0:
                                sstart = j
                            if original_string[j:j + 1].isnumeric():
                                count = count + 1
                        a.append(original_string[sstart:sstart + count])
                        a.append(sstart)
                        a.append(sstart + count)
                        age_list.append(a)
                        original_string = original_string[:sstart] + 'X' * count + original_string[sstart + count:]
    except:
        print("Error occurred for Age deidentification")

    # ** Last step is packing all the extracted pattern in a dict
    info_dict = {'date': final_date_list, 'aadhar': aadhar_list, 'ssn': ssn_list, 'mail': mail_list, 'ip': ip_list,
                 'url': url_list, 'licence_plate': license_plate_list, 'usa_ph_no': usa_ph_no,
                 'phone_fax': phone_fax_list, 'pan': pan_list, 'passport': passport_list,
                 'account_details': account_and_serial_list, 'credit_card': credit_card_list, 'age': age_list,
                 'address': addr_list, 'medical_report_no': mrn_list, 'date_shift': date_shift}
    # info_dict['dob'] = dob_list
    # info_dict['indian_ph_no'] = indian_ph_no

    shift = random_value

    if choice == 1:
        return original_string, info_dict, None
    else:
        return original_string, info_dict, shift
