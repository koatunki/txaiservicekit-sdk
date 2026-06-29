import argparse
import json
from tractusx_sdk.dataspace.services.connector.base_connector_provider import (
    BaseConnectorProviderService,
)


def main():
    print("Hello from txaiservicekit-sdk!")

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
        base_url="http://dataprovider-controlplane.tx.test",
        dma_path="/management",
        headers={
            "X-Api-Key": "TEST2",
            "Content-Type": "application/json"
        }
    )

    if args.op == "create":  
        # Create a simple data asset
        asset = connector.create_asset(
            asset_id=args.id,
            base_url="https://backend.example.com/api/data",
            dct_type="application/json",
            version="3.0"
        )
        print(f"Asset created: {asset['@id']}")

    if args.op == "list":
        # List all assets
        response = connector.assets.get_all()
        assets = response.json()
        for asset in assets:
            print(f"Asset ID: {asset['@id']}")

    if args.op == "get":
        # List all assets
        response = connector.assets.get_by_id(args.id)
        asset = response.json()
        print(f"{json.dumps(asset, indent=2)}")

                  
if __name__ == "__main__":
    main()
