import pandas as pd
import re
import requests
import json
from string import ascii_uppercase

alphabet = ascii_uppercase

#   PROVIDES LIST OF LETTERS TO BE USED AS COLUMN HEADINGS FOR SPREADSHEET PREVIEW


def excel_style_letters(length):
    alphabet_length = None
    if (length > 26):
        alphabet_length = length + 1
    else:
        alphabet_length = length
    alphabet_list = [""]
    completedAlphabetLoops = 0
    alphabetIndexIterator = 0
    for i in range(0, alphabet_length):
        letter = ""
        if i % 26 == 0 and i != 0:
            if completedAlphabetLoops > 0:
                letter += alphabet[completedAlphabetLoops - 1]
                letter += alphabet[alphabetIndexIterator]
                alphabet_list.append(letter)
            completedAlphabetLoops += 1
            alphabetIndexIterator = 0
            continue
        if completedAlphabetLoops == 0:
            letter += alphabet[alphabetIndexIterator]
        else:
            letter += alphabet[completedAlphabetLoops - 1]
            letter += alphabet[alphabetIndexIterator]
        alphabet_list.append(letter)
        alphabetIndexIterator += 1
    return alphabet_list


#   CHECKS IF ABN FORMAT IS VALID AND MAKES REQUEST TO ABR WEB SERVICES FOR ENTITY / BUSINESS NAME

guid = "99b768e7-0dd4-44da-a2e2-4305162240a5"


def abn_validator(file_location, first_row_headings, orientation, abn_index):

    # Initialise weighting factor array
    weighting = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    # Initialise some variables
    results_list = []
    entity_name_list = []
    business_name_list = []

    # Open file
    if orientation == 'columns':
        abns = pd.read_excel(file_location, header=None)
    else:
        abns = pd.read_excel(file_location, header=None).swapaxes(
            "index", "columns")

    # Check whether ABN is valid
    for index, abn in enumerate(abns[int(abn_index) - 1]):

        # Initialise sum variable
        sum = 0

        # Add heading to column if first rows are headings
        if index == 0 and first_row_headings == 'on':
            results_list.append('Valid ABN?')
            business_name_list.append('Business Name(s)')
            entity_name_list.append('Entity Name')
            continue

        # Check and convert data type
        if type(abn) == float:
            results_list.append('Invalid - Empty Field')
            business_name_list.append('')
            entity_name_list.append('')
            continue
        elif type(abn) == str:
            digits_extracted = re.sub('[^0-9]', '', abn)
            if digits_extracted:
                converted_abn = int(digits_extracted)
            else:
                results_list.append('Invalid - Field Contains No Integers')
                business_name_list.append('')
                entity_name_list.append('')
                continue
        else:
            converted_abn = abn

        # Convert ABN to list
        abn_list = list(map(int, str(converted_abn)))

        # Check length
        if len(abn_list) != 11:
            results_list.append('Invalid - Incorrect Length')
            business_name_list.append('')
            entity_name_list.append('')
            continue

        # Step 1: Subtract 1 from first digit
        abn_list[0] -= 1

        # Step 2: Multiply each digit by weighting factor
        for index, digit in enumerate(abn_list):
            abn_list[index] *= weighting[index]

        # Step 3: Sum resulting 11 digits
        for digit in abn_list:
            sum += digit

        # Step 4: Is it divisible by 89?
        if sum % 89 == 0:
            results_list.append('Valid')
            ABR = "https://abr.business.gov.au/json/"
            abr_call = "{ABR}AbnDetails.aspx?abn={ABN}&callback=callback&guid={GUID}".format(
                ABR=ABR, ABN=converted_abn, GUID=guid)
            abr_call_error = False
            if not abr_call_error:
                try:
                    r = requests.get(abr_call)
                    response_text = r.text
                    data_json = response_text.split("(", 1)[1].strip(")")
                    abn_dict = json.loads(data_json)
                    if 'GUID' in abn_dict['Message']:
                        abr_call_error = True
                        entity_name_list.append(
                            'An error ocurred communicating with the ABR server. Entity name search cannot be performed at this time.')
                        business_name_list.append(
                            "An error ocurred communicating with the ABR server. Business name search cannot be performed at this time.")
                    elif 'not a valid ABN' in abn_dict['Message']:
                        entity_name_list.append(
                            'The ABR search identified that no entity is registered under this ABN.')
                        business_name_list.append('')
                    else:
                        entity_name_list.append(abn_dict["EntityName"])
                        business_name_list.append(abn_dict["BusinessName"])
                except:
                    abr_call_error = True
                    entity_name_list.append(
                        'An error ocurred communicating with the ABR server. Entity name search cannot be performed at this time.')
                    business_name_list.append(
                        "An error ocurred communicating with the ABR server. Business name search cannot be performed at this time.")
        else:
            results_list.append('Invalid')
            business_name_list.append('')
            entity_name_list.append('')

    # Insert results list into dataframe
    abns.insert(int(abn_index), int(abn_index), results_list, True)
    abns.insert(int(abn_index) + 1, int(abn_index) +
                1, entity_name_list, True)
    abns.insert(int(abn_index) + 2, int(abn_index) +
                2, business_name_list, True)

    if orientation == 'rows':
        abns.swapaxes("index", "columns").to_excel(file_location, index=False, header=False,
                                                   sheet_name='Valid ABN Results')
    else:
        abns.to_excel(file_location, index=False, header=False,
                      sheet_name='Valid ABN Results')
