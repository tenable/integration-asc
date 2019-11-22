# Tenable.io for Azure Security Center

> *Please Note:*  This script leverages preview APIs for Azure Security Center (ASC).
>               While this is expected, the API may change
>               unexpectedly on the Microsoft side.  However, we plan to update
>               this integration as Microsoft updates their APIs for ASC. 

This integration is designed to pull Tenable.io vulnerabilities from Azure assets and summarize (count) them by severity. Once the vulnerabilities are summarized for each Azure asset, the integration creates an Azure Security Center recommendation for each host.   The recommendation includes a summary of the number of vulnerabilities on each host and lists them by severity.

This integration can be run as a one-shot ingest or continuous service.


## Requirements

* A working Azure connector in your Tenable.io instance
* A set of Azure credentials for the integration to use.  You will need to know the App Secret,
  App ID, and Tenant ID.  See the [Azure documentation][asc_keys] for
  instructions.
* A set of Tenable.io API keys with the Administrator role.  [See the Tenable.io Generate API Key Instructions][tio_keys] for more information.
* A host to run the script on.  This can be located anywhere as the integrations is linking
  cloud-to-cloud.


## Setup
```shell
pip install .
```

## Options
The following script details, both, command-line arguments and equivalent environment variables.

```
Usage: tenable-asc [OPTIONS]

  Tenable.io -> Azure Security Center Transformer & Ingester

Options:
  --tio-access-key TEXT     Tenable.io Access Key
  --tio-secret-key TEXT     Tenable.io Secret Key
  -b, --batch-size INTEGER  Export/Import Batch Sizing
  -v, --verbose             Logging Verbosity
  -r, --run-every INTEGER   How many hours between recurring imports
  --auth-uri TEXT           Azure Security Center authentication URI
  --azure-uri TEXT          Azure Security Center API base URI
  --azure-app-id TEXT       Azure Security Center application id
  --azure-tenant-id TEXT    Azure Security Center tenant id
  --azure-app-secret TEXT   Azure Security Center application secret
  --help                    Show this message and exit.
```

## Example Usage

Run the import once:

```
tenable-asc                                     \
    --tio-access-key {TIO_ACCESS_KEY}           \
    --tio-secret-key {TIO_SECRET_KEY}           \
    --azure-app-id {AZURE_APP_ID}               \
    --azure-tenant-id {AZURE_TENANT_ID}         \
    --azure-app-secret {AZURE_APP_SECRET}
```

Run the import once an hour:

```
tenable-asc                                     \
    --tio-access-key {TIO_ACCESS_KEY}           \
    --tio-secret-key {TIO_SECRET_KEY}           \
    --azure-app-id {AZURE_APP_ID}               \
    --azure-tenant-id {AZURE_TENANT_ID}         \
    --azure-app-secret {AZURE_APP_SECRET}
    --run-every 1
```

## Changelog
[Visit the CHANGELOG](CHANGELOG.md)

[tio_keys]: https://docs.tenable.com/cloud/Content/Settings/GenerateAPIKey.htm
[asc_keys]: https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal
