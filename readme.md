# Tenable.io for Azure Security Center

> *Please Note:*  This script leverages preview APIs for Azure Security Center.
>               While this is expected in this case, this API may change
>               unexpectedly on the Microsoft side moving forward.  You have been warned.
>               We will update this integration as MS updates and GAs their new API for ASC. 

This integration is designed to pull Tenable.io for vulnerabilities on Azure assets and summarize (count) them by severity.
Once the vulnerabilities are summarized for each Azure asset it creates a Azure Security Center recommendation for each host with a summary of the number of vulnerabilities on that host by severity.

This integration can be run as a one-shot ingest or as a continuous service.

## Requirements

* The Tenable.io Azure connector must be setup and working correctly in your Tenable.io instance
* A set of Azure credentials for the integration to use.  You will need to know the App Secret,
  App id, and Tenant id.  See the [Azure documentation][asc_keys] for
  instructions.
* A set of Tenable.io API keys with the Administrator role.  [See the Instructions][tio_keys] on
  Tenable's documentation for more information.
* A host to run the script on.  This can be located anywhere as the integrations is linking
  cloud-to-cloud.


## Setup
```shell
pip install .
```

## Options
The following below details both the command-line arguments as well as the
equivalent environment variables.

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
