import argparse
import json
from tractusx_sdk.dataspace.services.connector import ServiceFactory

# connector settings (provider side)
connector_base_url = "http://dataprovider-controlplane.tx.test"
connector_dma_path = "/management"  # Management API path
connector_api_key = "TEST2"
dataspace_version = "jupiter"  # EDC dataspace version

# items id
asset_id = "100"
access_policy_id = "101"
usage_policy_id = "102"
contract_id = "103"

# asset
asset_base_url = "http:test"
asset_dct_type="cx-taxo:SubmodelBundle",
asset_version="3.0",
asset_semantic_id="urn:samm:io.catenax.part_type_information:1.0.0#PartTypeInformation"

access_permission=[
    {
        "action": "access",
        "constraint": [
            {
                "and": [
                    {
                        "leftOperand": "Membership",
                        "operator": "eq",
                        "rightOperand": "active"
                    },
                    {
                        "leftOperand": "FrameworkAgreement",
                        "operator": "eq",
                        "rightOperand": "DataExchangeGovernance:1.0"
                    },
                    {
                        "leftOperand": "BusinessPartnerNumber",
                        "operator": "isAnyOf",
                        "rightOperand": ["BPNL00000003AZQP"]
                    }
                ]
            }
        ]
    }
]
usage_permission=[
    {
        "action": "use",
        "constraint": {
            "and": [
                {
                    "leftOperand": "Membership",
                    "operator": "eq",
                    "rightOperand": "active"
                },
                {
                    "leftOperand": "FrameworkAgreement",
                    "operator": "eq",
                    "rightOperand": "DataExchangeGovernance:1.0"
                },
                {
                    "leftOperand": "UsagePurpose",
                    "operator": "isAnyOf",
                    "rightOperand": [
                        "cx.core.industrycore:1"
                    ]
                }
            ]
        }
    }
]

sample_policies = [
    {
        "edctype": "edc:Policy",
        "odrl:permission": {
            "odrl:action": "use",
            "odrl:constraint": {
                "odrl:leftOperand": "BusinessPartnerNumber",
                "odrl:operator": "eq",
                "odrl:rightOperand": "BPNL00000003AZQP"
            }
        }
    }
]

def main():
    print("Starting...")
    # Initialize the parser

    parser = argparse.ArgumentParser(description="A sample Python CLI tool.")

    # Add a positional argument (required by default)
    parser.add_argument("type", type=str, help="asset, policy, contract")
    parser.add_argument("op", type=str, help="create, list, get <id>, listid; create-access, create-usage, list, listid; create, list, listid, get <id>")
    parser.add_argument("-i", "--id", type=str, help="Target id")
    
    # Parse the arguments
    args = parser.parse_args()

    # Provider: Create and publish an asset
    service = ServiceFactory.get_connector_provider_service(
        dataspace_version=dataspace_version,
        base_url=connector_base_url,
        dma_path=connector_dma_path,
        headers={"X-Api-Key": connector_api_key, "Content-Type": "application/json"},
        verbose=True
    )

    if args.type == "asset":
        if args.op == "create":
            if args.id != None:
                global asset_id
                asset_id = args.id
            print(f"{asset_id=}")
            response = service.create_asset(
                asset_id=asset_id,
                properties={
                    "name": "ai-catalog1",
                    "cx-common:name": "ai-catalog2",
                    "https://w3id.org/catenax/ontology/common#name": "ai-catalog3",
                    "https://w3id.org/catenax/ontology/common#cx-common:name": "ai-catalog4",
                },
                private_properties={
                    "aicatalog": "test"
                },
                base_url=asset_base_url,
                # dct_type=asset_dct_type,
                # version=asset_version,
                # semantic_id=asset_semantic_id

                # if context is None:
                context={
                    "edc": "https://w3id.org/edc/v0.0.1/ns/",
                    # "cx-common": "https://w3id.org/catenax/ontology/common#",
                    # "cx-taxo": "https://w3id.org/catenax/taxonomy#",
                    "dct": "http://purl.org/dc/terms/",
                    "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
                    "tx": "https://w3id.org/tractusx/v0.0.1/ns/",
                    "tx-auth": "https://w3id.org/tractusx/auth/",
                    "cx-policy": "https://w3id.org/catenax/policy/",
                    "odrl": "http://www.w3.org/ns/odrl/2/"
                },
                dct_type="example-type",
                version="3.0"
            )
            
        if args.op == "list":
            response = service.assets.get_all()
            asset = response.json()
            print(f"{json.dumps(asset, indent=2)}")

        if args.op == "listid":
            response = service.assets.get_all()
            assets = response.json()
            for asset in assets:
                print(f"  {asset["@id"]}")

        if args.op == "get":
            print(f"{args.id=}")
            response = service.assets.get_by_id(args.id)
            asset = response.json()
            print(f"{json.dumps(asset, indent=2)}")

        
    if args.type == "policy":
        if args.op == "sample":
            service.create_policy(
                policy_id="333",
                permission=sample_policies
            )

        if args.op == "create-access":
            service.create_policy(
                policy_id=access_policy_id,
                permission=[
                    {
                        "action": "access",
                        "constraint": access_permission,
                    }
                ],
            )

        if args.op == "create-usage":
            service.create_policy(
                policy_id=usage_policy_id,
                permission=usage_permission,
                prohibition=[],
                obligation=[],
            )
        if args.op == "list":
            response = service.policies.get_all()
            policies = response.json()
            print(f"{json.dumps(policies, indent=2)}")

        if args.op == "listid":
            response = service.policies.get_all()
            policies = response.json()
            for policy in policies:
                print(f"  {policy["@id"]}")

    if args.type == "contract":
        if args.op == "sample":
            service.create_contract(
                contract_id="333",
                asset_id="100",
                access_policy_id="333",
                usage_policy_id="333",
            )

        if args.op == "create":
            service.create_contract(
                contract_id=contract_id,
                asset_id=asset_id,
                access_policy_id=access_policy_id,
                usage_policy_id=usage_policy_id,
            )

        if args.op == "list":
            response = service.contract_definitions.get_all()
            contracts = response.json()
            print(f"{json.dumps(contracts, indent=2)}")

        if args.op == "listid":
            response = service.contract_definitions.get_all()
            contracts = response.json()
            for contract in contracts:
                print(f"  {contract["@id"]}")

        if args.op == "get":
            response = service.contract_definitions.get_by_id(args.id)
            contract = response.json()
            print(f"{json.dumps(contract, indent=2)}")

    print("Finished.")

if __name__ == "__main__":
    main()