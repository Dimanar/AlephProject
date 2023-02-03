import ast
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
        .drop(['service', 'guid_contract', 'services'], axis=1) \
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


def preprocess_organisation(dict_dataframe: Dict) -> Dict:
    dataframe = dict_dataframe['original']
    dataframe = dataframe.rename(mapping['organization'], axis=1)

    dataframe = dataframe.drop_duplicates(keep='last')

    dataframe['name'] = dataframe['name'].apply(get_name)
    dataframe['innCode'] = dataframe['innCode'].apply(fix_inn)
    dataframe['okpoCode'] = dataframe['okpoCode'].apply(str)
    dataframe['jurisdiction'] = 'Russia'

    dict_dataframe['organization'] = dataframe

    return dict_dataframe


def preprocess_company(dict_dataframe: Dict) -> Dict:
    dataframe = dict_dataframe['original']
    dataframe = dataframe.rename(mapping['company'], axis=1)

    dataframe = dataframe.drop_duplicates(keep='last')

    dataframe['name'] = dataframe['name'].apply(str.strip)
    dataframe['innCode'] = dataframe['innCode'].apply(fix_inn)
    dataframe['kppCode'] = dataframe[''].apply()
    dataframe['jurisdiction'] = 'Russia'

    dict_dataframe['company'] = dataframe

    return dict_dataframe


def preprocess_contract(dict_dataframe: Dict) -> Dict:
    pass


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


