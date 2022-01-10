from setuptools import setup, find_packages

setup(
    name='vestapol',
    version='0.0.1',
    description=(
        'Python package that loads data from the web and deploys a'
        ' corresponding external table definition, so that the data can be' 
        ' queried using standard SQL.'
    ),
    # TODO: edit so that install doesn't require gcp client libs
    install_requires=[
        'requests>=2.26.0',
        'google-cloud-storage>=1.43.0',
        'google-cloud-bigquery>=2.31.0'
    ],
    url='http://github.com/phillymedia/vestapol',
    packages=find_packages(),
    zip_safe=False
)
