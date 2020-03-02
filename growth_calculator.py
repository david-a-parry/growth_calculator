import pandas as pd
import glob
import os
import numpy as np
from collections import defaultdict

measurements = defaultdict(dict)
for dataset in ['british_1990', 'UK_WHO_preterm']:
    for csv in glob.glob("data/*{}.csv".format(dataset)):
        msr = os.path.basename(csv).replace('_' + dataset + '.csv', '')
        measurements[dataset][msr] = pd.read_csv(csv, sep='\t')
        measurements[dataset][msr]['Gender'] = (
            measurements[dataset][msr]['Gender'].apply(
                lambda x: 'male' if x == 1 else 'female'))

unit_converter = {'days': lambda x: x/365.25,
                  'weeks': lambda x: x/52.1429,
                  'months': lambda x: x/12,
                  'years': lambda x: x}


def adjust_age(years, weeks_gestation, verbose=False):
    if weeks_gestation < 40:
        adjust = unit_converter['weeks'](40 - weeks_gestation)
        if verbose:
            print("Adjusting age by {} for {} weeks gestation".format(
                    adjust, weeks_gestation))
        years -= adjust
    return years


def calculate_zscore(measure, x, gender, age, weeks_gestation=40,
                     dataset='british_1990',
                     age_unit='years', return_nearest_age=False,
                     verbose=False):
    age = unit_converter[age_unit](age)
    age = adjust_age(age, weeks_gestation, verbose=verbose)
    gender = gender.lower()
    df = measurements[dataset][measure]
    row = df.iloc[np.abs(df[df.Gender == gender].Age - age).idxmin()]
    z = ((x / row.M)**row.L - 1) / (row.S * row.L)
    if verbose:
        print("Using nearest age of {} for user provided age of {}".format(
            row.Age, age))
        print("Using {} dataset".format(dataset))
        print("Z-score for {} years old {} {} of {} = {}".format(
              age, gender, measure, x, z))
    if return_nearest_age:
        return z, row.Age, age
    return z


def zscore_cohort(individuals, dataset='british_1990',
                  default_age_unit='years'):
    col_order = ['ID', 'weight', 'weight SD', 'ofc', 'ofc SD', 'height',
                 'height SD', 'Gender', 'Provided_Age',
                 'Provided_Age_Unit', 'Gestation', 'Age', 'Adjusted_age',
                 'Nearest_age_weight', 'Nearest_age_ofc', 'Nearest_age_height']
    results = defaultdict(list)
    for i in range(len(individuals)):
        for req in ['id', 'gender', 'age']:
            if req not in individuals[i]:
                raise ValueError("Required field '{}' ".format(req) +
                                 "not available for individual {}".format(i))
        age_unit = individuals[i].get('age_unit', default_age_unit)
        years = unit_converter[age_unit](individuals[i]['age'])
        results['ID'].append(individuals[i]['id'])
        results['Provided_Age'].append(individuals[i]['age'])
        results['Provided_Age_Unit'].append(age_unit)
        results['Age'].append(years)
        results['Adjusted_age'].append(adjust_age(years,
                                                  individuals[i].get(
                                                      'gestation', 40)))
        results['Gender'].append(individuals[i]['gender'])
        results['Gestation'].append(individuals[i].get('gestation', 40))
        for m in ['weight', 'ofc', 'height']:
            z, n, adj = None, None, unit_converter[age_unit](
                individuals[i]['age'])
            if m in individuals[i]:
                z, n, adj = calculate_zscore(
                    measure=m,
                    x=individuals[i][m],
                    gender=individuals[i]['gender'],
                    weeks_gestation=individuals[i].get('gestation', 40),
                    age=individuals[i]['age'],
                    age_unit=age_unit,
                    dataset=dataset,
                    return_nearest_age=True)
            results[m].append(individuals[i].get(m, None))
            results[m + " SD"].append(z)
            results['Nearest_age_{}'.format(m)].append(n)
    df = pd.DataFrame.from_dict(results)
    df = df[col_order]
    return df
