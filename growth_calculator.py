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
    ''' Adjust age in years by if weeks_gestation < 40.'''
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
    '''
        Calculate a Z-score for a single measurement. Returns Z-score
        and optionally the nearest age in the reference dataset used for
        the calculation.

    Args:
        measure:
                type of measurement. Required. Must be one of the
                following:
                    'height' (in cm)
                    'ofc' (in cm)
                    'weight' (in kg)

        x:      value for this measurement. Required.

        gender: 'male' or 'female' Required.

        age:    age at time of measurement. Required. Either in years or
                using a unit specified by the 'age_unit' argument (see
                below).

        weeks_gestation:
                Give the weeks gestation if the measurements should be
                adjusted for gestation. Default=40.

        dataset:
                Which growth dataset to use. Either 'british_1990' or
                'UK_WHO_preterm'. Default='british_1990'.

        age_unit:
                Unit for the provided age. Default='years'. Options are:
                    'days'
                    'weeks'
                    'months'
                    'years'

        return_nearest_age:
                If True the function will return 3 arguments, the
                Z-score, the age used in the calculation (in years) and
                the provided age (converted to years). Default=False.

        verbose:
                If True, print information about the calaulation to
                STDOUT. Default=False.

    '''
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
    '''
        Calculate Z-scores for multiple measurements and individuals.
        Returns a pandas dataframe.

        Args:
            individuals:
                 an iterable of dicts, one per individual. The keys 'id',
                 'gender' and 'age' must be present for each individual.

                Optional keys are:
                     'height' (in cm)
                     'ofc' (in cm)
                     'weight' (in kg)
                     'gestation' (in weeks)
                     'age_unit' (days, weeks, months or years [default])

                Example: [dict(id=1, gender='male', gestation=35,
                               age=9, age_unit='months', weight=3.00,
                               ofc=38, height=55),
                          dict(id=2, gender='female', age=10,
                               age_unit='months', weight=5.00,
                               ofc=42, height=64)]

            dataset:
                    Which growth dataset to use. Either 'british_1990' or
                    'UK_WHO_preterm'. Default='british_1990'.

            default_age_unit:
                    Unit for the provided age for each individual where
                    'age_unit' is not provided. Default='years'.
                    Options are:
                        'days'
                        'weeks'
                        'months'
                        'years'

    '''
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
