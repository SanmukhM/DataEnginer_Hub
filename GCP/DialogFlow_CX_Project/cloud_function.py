from google.cloud import bigquery
from google.cloud import storage
import os

# Set environment variable for authentication (important!)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-service-account.json"

def load_gcs_to_bq(event, context):
    """Triggered by a change in a specified GCS bucket.

    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    # Get file information from the event
    file = event
    bucket_name = file['bucket']
    file_name = file['name']

    # BigQuery configuration
    project_id = 'your-project-id'
    dataset_id = 'your_dataset_id'
    table_id = 'your_table_id'
    table_ref = f'{project_id}.{dataset_id}.{table_id}'

    # Construct GCS URI
    gcs_uri = f'gs://{bucket_name}/{file_name}'

    # BigQuery load job configuration
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, # Adjust if needed
        autodetect=True,  # Set to False if you need to provide a schema
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND # Or WRITE_TRUNCATE
    )

    # Create BigQuery client
    client = bigquery.Client()

    # Load data from GCS to BigQuery
    load_job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    load_job.result()  # Wait for the job to complete

    print(f"Data from gs://{bucket_name}/{file_name} loaded to {table_ref}.")
