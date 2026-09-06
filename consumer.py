import logging
import argparse
import json
from tractusx_sdk.dataspace.services.connector import ServiceFactory
from tractusx_sdk.dataspace.models.connector import ModelFactory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

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
#asset_id="MTAz:MTAw:ZGU1ZTE1MTMtNzllMy00ZmQzLTg4NGYtNWVhNWJjZjM3OWNk"

policies_to_accept=[{
    "odrl:permission": [{
        "odrl:action": "odrl:use",
        "odrl:constraint": [{
            "odrl:and": [{
                "odrl:leftOperand": "https://w3id.org/catenax/2025/9/policy/FrameworkAgreement",
                "odrl:operator": "odrl:eq",
                "odrl:rightOperand": "DataExchangeGovernance:1.0"
            },
            {
                "odrl:leftOperand": "https://w3id.org/catenax/2025/9/policy/Membership",
                "odrl:operator": "odrl:eq",
                "odrl:rightOperand": "active"
            },
            {
                "odrl:leftOperand": "https://w3id.org/catenax/2025/9/policy/UsagePurpose",
                "odrl:operator": "odrl:isAnyOf",
                "odrl:rightOperand": "cx.core.industrycore:1"
            }]
        }]
    }]
}]

def main():
    logger.info("Starting...")

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
        verbose=True,
        logger = logger,
        debug=True
    )

    filter=service.get_filter_expression(
        # key="https://w3id.org/edc/v0.0.1/ns/id",
        key="BusinessPartnerNumber",
        operator="=",
        value=consumerBPN
    )
    #print(f"{filter=}")

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
                counter_party_address=providerURL,
                counter_party_id=providerBPN,
                queryspec=query
            )
            response=service.get_catalog(
                request=catalog
            )
            print(f"{json.dumps(response, indent=2)}")



    """ dsp """
    if args.type == "dsp":

        """ do1 """
        if args.op == "do":
            if not args.id:
                raise(BaseException("Required id"))
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


    logger.info ("Finished.")


if __name__ == "__main__":
    main()
