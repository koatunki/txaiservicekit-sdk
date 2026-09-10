

# Prepare the backend services:

1. Follow setup [here](https://github.com/eclipse-tractusx/tractus-x-umbrella/blob/main/docs/user/linux/README.md)
   Use helm install for [Data Exchange Subset (legacy centralized flow)](https://github.com/eclipse-tractusx/tractus-x-umbrella/blob/main/docs/user/linux/README.md#data-exchange-subset-legacy-centralized-flow)

2. Wait until all pods are running:

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


3. Optionally, you can use Bruno script [here](https://github.com/eclipse-tractusx/tractus-x-umbrella/tree/main/docs/common/api/bruno/Umbrella-bru) to check everything is working.

# uv 

The command line to run python for provider and consumer below is using uv, prepare the environment.

```bash
uv venv
source .venv/bin/activate
```

# Provider

1. Create Asset

   ```bash
   uv run provider.py asset create
   ```
   <details> 
   <summary> Results</summary>
   <pre>
   </pre>
   </details>
   <br/>

2. Create Access Policy

   ```bash
   uv run provider policy create-access
   ```
   <details> 
   <summary> Results</summary>
   <pre>
   </pre>
   </details>
   <br/>

3. Create Usage Policy

   ```bash
   uv run provider policy create-usage
   ```
   <details> 
   <summary> Results</summary>
   <pre>
   </pre>
   </details>
   <br/>

4. Create Contract

   ```bash
   uv run provider contract create
   ```
   <details> 
   <summary> Results</summary>
   <pre>
   </pre>
   </details>
   <br/>


# Consumer

1. Show Catalog

   ```bash
   uv run consumer.py catalog listid
   ```
   <details> 
   <summary> Results</summary>
   <pre>
   </pre>
   </details>
   <br/>
   
2. Negotiation

   ```bash
   uf run consumer.py dsp do --id 100
   ```
   <details> 
   <summary> Results</summary>
   <pre>
   </pre>
   </details>
   <br/>