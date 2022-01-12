import os
import pathlib
import logging
from google.cloud import storage
from vestapol import external_tables
from vestapol.destinations import base_destination

logger = logging.getLogger(__name__)


class GoogleCloudPlatform(base_destination.BaseDestination):
    def __init__(
        self,
        gcs_bucket_name=None,
        gcs_root_prefix=None,
        gbq_project_id=None,
        gbq_dataset_id=None,
        gbq_dataset_location=None,
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
        blob.upload_from_string(data)

    def create_table(self, resource):
        common_prefix = pathlib.Path(
            resource.name, resource.external_data_format_tag, resource.version
        )

        sources = [f"{common_prefix}/*/{resource.response_filename}"]

        source_uris = [f"{self.gcs_root_prefix_fq}{source}" for source in sources]

        source_uri_prefix_fq = f"{self.gcs_root_prefix_fq}{common_prefix}/"

        tablename = resource.name

        external_tables.create_gcp_table(
            resource.external_data_format_tag,
            self.gbq_project_id,
            self.gbq_dataset_id,
            self.gbq_dataset_location,
            tablename,
            source_uri_prefix_fq,
            source_uris,
        )

        tablename_fq = f"{self.gbq_project_id}.{self.gbq_dataset_id}.{tablename}"

        return tablename_fq
