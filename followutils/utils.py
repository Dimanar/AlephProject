import ast
import re
import pandas as pd

from tqdm import tqdm
from typing import Dict

from followutils.mapper import Mapper
from followutils.entities.organization import Organisation
from followutils.entities.company import Company
from followutils.entities.contract import Contract

mapping = Mapper()


def read_source_data(path: str, file_name: str) -> Dict:
    full_path = f"{path}/{file_name}"
    source_data = {}

    original_data = pd.read_excel(full_path)\
        .drop(['service', 'guid_contract', 'services', 'items'], axis=1) \
        .rename(columns={"Unnamed: 0": 'id'})

    source_data['original'] = original_data

    return source_data


def get_name(row: str) -> str:
    list_name = list(ast.literal_eval(row).values())
    return list_name[0]


def fix_inn(inn: str) -> str:
    inn = str(inn).strip()
    if len(inn) in {9, 11}:
        return '0' + inn
    return inn


def get_kpp(row: str) -> str:
    pattern = re.compile(r"[a-zA-Z][a-zA-Z][a-zA-Z]=[0-9]+\?", re.IGNORECASE)
    kpp = pattern.findall(row)[0]
    return kpp[4:-1]


def preprocess_organisation(dict_dataframe: Dict) -> Dict:
    dataframe = dict_dataframe['original']
    dataframe = dataframe.rename(mapping['organization'], axis=1)
    dataframe = dataframe[mapping['organization'].values()]
    dataframe = dataframe.drop_duplicates('idNumber', keep='last')
    print(dataframe.columns)
    dataframe['name'] = dataframe['name'].apply(get_name)
    dataframe['innCode'] = dataframe['innCode'].apply(fix_inn)
    dataframe['okpoCode'] = dataframe['okpoCode'].apply(str)
    dataframe['jurisdiction'] = 'Russia'

    dict_dataframe['organization'] = dataframe

    return dict_dataframe


def preprocess_company(dict_dataframe: Dict) -> Dict:
    dataframe = dict_dataframe['original']
    dataframe = dataframe.rename(mapping['company'], axis=1)

    dataframe['kppCode'] = dataframe['website'].apply(get_kpp)

    dataframe = dataframe[mapping['company'].values()]
    dataframe = dataframe.drop_duplicates('registrationNumber', keep='last')
    print(dataframe.columns)
    dataframe['name'] = dataframe['name'].apply(str.strip)
    dataframe['registrationNumber'] = dataframe['registrationNumber'].apply(str)
    dataframe['capital'] = dataframe['capital'].apply(str)
    dataframe['innCode'] = dataframe['innCode'].apply(fix_inn)
    dataframe['kppCode'] = dataframe['website'].apply(get_kpp)

    dataframe['jurisdiction'] = 'Russia'

    dict_dataframe['company'] = dataframe

    return dict_dataframe


def preprocess_contract(dict_dataframe: Dict) -> Dict:
    dataframe = dict_dataframe['original']
    dataframe = dataframe.rename(mapping['contract'], axis=1)
    dataframe = dataframe[mapping['contract'].values()]
    dataframe = dataframe.drop_duplicates('procedureNumber', keep='last')
    print(dataframe.columns)
    dataframe['title'] = dataframe['title'].fillna('Предмет: Неизвестная услуга')
    dataframe['contractDate'] = dataframe['contractDate'].fillna('None')
    dataframe['numberAwards'] = dataframe['numberAwards'].apply(str)
    dataframe['type'] = 'S'

    dict_dataframe['contract'] = dataframe

    return dict_dataframe


def create_organization(row):
    org = Organisation(row[mapping['organization'].values()])
    return [org.to_ftm()]


def create_company(row):
    company = Company(row[mapping['company'].values()])
    return [company.to_ftm()]


def create_contract(row):
    contract = Contract(row[mapping['contract'].values()])
    return [contract.to_ftm()]


def generate_enitites(df, entity_func, **kwargs):
    entities = []
    for i, row in tqdm(df.iterrows(), total=len(df)):
        entities += entity_func(row, **kwargs)
    return entities


