import os
from datetime import datetime, timedelta
import random

# Define parameters
environments = ['mainnet', 'testnet', 'preprod']
sidecar_versions = ['v1.0.0', 'v1.0.1', 'v1.0.2']

# Create 10 dump files
for i in range(10):
    # Randomly select environment
    environment = random.choice(environments)
    
    # Select network based on environment
    if environment == 'mainnet':
        network = 'ethereum'
    else:
        network = 'holesky'
    
    # Randomly select sidecar version
    sidecar_version = random.choice(sidecar_versions)
    
    # Generate a random offset in seconds within the last 6 days
    offset_seconds = random.randint(0, 6 * 24 * 60 * 60)  # 6 days in seconds
    datetime_offset = datetime.utcnow() - timedelta(seconds=offset_seconds)
    datetime_now = datetime_offset.strftime('%Y%m%dT%H%M%S')
    
    # Construct directory path
    directory = f'snapshots/{environment}/{network}'
    os.makedirs(directory, exist_ok=True)
    
    # Construct file path
    file_name = f'snapshot-{sidecar_version}-{datetime_now}.dump'
    file_path = os.path.join(directory, file_name)
    
    # Write dummy data to file to make it approximately 3KB
    with open(file_path, 'w') as f:
        f.write('0' * 3072)  # 3KB of zeros

    print(f'Created: {file_path}') 