# Growth Parameter Calculations

Simple python utilities for calculating Z-scores for human growth data (height,
weight, OFC).

## Installation/Usage

Requires python >=3.5

    pip3 install git+https://github.com/david-a-parry/growth_calculator.git --user

You may also choose to clone this repository and see the examples.ipynb
notebook for example use cases.

    git clone https://github.com/david-a-parry/growth_calculator.git
    cd growth_params
    jupyter-notebook

A few example use cases are given below:

~~~
from human_growth_calculator.growth_calculator import calculate_zscore

zscore = calculate_zscore(measure='weight', x=18.25, gender='Male', age=18)
zscore = calculate_zscore(measure='ofc', x=30, gender='Female', age=8,
                          age_unit='weeks')
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
df1 = zscore_cohort(prenatal)

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
df2 = zscore_cohort(postnatal)

~~~

Use `help(calculate_zscore)` or `help(calculate_zscore_cohort)` for detailed
help information.

