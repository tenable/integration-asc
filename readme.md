# Tenable.io -> Azure Security Center

> *Please Note:*  This script leverages preview APIs for Azure.
>               While this is expected in this case, this API may change
>               unexpectedly on the Microsoft side moving forward.  You have been warned.
>               We will update this integration as MS updates and GAs their new API for ASC. 

This tool is designed to consume Tenable.io vulnerability data,
transform that data into the Azure Security Center format, and then
upload the resulting data into Azure Security Center.

The tool can be run as either as a one-shot ingest or as a continuous service.

### Requirements for use

* The Azure connector setup and working in your Tenable.io instance
* A set of credentials for the script.  You will need to know the App Secret,
  App id, and Tenant id.  See the [Azure documentation][asc_keys] for
  instructions.
* A set of admin API keys for Tenable.io.  [See the Instructions][tio_keys] on
  Tenable's documenation for more information.
* A host to run the script on.  This can be located anywhere as the script links
  cloud-to-cloud.


### Installing
```shell
pip install .
```

### Options
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

### Usage

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

### Changelog
[Visit the CHANGELOG](CHANGELOG.md)

[tio_keys]: https://docs.tenable.com/cloud/Content/Settings/GenerateAPIKey.htm
[asc_keys]: https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal
