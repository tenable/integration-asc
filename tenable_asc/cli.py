#!/usr/bin/env python
'''
MIT License

Copyright (c) 2019 Tenable Network Security, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import click, logging, time
from tenable.io import TenableIO
from .asc import AzureSecurityCenter
from .transform import Tio2ASC
from . import __version__


@click.command()
@click.option('--tio-access-key',
    envvar='TIO_ACCESS_KEY', help='Tenable.io Access Key')
@click.option('--tio-secret-key',
    envvar='TIO_SECRET_KEY', help='Tenable.io Secret Key')
@click.option('--batch-size', '-b', envvar='BATCH_SIZE', default=1000,
    type=click.INT, help='Export/Import Batch Sizing')
@click.option('--verbose', '-v', envvar='VERBOSITY', default=0,
    count=True, help='Logging Verbosity')
@click.option('--run-every', '-r', envvar='RUN_EVERY',
    type=click.INT, help='How many hours between recurring imports')
@click.option('--auth-uri', envvar='AZURE_AUTH_URI',
    help='Azure Security Center authentication URI',
    default='https://login.microsoftonline.com')
@click.option('--azure-uri', envvar='AZURE_API_URI',
    help='Azure Security Center API base URI',
    default='https://management.azure.com')
@click.option('--azure-app-id', envvar='AZURE_APP_ID',
    help='Azure Security Center application id')
@click.option('--azure-tenant-id', envvar='AZURE_TENANT_ID',
    help='Azure Security Center tenant id')
@click.option('--azure-app-secret', envvar='AZURE_APP_SECRET',
    help='Azure Security Center application secret')
@click.option('--subscription', '-s', multiple=True,
    help='Only upload this subscription to Azure')
def cli(tio_access_key, tio_secret_key, batch_size, verbose,
        run_every, auth_uri, azure_uri, azure_app_id,
        azure_tenant_id, azure_app_secret, subscription):
    '''
    Tenable.io -> Azure Security Center Transformer & Ingester
    '''
    # Setup the logging verbosity.
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose > 1:
        logging.basicConfig(level=logging.DEBUG)

    # Initiate the Tenable.io API model, the Ingester model, and start the
    # ingestion and data transformation.
    tio = TenableIO(tio_access_key, tio_secret_key,
        vendor='Tenable',
        product='Azure Security Center',
        build=__version__)
    asc = AzureSecurityCenter(
        azure_tenant_id,
        azure_app_id,
        azure_app_secret,
        auth_url=auth_uri,
        url=azure_uri
    )
    ingest = Tio2ASC(tio, asc, allowed_subs=subscription)
    ingest.ingest(batch_size)

    # If we are expected to continually re-run the transformer, then we will
    # need to track the passage of time and run every X hours, where X is
    # defined by the user.
    if run_every and run_every > 0:
        while True:
            sleeper = run_every * 3600
            last_run = int(time.time())
            logging.info(
                'Sleeping for {}s before next iteration'.format(sleeper))
            time.sleep(sleeper)
            logging.info(
                'Initiating ingest with observed_since={}'.format(last_run))
            ingest.ingest(last_run, batch_size, threads)