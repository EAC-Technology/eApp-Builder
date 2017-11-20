import os

promail_cloud_host_start = 'promail-pis'

def is_cloud_version(host=None):
    return os.environ.get('CLOUD_DOMAIN') is not None

def promail_domain():
    cloud_domain = os.environ.get('CLOUD_DOMAIN')
    if not cloud_domain:
        cloud_domain = 'appinmail.io'
    return cloud_domain.lstrip('.')
