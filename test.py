from followthemoney import model
import pandas as pd

# Read the sample data
companies = pd.read_csv('~/Companies.csv', nrows=100000, keep_default_na=False)
companies = companies[companies['relatedToRussia'] == 'Yes']  # let's test at more interesting subset of data


# A func which yields entity from pandas row
def convert_row(row):
    entity = model.make_entity(company_schema)
    entity.make_id(row.get('name'), row.get('regCode'))

    # refistration nu,ber is the property of type Company
    entity.add('registrationNumber', row.get('regCode'))
    entity.add('status', row.get('status'))
    entity.add('legalForm', row.get('category'))
    entity.add('mainCountry', row.get('countryOfOrigin'))
    entity.add('alias', row.get('otherNames'))
    entity.add('address', row.get('address'))
    entity.add('incorporationDate', row.get('incorporationDate'))
    entity.add('dissolutionDate', row.get('dissolutionDate'))
    entity.add('okvedCode', row.get('activities'))
    entity.add('modifiedAt', row.get('actualDate'))

    desc_prop = ''
    for k, v in row.items():
        if len(str(v)) > 0:
            desc_prop += '{}: {} \n'.format(k, v)
    entity.add('description', desc_prop)
    yield entity


# for batch processing
def companies_iterator(df):
    for row in df.to_dict(orient='records'):
        yield from convert_row(row)

# Then you save the stream of data into jsonlines file.