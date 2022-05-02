# vestapol

vestapol is a Python package that loads data from the web and deploys a corresponding external table definition, so that the data can be queried using standard SQL.

["Vestapol"](https://www.youtube.com/watch?v=SKQG-JGyn7U) is an open D Major tuning for the guitar. It is named after a 19th-century composition distributed in some of the earliest instructional guides for guitar.

## Setup

1. Install poetry:

```shell
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

2. Add poetry to path:

```shell
    source $HOME/.poetry/env
```

3. Check that you have a Python version compatible with requirements for this project. See `python` under `[tool.poetry.dependencies]` in `pyproject.toml` for current dependencies. If you are not currently using Pyenv to manange Python installation, refer to our [Documentation](https://inquirer.atlassian.net/wiki/spaces/KB/pages/1763704858/How+to+manage+Python+installations+on+your+machine+with+Pyenv). Follow instructions there to install an appropriate version.

```shell
    pyenv versions
```

4. Check futher that you have Python versions installed for all that are tested by tox. See `envlist` under `[tox]` in `tox.ini` for current dependencies.

```shell
    pyenv install <version>
```

5. Create poetry virtualenv:

```shell
    poetry shell
```

6. Make sure poetry.lock is up to date:

```shell
    poetry update
```

7. Install vestapol in poetry virtualenv:

```shell
    poetry install
```

8. Set environment variables for development:

### Google Cloud Platform (`vestapol.destinations.GoogleCloudPlatform`)

- `GCS_BUCKET_NAME`: the Google Cloud Storage bucket where data is loaded (e.g. `inq-warehouse-waligob`)
- `GCS_ROOT_PREFIX`: the GCS prefix where data is loaded (e.g. `data_catalog`)
- `GBQ_PROJECT_ID`: the BigQuery project identifier (e.g. `inq-warehouse`)
- `GBQ_DATASET_ID`: the BigQuery dataset where external tables will be created (e.g. `data_catalog_waligob`)
- `GBQ_DATASET_LOCATION`: the BigQuery dataset location (e.g. `US`)
- `GOOGLE_APPLICATION_CREDENTIALS=`: location of the GCS service account keyfile (e.g. `~/inq-warehouse-f0962a57089e-inf.json`)

8. run tests in clean poetry environment:

```shell
    tox
```

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
