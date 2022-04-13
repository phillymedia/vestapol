# vestapol
vestapol is a Python package that loads data from the web and deploys a corresponding external table definition, so that the data can be queried using standard SQL.

["Vestapol"](https://www.youtube.com/watch?v=SKQG-JGyn7U) is an open D Major tuning for the guitar. It is named after a 19th-century composition distributed in some of the earliest instructional guides for guitar.

## Usage
```python
from vestapol.web_resources import CSVResource
from vestapol.destinations import GoogleCloudPlatform


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

### Environment Variables
#### Google Cloud Platform (`vestapol.destinations.GoogleCloudPlatform`)
- `GCS_BUCKET_NAME`: the Google Cloud Storage bucket where data is loaded
- `GCS_ROOT_PREFIX`: the GCS prefix where data is loaded
- `GCLOUD_PROJECT_ID`: the BigQuery project identifier
- `BIGQUERY_DATASET_ID`: the BigQuery dataset where external tables will be created