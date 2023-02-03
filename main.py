import bz2
import json

from followutils import utils


folder = 'data'
file_name = 'procurements_contracts_info_2022_12_08.xlsx'
json_filename = 'result/ru-org-comp-cont.ftm.json.bzip'

original_data = utils.read_source_data(folder, file_name)

preprocessed_data = utils.preprocess_organisation(original_data)
preprocessed_data = utils.preprocess_company(preprocessed_data)
preprocessed_data = utils.preprocess_contract(preprocessed_data)


organization = utils.generate_enitites(preprocessed_data['organization'], utils.create_organization)
company = utils.generate_enitites(preprocessed_data['company'], utils.create_company)
contracts = utils.generate_enitites(preprocessed_data['contract'], utils.create_contract)

data = organization + company + contracts
items = [i.to_dict() for i in data]

json_str = json.dumps(items) + "\n"
json_bytes = json_str.encode('utf-8')

with bz2.open(json_filename, 'w') as fout:
    fout.write(json_bytes)


