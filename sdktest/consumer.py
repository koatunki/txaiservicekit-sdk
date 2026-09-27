import logging
import argparse
import json
from urllib.parse import urlparse
import requests
from tractusx_sdk.dataspace.services.connector import ServiceFactory
from tractusx_sdk.dataspace.models.connector import ModelFactory

logger = logging.getLogger(__name__)

providerBPN = "BPNL00000003AYRE"
consumerBPN = "BPNL00000003AZQP"

providerURL = "http://dataprovider-controlplane.tx.test/api/v1/dsp"
consumerURL = "http://dataconsumer-1-controlplane.tx.test"

# connector settings (consumer)
connector_base_url = consumerURL
connector_dma_path = "/management"  # Management API path
connector_api_key = "TEST1"
dataspace_version = "jupiter"  # EDC dataspace version

# apisix admin api (via ingress; or kubectl port-forward svc/aiservicedemo-apisix-admin 9180:9180 and use http://127.0.0.1:9180)
apisix_admin_url = "http://apisix-admin.tx.test"
apisix_admin_key = "edd1c9f034335f136f87ad84b625c8f1"  # chart default admin key
apisix_route_id = "dataplane"

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

negotiation_context=[
    "https://w3id.org/catenax/2025/9/policy/odrl.jsonld",
    "https://w3id.org/catenax/2025/9/policy/context.jsonld",
    {"@vocab": "https://w3id.org/edc/v0.0.1/ns/"},
]

def set_apisix_route(route_id, url, token):
    """ route /<route_id>/* on apisix to url, adding the token as Authorization header """
    target = urlparse(url)
    port = target.port or (443 if target.scheme == "https" else 80)
    route = {
        "uri": f"/{route_id}/*",
        "upstream": {
            "type": "roundrobin",
            "scheme": target.scheme,
            "pass_host": "node",
            "nodes": {f"{target.hostname}:{port}": 1},
        },
        "plugins": {
            "proxy-rewrite": {
                "regex_uri": [f"^/{route_id}/(.*)", f"{target.path.rstrip('/')}/$1"],
                "headers": {"set": {"Authorization": token}},
            }
        },
    }
    response = requests.put(
        f"{apisix_admin_url}/apisix/admin/routes/{route_id}",
        headers={"X-API-KEY": apisix_admin_key},
        json=route,
    )
    response.raise_for_status()
    return response.json()

def main():
    logger.info("Starting...")

    # Initialize the parser
    parser = argparse.ArgumentParser(description="A sample Python CLI tool.")

    # Add a positional argument (required by default)
    parser.add_argument("type", type=str, help="catalog, dsp, apisix")
    parser.add_argument("op", type=str, help="list, listid, get; do; setroute")
    parser.add_argument("-i", "--id", type=str, help="Target id")
    parser.add_argument("-u", "--url", type=str, help="Route target url (apisix setroute)")
    parser.add_argument("-t", "--token", type=str, help="Api token for the route target (apisix setroute)")
    parser.add_argument("-r", "--route", type=str, default=apisix_route_id, help="Apisix route id")
    parser.add_argument("-d", "--debug", action="store_true", help="Turn on debug")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")

    # Parse the arguments
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO if args.verbose else logging.WARNING)

    service = ServiceFactory.get_connector_consumer_service(
        dataspace_version=dataspace_version,
        base_url=connector_base_url,
        dma_path=connector_dma_path,
        headers={"X-Api-Key": connector_api_key, "Content-Type": "application/json"},
        verbose=args.verbose,
        logger = logger,
        debug=args.debug
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
                policies=policies_to_accept,
                negotiation_context=negotiation_context
            )
            print(f"{dataplane_proxy_url=}")
            print(f"{access_token=}")

            # Set the counterpart edc url and token to apisix
            response = set_apisix_route(apisix_route_id, dataplane_proxy_url, access_token)
            print(f"{json.dumps(response, indent=2)}")      

    logger.info ("Finished.")


if __name__ == "__main__":
    main()
