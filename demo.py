from google.cloud import bigquery
from vestapol.web_resources import CSVResource
from vestapol.destinations import GoogleCloudPlatform


class NYTCovid19Data_2022(CSVResource):
    name = 'nyt_covid19_us_counties_2022'
    base_url = 'https://raw.githubusercontent.com/'
    endpoint = 'nytimes/covid-19-data/master/rolling-averages/us-counties-2022.csv'
    version = 'v0'
    has_header = True


destination = GoogleCloudPlatform()

resource = NYTCovid19Data_2022()
resource.load(destination)
tablename = destination.create_table(resource)


client = bigquery.Client()
query = f"""
    select 
        date,
        state,
        county,
        cases_avg_per_100k
    from `{tablename}`
    where requested_at = '{resource.requested_at}'
          and county = 'Philadelphia'
    order by 1 desc
    limit 5
"""
query_job = client.query(query)
for row in query_job.result():
    print(row)
