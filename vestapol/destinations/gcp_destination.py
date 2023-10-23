from __future__ import annotations

import logging
import os
import pathlib
from typing import TYPE_CHECKING

import google.cloud.bigquery as bigquery
import google.cloud.storage as storage

from vestapol import external_tables
from vestapol.destinations import base_destination


if TYPE_CHECKING:
    from vestapol.web_resources.base_resource import BaseResource

logger = logging.getLogger(__name__)


class GoogleCloudPlatform(base_destination.BaseDestination):
    def __init__(
        self,
        gcs_bucket_name: str = None,
        gcs_root_prefix: str = None,
        gbq_project_id: str = None,
        gbq_dataset_id: str = None,
        gbq_dataset_location: str = None,
    ):
        self.gcs_bucket_name = gcs_bucket_name or os.environ["GCS_BUCKET_NAME"]
        self.gcs_root_prefix = gcs_root_prefix or os.environ["GCS_ROOT_PREFIX"]
        self.gcs_root_prefix_fq = f"gs://{self.gcs_bucket_name}/{self.gcs_root_prefix}/"
        self.gbq_project_id = gbq_project_id or os.environ["GBQ_PROJECT_ID"]
        self.gbq_dataset_id = gbq_dataset_id or os.environ["GBQ_DATASET_ID"]
        self.gbq_dataset_location = (
            gbq_dataset_location or os.environ["GBQ_DATASET_LOCATION"]
        )

    def write_data(self, data: str, pathname: str):
        destination_blob_name = f"{self.gcs_root_prefix}/{str(pathname)}"
        logger.debug(
            f"Uploading data to gs://{self.gcs_bucket_name}/{destination_blob_name}"
        )
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.gcs_bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(data, timeout=120)

    def create_table(self, resource: BaseResource):
        common_prefix = pathlib.Path(
            resource.name, resource.external_data_format_tag, resource.version
        )

        sources = [f"{common_prefix}/*/{resource.response_filename}"]

        source_uris = [f"{self.gcs_root_prefix_fq}{source}" for source in sources]

        source_uri_prefix_fq = f"{self.gcs_root_prefix_fq}{common_prefix}/"

        tablename = resource.name

        if resource.manual_schema is not None:
            table_schema = [self.dict_to_schema(s) for s in resource.manual_schema]
        else:
            table_schema = None

        external_tables.create_gcp_table(
            resource.external_data_format_tag,
            self.gbq_project_id,
            self.gbq_dataset_id,
            self.gbq_dataset_location,
            tablename,
            source_uri_prefix_fq,
            source_uris,
            table_schema,
            resource.skip_leading_rows,
            resource.allow_quoted_newlines,
            resource.field_delimiter,
        )

        tablename_fq = f"{self.gbq_project_id}.{self.gbq_dataset_id}.{tablename}"

        return tablename_fq

    def dict_to_schema(self, dict_schema):
        if "fields" in dict_schema.keys():
            dict_schema["fields"] = [
                self.dict_to_schema(f) for f in dict_schema["fields"]
            ]
        return bigquery.SchemaField(**dict_schema)
