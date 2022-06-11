from storages.backends.azure_storage import AzureStorage


#

class PublicAzureStorage(AzureStorage):
    account_name = 'philippinesprimary'
    account_key = 'XM4q1Y44PW7aJnuYrTPUOxPl9e4NnFk7GXe+m4IW08sIMlRKcBLqp37rD/j6dzrBwll+tFQ+s9MKtZNGJmHxUQ=='
    azure_container = 'boreco'
    expiration_secs = None


class AzureMediaStorage(AzureStorage):
    location = 'media'
    file_overwrite = False
