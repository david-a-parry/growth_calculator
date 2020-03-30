#!/usr/bin/env python3
from math import isclose
from nose.tools import assert_equal
import pandas as pd
from pandas.testing import assert_frame_equal
from human_growth_calculator.growth_calculator import adjust_age, zscore_cohort
from human_growth_calculator.growth_calculator import calculate_zscore


def test_adjust_age():
    for g in range(40, 30, -1):
        d = 40 - g
        adj = d/52.1429
        assert_equal(adjust_age(1, g), 1 - adj)


def test_no_adjust_age():
    assert_equal(adjust_age(1, 40), 1)
    assert_equal(adjust_age(1, 41), 1)


def test_calculate_zscore_british_1990():
    dset = 'british_1990'
    assert isclose(calculate_zscore('weight', 18.25, 'Male', 18, dataset=dset),
                   -14.239794954580626)
    assert isclose(calculate_zscore('height', 109.9, 'Male', 18, dataset=dset),
                   -9.585942360337782)
    assert isclose(calculate_zscore('ofc', 48.5, 'Male', 18, dataset=dset),
                   -5.11489060264972)
    assert isclose(calculate_zscore('weight', 1.88, 'Female', 8,
                                    age_unit='weeks', dataset=dset),
                   -6.819787110350214)
    assert isclose(calculate_zscore('ofc', 30, 'Female', 8, age_unit='weeks',
                                    dataset=dset),
                   -7.41293629546379)
    assert isclose(calculate_zscore('height', 40, 'Female', 8,
                                    age_unit='weeks',  dataset=dset),
                   -8.494449070930305)


def test_calculate_zscore_UK_WHO_preterm():
    dset = 'UK_WHO_preterm'
    assert isclose(calculate_zscore('weight', 0.74, 'Female', -10,
                                    age_unit='weeks', dataset=dset),
                   -2.3798957699137215)
    assert isclose(calculate_zscore('ofc', 25, 'Female', -10, age_unit='weeks',
                                    dataset=dset),
                   -2.0575018824447757)
    assert isclose(calculate_zscore('height', 34, 'Female', -10,
                                    age_unit='weeks', dataset=dset),
                   -2.337822449368135)


def test_zscore_cohort():
    prenatal = [dict(id=1, gender='female', gestation=30,
                     age=0, weight=0.74, ofc=25, height=34),
                dict(id=2, gender='male', gestation=35,
                     age=0, weight=0.99, ofc=28, height=38),
                dict(id=3, gender='male', gestation=38,
                     age=0, weight=1.64, ofc=29, height=40.5),
                dict(id=4, gender='female', gestation=38,
                     age=0, weight=1.48, ofc=32, height=40),
                dict(id=5, gender='male', gestation=38,
                     age=0, weight=1.956)]
    postnatal = [dict(id=1, gender='female', gestation=30, age=4.5,
                      age_unit='months', weight=1.88, ofc=30, height=40),
                 dict(id=2, gender='male', gestation=35, age=9,
                      age_unit='months', weight=3.00, ofc=38, height=55),
                 dict(id=3, gender='female', gestation=38, age=16,
                      age_unit='months', weight=2.74, ofc=41, height=54),
                 dict(id=4, gender='male', gestation=38, age=5,
                      age_unit='years', weight=6.095, ofc=41, height=71),
                 dict(id=5, gender='male', gestation=38, age=2.03,
                      weight=3.78, ofc=43.5, height=55.7)]
    assert_frame_equal(zscore_cohort(prenatal),
                       pd.read_csv("test_data/pre.csv"))
    assert_frame_equal(zscore_cohort(postnatal),
                       pd.read_csv("test_data/post.csv"))


if __name__ == '__main__':
    import nose
    nose.run(defaultTest=__name__)
