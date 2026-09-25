

# Prepare the backend services:

## 1. Follow setup [here](https://github.com/eclipse-tractusx/tractus-x-umbrella/blob/main/docs/user/linux/README.md)
   Use helm install for [Data Exchange Subset (legacy centralized flow)](https://github.com/eclipse-tractusx/tractus-x-umbrella/blob/main/docs/user/linux/README.md#data-exchange-subset-legacy-centralized-flow)

## 2. Wait until all pods status are running and/or completed:
```bash
kubectl get pods --namespace umbrella
```
<details> 
<summary> Results</summary>
<pre>
NAME                                                              READY   STATUS      RESTARTS       AGE
dataprovider-digital-twin-db-0                                    1/1     Running     0              3d4h
ssi-dim-wallet-stub-6797d6cfc7-dlwqv                              1/1     Running     2 (3d4h ago)   3d4h
umbrella-dataconsumer-1-db-0                                      1/1     Running     0              3d4h
umbrella-dataconsumer-1-edc-controlplane-75468479b8-24m2t         1/1     Running     0              3d4h
umbrella-dataconsumer-1-edc-dataplane-c6897fc5d-dqlg8             1/1     Running     1 (3d4h ago)   3d4h
umbrella-dataprovider-db-0                                        1/1     Running     0              3d4h
umbrella-dataprovider-dtr-6fd7445b-t8gjg                          1/1     Running     2 (3d4h ago)   3d4h
umbrella-dataprovider-edc-controlplane-755b45bdfb-n6q7g           1/1     Running     0              3d4h
umbrella-dataprovider-edc-dataplane-6796845bc-526b6               1/1     Running     0              3d4h
umbrella-dataprovider-submodelserver-7f95c7fff-kmml7              1/1     Running     0              3d4h
umbrella-edc-dataconsumer-1-vault-0                               1/1     Running     0              3d4h
umbrella-edc-dataconsumer-1-vault-agent-injector-7b9cd94892c7rl   1/1     Running     0              3d4h
umbrella-edc-dataprovider-vault-0                                 1/1     Running     0              3d4h
umbrella-edc-dataprovider-vault-agent-injector-7879866b88-jhtt9   1/1     Running     0              3d4h
umbrella-pgadmin4-768675f5d7-j8h6s                                1/1     Running     0              3d4h
umbrella-portal-portal-migrations-wm845                           0/1     Completed   0              3d4h
umbrella-portal-provisioning-migrations-g98z8                     0/1     Completed   0              3d4h
wallet-postgres-0                                                 1/1     Running     0              3d4h
</pre>
</details>
<br/>

## 3. Optionally, you can use Bruno script [here](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/docs/common/api/bruno/Umbrella-bru) to check everything is working.

# uv 

The command line to run python for provider and consumer below is using uv, prepare the environment.

```bash
uv venv
source .venv/bin/activate
```

# Provider

## 1. Create Asset

```bash
uv run provider.py asset create
```
<details> 
<summary> Results</summary>
<pre>
Starting...
asset_id='100'
INFO:__main__:Creating asset 100 at http://a2a.agent.test.tx.
INFO:__main__:[Connector Service] [ASSET REQUEST]: {"@context": {"edc": "https://w3id.org/edc/v0.0.1/ns/", "cx-common": "https://w3id.org/catenax/ontology/common#", "cx-taxo": "https://w3id.org/catenax/taxonomy#", "dct": "http://purl.org/dc/terms/"}, "@type": "Asset", "@id": "100", "properties": {"cx-common:version": "3.0", "ai-catalog": {"type": "a2a", "description": "ai agent"}}, "privateProperties": {}, "dataAddress": {"@type": "DataAddress", "type": "HttpData", "baseUrl": "http://a2a.agent.test.tx", "proxyQueryParams": "false", "proxyPath": "true", "proxyMethod": "true", "proxyBody": "false"}}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): dataprovider-controlplane.tx.test:80
DEBUG:urllib3.connectionpool:http://dataprovider-controlplane.tx.test:80 "POST /management/v3/assets HTTP/1.1" 200 296
INFO:__main__:Asset 100 created successfully.
response:
{
  "@type": "IdResponse",
  "@id": "100",
  "createdAt": 1789056133100,
  "@context": [
    "https://w3id.org/catenax/2025/9/policy/context.jsonld",
    {
      "tx-auth": "https://w3id.org/tractusx/auth/",
      "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
      "edc": "https://w3id.org/edc/v0.0.1/ns/",
      "odrl": "http://www.w3.org/ns/odrl/2/"
    }
  ]
}
DEBUG:urllib3.connectionpool:http://dataprovider-controlplane.tx.test:80 "GET /management/v3/assets/100 HTTP/1.1" 200 581
get:
{
  "@id": "100",
  "@type": "Asset",
  "properties": {
    "ai-catalog": {
      "type": "a2a",
      "description": "ai agent"
    },
    "https://w3id.org/catenax/ontology/common#version": "3.0",
    "id": "100"
  },
  "dataAddress": {
    "@type": "DataAddress",
    "proxyPath": "true",
    "type": "HttpData",
    "proxyMethod": "true",
    "proxyQueryParams": "false",
    "proxyBody": "false",
    "baseUrl": "http://a2a.agent.test.tx"
  },
  "@context": [
    "https://w3id.org/catenax/2025/9/policy/context.jsonld",
    {
      "tx-auth": "https://w3id.org/tractusx/auth/",
      "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
      "edc": "https://w3id.org/edc/v0.0.1/ns/",
      "odrl": "http://www.w3.org/ns/odrl/2/"
    }
  ]
}
Finished.
</pre>
</details>
<br/>

## 2. Create Access Policy

```bash
uv run provider.py policy create-access
```
<details> 
<summary> Results</summary>
<pre>
Starting...
INFO:__main__:Creating new policy with ID 101.
INFO:__main__:[Connector Service] [POLICY REQUEST]: {"@context": ["https://w3id.org/dspace/2025/1/odrl-profile.jsonld", "https://w3id.org/catenax/2025/9/policy/context.jsonld", {"@vocab": "https://w3id.org/edc/v0.0.1/ns/"}], "@type": "PolicyDefinition", "@id": "101", "policy": {"@context": "http://www.w3.org/ns/odrl.jsonld", "@type": "odrl:Set", "permission": [{"action": "access", "constraint": [{"and": [{"leftOperand": "Membership", "operator": "eq", "rightOperand": "active"}, {"leftOperand": "BusinessPartnerNumber", "operator": "isAnyOf", "rightOperand": ["BPNL00000003AZQP"]}]}]}], "prohibition": [], "obligation": []}}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): dataprovider-controlplane.tx.test:80
DEBUG:urllib3.connectionpool:http://dataprovider-controlplane.tx.test:80 "POST /management/v3/policydefinitions HTTP/1.1" 200 296
INFO:__main__:Policy 101 created successfully.
DEBUG:urllib3.connectionpool:http://dataprovider-controlplane.tx.test:80 "GET /management/v3/policydefinitions/101 HTTP/1.1" 200 770
{
  "@id": "101",
  "@type": "PolicyDefinition",
  "createdAt": 1789056477077,
  "policy": {
    "@id": "36d1d8f5-2e5a-42b5-b84d-ceed5a8aa751",
    "@type": "odrl:Set",
    "odrl:permission": {
      "odrl:action": {
        "@id": "cx-policy:access"
      },
      "odrl:constraint": {
        "odrl:and": [
          {
            "odrl:leftOperand": {
              "@id": "cx-policy:Membership"
            },
            "odrl:operator": {
              "@id": "odrl:eq"
            },
            "odrl:rightOperand": "active"
          },
          {
            "odrl:leftOperand": {
              "@id": "cx-policy:BusinessPartnerNumber"
            },
            "odrl:operator": {
              "@id": "odrl:isAnyOf"
            },
            "odrl:rightOperand": "BPNL00000003AZQP"
          }
        ]
      }
    },
    "odrl:prohibition": [],
    "odrl:obligation": []
  },
  "@context": [
    "https://w3id.org/catenax/2025/9/policy/context.jsonld",
    {
      "tx-auth": "https://w3id.org/tractusx/auth/",
      "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
      "edc": "https://w3id.org/edc/v0.0.1/ns/",
      "odrl": "http://www.w3.org/ns/odrl/2/"
    }
  ]
}
Finished.
</pre>
</details>
<br/>

## 3. Create Usage Policy

```bash
uv run provider.py policy create-usage
```
<details> 
<summary> Results</summary>
<pre>
Starting...
INFO:__main__:Creating new policy with ID 102.
INFO:__main__:[Connector Service] [POLICY REQUEST]: {"@context": ["https://w3id.org/dspace/2025/1/odrl-profile.jsonld", "https://w3id.org/catenax/2025/9/policy/context.jsonld", {"@vocab": "https://w3id.org/edc/v0.0.1/ns/"}, {}], "@type": "PolicyDefinition", "@id": "102", "policy": {"@context": "http://www.w3.org/ns/odrl.jsonld", "@type": "odrl:Set", "permission": [{"action": "use", "constraint": {"and": [{"leftOperand": "Membership", "operator": "eq", "rightOperand": "active"}, {"leftOperand": "FrameworkAgreement", "operator": "eq", "rightOperand": "DataExchangeGovernance:1.0"}, {"leftOperand": "UsagePurpose", "operator": "isAnyOf", "rightOperand": ["cx.core.industrycore:1"]}]}}], "prohibition": [], "obligation": []}}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): dataprovider-controlplane.tx.test:80
DEBUG:urllib3.connectionpool:http://dataprovider-controlplane.tx.test:80 "POST /management/v3/policydefinitions HTTP/1.1" 200 296
INFO:__main__:Policy 102 created successfully.
DEBUG:urllib3.connectionpool:http://dataprovider-controlplane.tx.test:80 "GET /management/v3/policydefinitions/102 HTTP/1.1" 200 902
{
  "@id": "102",
  "@type": "PolicyDefinition",
  "createdAt": 1789056538925,
  "policy": {
    "@id": "36f68aa1-c7b8-432c-9859-138eaa8a7097",
    "@type": "odrl:Set",
    "odrl:permission": {
      "odrl:action": {
        "@id": "odrl:use"
      },
      "odrl:constraint": {
        "odrl:and": [
          {
            "odrl:leftOperand": {
              "@id": "cx-policy:Membership"
            },
            "odrl:operator": {
              "@id": "odrl:eq"
            },
            "odrl:rightOperand": "active"
          },
          {
            "odrl:leftOperand": {
              "@id": "cx-policy:FrameworkAgreement"
            },
            "odrl:operator": {
              "@id": "odrl:eq"
            },
            "odrl:rightOperand": "DataExchangeGovernance:1.0"
          },
          {
            "odrl:leftOperand": {
              "@id": "cx-policy:UsagePurpose"
            },
            "odrl:operator": {
              "@id": "odrl:isAnyOf"
            },
            "odrl:rightOperand": "cx.core.industrycore:1"
          }
        ]
      }
    },
    "odrl:prohibition": [],
    "odrl:obligation": []
  },
  "@context": [
    "https://w3id.org/catenax/2025/9/policy/context.jsonld",
    {
      "tx-auth": "https://w3id.org/tractusx/auth/",
      "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
      "edc": "https://w3id.org/edc/v0.0.1/ns/",
      "odrl": "http://www.w3.org/ns/odrl/2/"
    }
  ]
}
Finished.
</pre>
</details>
<br/>

## 4. Create Contract

```bash
uv run provider.py contract create
```
<details> 
<summary> Results</summary>
<pre>
Starting...
INFO:__main__:Creating new contract with ID 103.
INFO:__main__:[Connector Service] [CONTRACT DEFINITION REQUEST]: {"@context": {"@vocab": "https://w3id.org/edc/v0.0.1/ns/"}, "@type": "ContractDefinition", "@id": "103", "accessPolicyId": "101", "contractPolicyId": "102", "assetsSelector": [{"operandLeft": "https://w3id.org/edc/v0.0.1/ns/id", "operator": "=", "operandRight": "100"}]}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): dataprovider-controlplane.tx.test:80
DEBUG:urllib3.connectionpool:http://dataprovider-controlplane.tx.test:80 "POST /management/v3/contractdefinitions HTTP/1.1" 200 296
INFO:__main__:Contract 103 created successfully.
DEBUG:urllib3.connectionpool:http://dataprovider-controlplane.tx.test:80 "GET /management/v3/contractdefinitions/103 HTTP/1.1" 200 451
{
  "@id": "103",
  "@type": "ContractDefinition",
  "accessPolicyId": "101",
  "contractPolicyId": "102",
  "assetsSelector": {
    "@type": "Criterion",
    "operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
    "operator": "=",
    "operandRight": "100"
  },
  "@context": [
    "https://w3id.org/catenax/2025/9/policy/context.jsonld",
    {
      "tx-auth": "https://w3id.org/tractusx/auth/",
      "@vocab": "https://w3id.org/edc/v0.0.1/ns/",
      "edc": "https://w3id.org/edc/v0.0.1/ns/",
      "odrl": "http://www.w3.org/ns/odrl/2/"
    }
  ]
}
Finished.
</pre>
</details>
<br/>


# Consumer

## 1. Show Catalog

```bash
uv run consumer.py catalog listid
```
<details> 
<summary> Results</summary>
<pre>
INFO:__main__:Starting...
INFO:__main__:[Connector Service] [CATALOG REQUEST]: {"@context": {"edc": "https://w3id.org/edc/v0.0.1/ns/", "odrl": "http://www.w3.org/ns/odrl/2/", "dct": "https://purl.org/dc/terms/"}, "@type": "CatalogRequest", "counterPartyAddress": "http://dataprovider-controlplane.tx.test/api/v1/dsp", "counterPartyId": "BPNL00000003AYRE", "protocol": "dataspace-protocol-http", "additionalScopes": [], "querySpec": {}}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): dataconsumer-1-controlplane.tx.test:80
DEBUG:urllib3.connectionpool:http://dataconsumer-1-controlplane.tx.test:80 "POST /management/v3/catalog/request HTTP/1.1" 200 3068
  2e807099-1107-4b2c-bae2-a0bf6154e391
  100
    MTAz:MTAw:ZDBkNjMxMWItZjM2MC00OWRmLWFlNDctN2I3MTQwOWZiNTAx
INFO:__main__:Finished.
</pre>
</details>
<br/>
   
## 2. Negotiation

```bash
uv run consumer.py dsp do --id 100
```
<details> 
<summary> Results</summary>
<pre>
INFO:__main__:Starting...
INFO:__main__:[Connector Service]: The EDR was not found in the cache for counter_party_address=[http://dataprovider-controlplane.tx.test/api/v1/dsp], counter_party_id=[BPNL00000003AYRE], filter=[{'operandLeft': 'https://w3id.org/edc/v0.0.1/ns/id', 'operator': '=', 'operandRight': '100'}] and selected policies, starting new contract negotiation!
INFO:__main__:[Connector Service] [CATALOG REQUEST]: {"@context": {"edc": "https://w3id.org/edc/v0.0.1/ns/", "odrl": "http://www.w3.org/ns/odrl/2/", "dct": "https://purl.org/dc/terms/"}, "@type": "CatalogRequest", "counterPartyAddress": "http://dataprovider-controlplane.tx.test/api/v1/dsp", "counterPartyId": "BPNL00000003AYRE", "protocol": "dataspace-protocol-http", "additionalScopes": [], "querySpec": {"@context": {"@vocab": "https://w3id.org/edc/v0.0.1/ns/"}, "@type": "QuerySpec", "filterExpression": {"operandLeft": "https://w3id.org/edc/v0.0.1/ns/id", "operator": "=", "operandRight": "100"}}}
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): dataconsumer-1-controlplane.tx.test:80
DEBUG:urllib3.connectionpool:http://dataconsumer-1-controlplane.tx.test:80 "POST /management/v3/catalog/request HTTP/1.1" 200 3068
DEBUG:tractusx_sdk.dataspace.tools.dsp_tools:Policy matched allowed policy at index 0.
INFO:__main__:[Connector Service] [NEGOTIATION REQUEST]: {"@context": {"@vocab": "https://w3id.org/edc/v0.0.1/ns/"}, "@type": "ContractRequest", "counterPartyAddress": "http://dataprovider-controlplane.tx.test/api/v1/dsp", "protocol": "dataspace-protocol-http", "policy": {"@id": "MTAz:MTAw:ZjU3MjYwZWQtOTA5My00NmU0LWE3MTYtM2U4YTI2MDg0N2Yz", "@type": "odrl:Offer", "assigner": "BPNL00000003AYRE", "target": "100", "odrl:permission": {"odrl:action": {"@id": "odrl:use"}, "odrl:constraint": {"odrl:and": [{"odrl:leftOperand": {"@id": "https://w3id.org/catenax/2025/9/policy/Membership"}, "odrl:operator": {"@id": "odrl:eq"}, "odrl:rightOperand": "active"}, {"odrl:leftOperand": {"@id": "https://w3id.org/catenax/2025/9/policy/FrameworkAgreement"}, "odrl:operator": {"@id": "odrl:eq"}, "odrl:rightOperand": "DataExchangeGovernance:1.0"}, {"odrl:leftOperand": {"@id": "https://w3id.org/catenax/2025/9/policy/UsagePurpose"}, "odrl:operator": {"@id": "odrl:isAnyOf"}, "odrl:rightOperand": "cx.core.industrycore:1"}]}}, "odrl:prohibition": [], "odrl:obligation": []}, "callbackAddresses": []}
DEBUG:urllib3.connectionpool:http://dataconsumer-1-controlplane.tx.test:80 "POST /management/v3/edrs HTTP/1.1" 400 387
Traceback (most recent call last):
  File "/home/ubuntu/github/koatunki/txaiservicekit-sdk/consumer.py", line 184, in <module>
    main()
    ~~~~^^
  File "/home/ubuntu/github/koatunki/txaiservicekit-sdk/consumer.py", line 170, in main
    dataplane_proxy_url, access_token = service.do_dsp(
                                        ~~~~~~~~~~~~~~^
        counter_party_id=providerBPN,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        policies=policies_to_accept
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/github/koatunki/txaiservicekit-sdk/.venv/lib/python3.14/site-packages/tractusx_sdk/dataspace/services/connector/base_connector_consumer.py", line 1700, in do_dsp
    transfer_id = self.get_transfer_id(
        counter_party_id=counter_party_id,
    ...<7 lines>...
        negotiation_context=negotiation_context
    )
  File "/home/ubuntu/github/koatunki/txaiservicekit-sdk/.venv/lib/python3.14/site-packages/tractusx_sdk/dataspace/services/connector/jupiter/connector_consumer_service.py", line 78, in get_transfer_id
    return super().get_transfer_id(
           ~~~~~~~~~~~~~~~~~~~~~~~^
        counter_party_id=counter_party_id,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<7 lines>...
        negotiation_context=negotiation_context,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/github/koatunki/txaiservicekit-sdk/.venv/lib/python3.14/site-packages/tractusx_sdk/dataspace/services/connector/base_connector_consumer.py", line 1299, in get_transfer_id
    edr_entry: dict = self.negotiate_and_transfer(counter_party_id=counter_party_id,
                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                  counter_party_address=counter_party_address, policies=policies,
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
                                                  catalog_context=catalog_context,
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                  negotiation_context=negotiation_context)
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/github/koatunki/txaiservicekit-sdk/.venv/lib/python3.14/site-packages/tractusx_sdk/dataspace/services/connector/base_connector_consumer.py", line 1201, in negotiate_and_transfer
    negotiation_id = self._start_negotiation_for_assets(
        counter_party_id=counter_party_id,
    ...<2 lines>...
        **negotiation_kwargs
    )
  File "/home/ubuntu/github/koatunki/txaiservicekit-sdk/.venv/lib/python3.14/site-packages/tractusx_sdk/dataspace/services/connector/base_connector_consumer.py", line 973, in _start_negotiation_for_assets
    raise RuntimeError(
        f"[Connector Service]: [{counter_party_address}] It was not possible to start the EDR Negotiation! The negotiation id is empty!")
RuntimeError: [Connector Service]: [http://dataprovider-controlplane.tx.test/api/v1/dsp] It was not possible to start the EDR Negotiation! The negotiation id is empty!
</pre>
</details>
<br/>