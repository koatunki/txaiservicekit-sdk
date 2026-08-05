import argparse
import json
from tractusx_sdk.dataspace.services.connector.base_connector_provider import (
    BaseConnectorProviderService,
)

def main():
    print("Consumer")

    # Initialize the parser
    parser = argparse.ArgumentParser(description="A sample Python CLI tool.")

    # Add a positional argument (required by default)
    parser.add_argument("op", type=str, help="Operation: create, list")
    parser.add_argument("-i", "--id", type=str, help="Target id")
    
    # Parse the arguments
    args = parser.parse_args()

    # Initialize connector provider service
    connector = BaseConnectorProviderService(
        dataspace_version="jupiter",  # or "saturn" for newer connectors
        base_url="http://dataconsumer-1-controlplane.tx.test",
        dma_path="/management",
        headers={
            "X-Api-Key": "TEST1",
            "Content-Type": "application/json"
        }
    )

    if args.op == "list":
        # List all assets
        response = connector.catalog.get_all()
        catalogs = response.json()
        for asset in catalogs:
            print(f"Asset ID: {asset['@id']}")

if __name__ == "__main__":
    main()
