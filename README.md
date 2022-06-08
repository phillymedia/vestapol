# vestapol

vestapol is a Python package that loads data from the web and deploys a corresponding external table definition, so that the data can be queried using standard SQL.

["Vestapol"](https://www.youtube.com/watch?v=SKQG-JGyn7U) is an open D Major tuning for the guitar. It is named after a 19th-century composition distributed in some of the earliest instructional guides for guitar.

## Usage

```python
from vestapol.web_resources.csv_resource import CSVResource
from vestapol.destinations.gcp_destination import GoogleCloudPlatform


nyt_covid_data_2022 = CSVResource(
    name="nyt_covid19_us_counties_2022",
    base_url="https://raw.githubusercontent.com/",
    endpoint="nytimes/covid-19-data/master/rolling-averages/us-counties-2022.csv",
    version="v0",
    has_header=True,
)

destination = GoogleCloudPlatform()

nyt_covid_data_2022.load(destination)
tablename = destination.create_table(nyt_covid_data_2022)


from google.cloud import bigquery

client = bigquery.Client()
query = f"""
    select date, state, county, cases_avg_per_100k
    from `{tablename}`
    where requested_at = '{nyt_covid_data_2022.requested_at}'
    limit 5
"""
query_job = client.query(query)
for row in query_job.result():
    print(row)
```


## Prerequisites

Installation of this project requires [Poetry](https://python-poetry.org/docs/) and Python version 3.8+.


## Installation

Install vestapol and its dependencies by running:

```shell
poetry install
```

## Testing

Run tests with the following command:

```shell
poetry run pytest
```

## Environment Variables

- `GCS_BUCKET_NAME`: the Google Cloud Storage bucket where data is loaded (e.g. `inq-warehouse-waligob`)
- `GCS_ROOT_PREFIX`: the GCS prefix where data is loaded (e.g. `data_catalog`)
- `GBQ_PROJECT_ID`: the BigQuery project identifier (e.g. `inq-warehouse`)
- `GBQ_DATASET_ID`: the BigQuery dataset where external tables will be created (e.g. `data_catalog_waligob`)
- `GBQ_DATASET_LOCATION`: the BigQuery dataset location (e.g. `US`)
- `GOOGLE_APPLICATION_CREDENTIALS=`: location of the GCS service account keyfile (e.g. `~/inq-warehouse-f0962a57089e-inf.json`)


## Publishing to PyPI

Instructions for pushing new versions of `vestapol` to PyPI:

1. Update `CHANGELOG.md`. Include Additions, Fixes, and Changes.

2. Update project version using either a valid [PEP 440 string](https://peps.python.org/pep-0440/) or a [valid bump rule](https://python-poetry.org/docs/master/cli/#version) following [Semantic Versioning](http://semver.org/).

```shell
    poetry version <version string or bump rule>
```

3. Create a [release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) and check the CD Pipeline [action](https://github.com/phillymedia/vestapol/actions/workflows/release.yml) to ensure that the project was built and published to PyPI successfully.
