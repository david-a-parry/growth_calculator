from setuptools import setup
setup(
    name="growth_calculator",
    packages=[""],
    version="0.1",
    description="Calculate Z-scores for body measurements",
    author="David A. Parry",
    author_email="david.parry@igmm.ed.ac.uk",
    url="https://git.ecdf.ed.ac.uk/dparry/growth_params",
    download_url="https://git.ecdf.ed.ac.uk/dparry/growth_params/archive/0.1.tar.gz",
    test_suite='nose.collector',
    tests_require=['nose'],
    python_requires='>=3.5',
    license='MIT',
    install_requires=[
        'pandas',
        'numpy',
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        ],
)
