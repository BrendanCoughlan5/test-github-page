import json
import boto3
import os
from datetime import datetime, timezone

def list_files_in_r2():
    try:
        # Use environment variables for credentials and endpoint
        r2_endpoint = os.getenv('R2_ENDPOINT')
        r2_access_key = os.getenv('R2_ACCESS_KEY')
        r2_secret_key = os.getenv('R2_SECRET_KEY')
        r2_bucket_name = os.getenv('R2_BUCKET_NAME')
        base_url = os.getenv('BASE_URL')

        if not all([r2_endpoint, r2_access_key, r2_secret_key, r2_bucket_name, base_url]):
            raise ValueError("One or more environment variables are missing.")

        # Create a session and client for R2
        session = boto3.session.Session()
        s3_client = session.client(
            's3',
            endpoint_url=r2_endpoint,
            aws_access_key_id=r2_access_key,
            aws_secret_access_key=r2_secret_key
        )
        
        # List objects in the bucket
        response = s3_client.list_objects_v2(Bucket=r2_bucket_name)
        
        if 'Contents' in response:
            files = []
            for obj in response['Contents']:
                key = obj['Key']
                size = obj['Size']
                parts = key.split('/')
                if len(parts) == 4:
                    environment, network, file_name = parts[1], parts[2], parts[3]
                    file_parts = file_name.split('-')
                    if len(file_parts) == 3:
                        sidecar_version = file_parts[1]
                        date = file_parts[2].replace('.dump', '')
                        files.append({
                            "name": key,
                            "path": f"/{key}",
                            "environment": environment,
                            "network": network,
                            "sidecar_version": sidecar_version,
                            "date": date,
                            "size": size,
                            "download_link": f"{base_url}/{key}"
                        })
            return files
        else:
            return []
    except Exception as e:
        raise RuntimeError(f"Failed to list files in R2: {e}")

def generate_recent_data():
    try:
        files = list_files_in_r2()
        data = {
            "meta": {
                "lastRefreshed": datetime.now(timezone.utc).isoformat(),
                "baseUrl": os.getenv('BASE_URL')
            },
            "snapshots": files
        }
        
        # Write the data to snapshot_data.json
        with open('snapshots_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise RuntimeError(f"An error occurred while generating recent data: {e}")

if __name__ == "__main__":
    try:
        generate_recent_data()
    except Exception as e:
        print(f"An error occurred: {e}")