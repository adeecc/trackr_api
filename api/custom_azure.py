import os

from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'shiftrio'
    account_key = os.environ.get('AZURE_ACCOUNT_KEY')
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'shiftrio' # Must be replaced by your storage_account_name
    account_key = os.environ.get('AZURE_ACCOUNT_KEY') # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None