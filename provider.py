import logging
import argparse
import json
from tractusx_sdk.dataspace.services.connector import ServiceFactory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

providerBPN = "BPNL00000003AYRE"
consumerBPN = "BPNL00000003AZQP"

providerURL = "http://dataprovider-controlplane.tx.test"

# connector settings (provider)
connector_base_url = providerURL
connector_dma_path = "/management"  # Management API path
connector_api_key = "TEST2"
dataspace_version = "jupiter"  # EDC dataspace version

# id settings
asset_id = "100"
access_policy_id = "101"
usage_policy_id = "102"
contract_id = "103"

# asset settings
asset_base_url = "http://a2a.agent.test.tx"
asset_dct_type="cx-taxo:SubmodelBundle",
asset_version="3.0",
asset_semantic_id="urn:samm:io.catenax.part_type_information:1.0.0#PartTypeInformation"

access_context= [
    "https://w3id.org/dspace/2025/1/odrl-profile.jsonld",
    "https://w3id.org/catenax/2025/9/policy/context.jsonld",
    {
      "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
    }
]

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
                        "leftOperand": "BusinessPartnerNumber",
                        "operator": "isAnyOf",
                        "rightOperand": ["BPNL00000003AZQP"]
                    }
                ]
            }
        ]
    }
]

usage_context= [
    "https://w3id.org/dspace/2025/1/odrl-profile.jsonld",
    "https://w3id.org/catenax/2025/9/policy/context.jsonld",
    {
      "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
    },
    {}
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
        verbose=True,
        logger = logger,
        debug=True
    )

    """ Asset """
    if args.type == "asset":

        """ create """
        if args.op == "create":
            if args.id != None:
                global asset_id
                asset_id = args.id
            print(f"{asset_id=}")
            response = service.create_asset(
                asset_id=asset_id,
                properties={
                    "ai-catalog": {
                        "type": "a2a",
                        "description": "ai agent"
                    }
                },
                base_url=asset_base_url,

            )
            print(f"response:\n{json.dumps(response, indent=2)}")

            response = service.assets.get_by_id(asset_id)
            asset = response.json()
            print(f"get:\n{json.dumps(asset, indent=2)}")

        """ list """
        if args.op == "list":
            response = service.assets.get_all()
            asset = response.json()
            print(f"{json.dumps(asset, indent=2)}")

        """ listid """
        if args.op == "listid":
            response = service.assets.get_all()
            assets = response.json()
            for asset in assets:
                print(f"  {asset["@id"]}")

        """ get """
        if args.op == "get":
            if not args.id:
                raise("get require id")
            print(f"{args.id=}")
            response = service.assets.get_by_id(args.id)
            asset = response.json()
            print(f"{json.dumps(asset, indent=2)}")
        
    """ policy """
    if args.type == "policy":

        if args.op == "create":
            if not args.id:
                raise(BaseException("Require id"))
            service.create_policy(
                policy_id=args.id,
                permissions=[
                    {
                        "odrl:action": "use",
                        "odrl:constraint": {
                            "odrl:leftOperand": "BusinessPartnerNumber",
                            "odrl:operator": "eq",
                            "odrl:rightOperand": "BPNL00000003AZQP"
                        }
                    }
                ]
            )
            response = service.policies.get_by_id(args.id)
            print(f"{json.dumps(response.json(), indent=2)}")

        """ create-access """
        if args.op == "create-access":
            id = access_policy_id
            if args.id:
                id = args.id
            service.create_policy(
                policy_id=id,
                context=access_context,
                permissions=access_permission
            )
            response = service.policies.get_by_id(id)
            print(f"{json.dumps(response.json(), indent=2)}")

        """ create-usage """ 
        if args.op == "create-usage":
            id = usage_policy_id
            if args.id:
                id = args.id
            service.create_policy(
                policy_id=id,
                context=usage_context,
                permissions=usage_permission,
                prohibitions=[],
                obligations=[],
            )
            response = service.policies.get_by_id(id)
            print(f"{json.dumps(response.json(), indent=2)}")

        """ list """
        if args.op == "list":
            response = service.policies.get_all()
            policies = response.json()
            print(f"{json.dumps(policies, indent=2)}")

        """ listid """
        if args.op == "listid":
            response = service.policies.get_all()
            policies = response.json()
            for policy in policies:
                print(f"  {policy["@id"]}")

        """ get """
        if  args.op == "get":
            if not args.id:
                raise("Require id")
            response = service.policies.get_by_id(args.id)
            print(f"{json.dumps(response.json(), indent=2)}")

    """ contract """
    if args.type == "contract":

        """ sample """
        if args.op == "sample":
            service.create_contract(
                contract_id="333",
                asset_id="100",
                access_policy_id="333",
                usage_policy_id="333",
            )

        """ create """
        if args.op == "create":
            service.create_contract(
                contract_id=contract_id,
                asset_id=asset_id,
                access_policy_id=access_policy_id,
                usage_policy_id=usage_policy_id,
            )
            response = service.contract_definitions.get_by_id(contract_id)
            contract = response.json()
            print(f"{json.dumps(contract, indent=2)}")    

        """ list """
        if args.op == "list":
            response = service.contract_definitions.get_all()
            contracts = response.json()
            print(f"{json.dumps(contracts, indent=2)}")

        """ listid """
        if args.op == "listid":
            response = service.contract_definitions.get_all()
            contracts = response.json()
            for contract in contracts:
                print(f"  {contract["@id"]}")

        """ get """
        if args.op == "get":
            if not args.id:
                raise("Required id")
            response = service.contract_definitions.get_by_id(args.id)
            contract = response.json()
            print(f"{json.dumps(contract, indent=2)}")

    print("Finished.")

if __name__ == "__main__":
    main()




xaccess_permission=[
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

                # dct_type=asset_dct_type,
                # version=asset_version,
                # semantic_id=asset_semantic_id

                # default context:
                # "edc": "https://w3id.org/edc/v0.0.1/ns/",
                # "cx-common": "https://w3id.org/catenax/ontology/common#",
                # "cx-taxo": "https://w3id.org/catenax/taxonomy#",
                # "dct": "http://purl.org/dc/terms/"