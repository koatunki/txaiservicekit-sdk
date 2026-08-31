import argparse
import json
from tractusx_sdk.dataspace.services.connector import ServiceFactory
from tractusx_sdk.dataspace.models.connector import ModelFactory

providerBPN = "BPNL00000003AYRE"
consumerBPN = "BPNL00000003AZQP"

providerURL = "http://dataprovider-controlplane.tx.test/api/v1/dsp"
consumerURL = "http://dataconsumer-1-controlplane.tx.test"

# connector settings (consumer)
connector_base_url = consumerURL
connector_dma_path = "/management"  # Management API path
connector_api_key = "TEST1"
dataspace_version = "jupiter"  # EDC dataspace version

asset_id="100"
# policies=[...]

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
policies_to_accept = [
    {
        "edctype": "edc:Policy",
        "odrl:permission": {
            "odrl:action": "use",
            "odrl:constraint": {
                "odrl:leftOperand": "BusinessPartnerNumber",
                "odrl:operator": "eq",
                "odrl:rightOperand": "BPNL00000003AYRE"
            }
        }
    }
]


def main():
    print("Starting...")

    # Initialize the parser
    parser = argparse.ArgumentParser(description="A sample Python CLI tool.")

    # Add a positional argument (required by default)
    parser.add_argument("type", type=str, help="catalog, edr")
    parser.add_argument("op", type=str, help="list, listid; create")
    parser.add_argument("-i", "--id", type=str, help="Target id")
    
    # Parse the arguments
    args = parser.parse_args()

    service = ServiceFactory.get_connector_consumer_service(
        dataspace_version=dataspace_version,
        base_url=connector_base_url,
        dma_path=connector_dma_path,
        headers={"X-Api-Key": connector_api_key, "Content-Type": "application/json"},
        verbose=True
    )

    filter=service.get_filter_expression(
        # key="https://w3id.org/edc/v0.0.1/ns/id",
        key="BusinessPartnerNumber",
        operator="=",
        value=consumerBPN
    )
    print(f"{filter=}")

    query_specification={
        "filterExpression": [filter],
        "offset": 0,
        "limit": 50,
    }


    """ catalog """
    if args.type == "catalog":

        """ list """
        if args.op == "list":
            catalogs = service.get_catalog(
                counter_party_id=providerBPN,
                counter_party_address=providerURL
            )
            print(f"{json.dumps(catalogs, indent=2)}")

        """ listid """
        if args.op == "listid":
            catalogs = service.get_catalog(
                counter_party_id=providerBPN,
                counter_party_address=providerURL
            )
            print(f"  {catalogs["@id"]}")
            datasets=catalogs["dcat:dataset"]
            if not datasets:
                print("    Datasets is empty.")
            if isinstance(datasets, list):
                for dataset in datasets:
                    print(f"  {dataset["@id"]}")
                    policies=dataset["odrl:hasPolicy"]
                    if isinstance(policies, list):
                        for policy in dataset["odrl:hasPolicy"]:
                            print(f"    {policy["@id"]}")
                    else:
                        print(f"    {policies["@id"]}")
            else:
                dataset = datasets
                print(f"  {dataset["@id"]}")
                policies=dataset["odrl:hasPolicy"]
                if isinstance(policies, list):
                    for policy in policies:
                        print(f"    {policy["@id"]}")
                else:
                    print(f"    {policies["@id"]}")

        """ get """
        if args.op  == "get":
            if not args.id:
                raise(BaseException("Required id"))
            else:
                print(f"{args.id=}")
            filter=service.get_filter_expression(
                key="https://w3id.org/edc/v0.0.1/ns/id",
                operator="=",
                value=args.id
            )
            print(f"{filter=}")
            query={
                "filterExpression": [filter],
                "offset": 0,
                "limit": 50
            }
            catalog=ModelFactory.get_catalog_model(
                dataspace_version="jupiter",
                counter_party_address=counter_party_address,
                counter_party_id=counter_party_id,
                queryspec=query
            )
            response=service.get_catalog(
                request=catalog
            )
            print(f"{json.dumps(response, indent=2)}")



    """ dspx """
    if args.type == "dspx":

        """ do """
        if args.op == "do":
            if not args.id:
                raise(BaseException("Required id"))
            permission=[{
                "action": "use",
                "constraint": [
                {
                    "and": [
                        {
                            "leftOperand": "Membership",
                            "operator": "eq",
                            "rightOperand": "active"
                        },
                        {
                            "leftOperand": "UsagePurpose",
                            "operator": "isAnyOf",
                            "rightOperand": "cx.core.industrycore:1"
                        }
                    ]
                }]
            }]
            policies_to_accept=[
                {
                    "edctype": "edc:Policy",
                    "permission": permission
                }
            ]
            registry_filter = service.get_filter_expression(
                key="https://w3id.org/edc/v0.0.1/ns/id",
                operator="=",
                value=args.id
            )
        
            dataplane_proxy_url, access_token = service.do_dsp(
                counter_party_id=providerBPN,
                counter_party_address=providerURL,
                filter_expression=registry_filter,
                policies=policies_to_accept
            )
            print(f"{dataplane_proxy_url=}")
            print(f"{access_token=}")


        """ dsp """
        if args.op == "dsp":
            print(f"{args.id=}")
            filter=service.get_filter_expression(
                # key="https://w3id.org/edc/v0.0.1/ns/id",
                key="BusinessPartnerNumber",
                operator="=",
                value=consumerBPN
            )
            print(f"{filter=}")
            dataplane_proxy_url, access_token = service.do_dsp(
                counter_party_id=providerBPN,
                counter_party_address=providerURL,
                policies=policies_to_accept,
                filter_expression=filter
            )
            print(f"{dataplane_proxy_url=}")
            print(f"{access_token}")

        """ create """
        if args.op == "create":
            policy={
                "@id": args.id,
                "policy": usage_permission
            }
            print(f"{policy=}")
            negotiation_id = service.start_edr_negotiation(
                counter_party_id=providerBPN,
                counter_party_address=providerURL,
                target=asset_id,
                policy=policy,
                protocol="dataspace-protocol-http",          # Jupiter
            )
            print(f"{negotiation_id=}")

    """ contract """
    if args.type == "contract":

        """ nego """
        if args.op == "nego":
            contract = service.contract_negotiations.create(
                counter_party_address=providerURL,
                counter_party_id=providerBPN,
                asset_id=asset_id,
                policies=policies
            )

    """ transfer """
    if args.type == "transfer":

        """ start """
        if args.op == "start":
            data = service.transfer(
                contract_id=contract.id,
                asset_id=asset_id
            )

    """ test """
    if args.type == "test":

        """ test """
        if args.op == "test":
            offer_policy={
                "@id": args.id,
                "policy": usage_permission
            }
            contract = ModelFactory.get_contract_negotiation_model(
                dataspace_version=dataspace_version,
                counter_party_address=providerURL,
                offer_id=args.id,
                asset_id=asset_id,
                provider_id=providerBPN,
                offer_policy=offer_policy
            )
            print(f"{contract=}")
            negotiation_id = service.start_edr_negotiation(
                counter_party_id=providerBPN,
                counter_party_address=providerURL,
                target=args.op,
                policy=offer_policy,
            )
            print(f"{negotiation_id=}")


    print("Finished.")


if __name__ == "__main__":
    main()







xpolicies_to_accept = [
    {
        "permission": usage_permission,
        "prohibition": [],
        "obligation": [],
     }
]


    # catalog_request_body={
    #     "@context": {
    #         "edc": "https://w3id.org/edc/v0.0.1/ns/"
    #     },
    #     "@type": "CatalogRequest",
    #     "providerUrl": counter_party_address,
    #     "protocol": "dataspace-protocol-http",
    #     "querySpec": {
    #         "filterExpression": [filter]
    #     }
    # }

    # catalog_response = service.get_catalog_by_dct_type(
    #     # dct_type="https://w3id.org/catenax/taxonomy#DigitalTwinRegistry",
    #     counter_party_id=counter_party_id,
    #     counter_party_address=counter_party_address,
    #     timeout=15
    # )

    # # Process the returned catalog items
    # offers = catalog_response.get("dcat:dataset", [])
    # if isinstance(offers, dict):
    #     offers = [offers]

    # print(f"\nFound {len(offers)} matching asset(s):")
    # for offer in offers:
    #     print(f"- Asset ID: {offer.get('@id')}")

