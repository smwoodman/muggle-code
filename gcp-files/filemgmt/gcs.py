"""
Functions adapted from sample code from Google. From e.g.:
https://github.com/googleapis/python-storage/tree/main/samples/snippets
https://cloud.google.com/storage/docs/copying-renaming-moving-objects#storage-copy-object-python
"""

from google.cloud import storage

def list_blobs_with_prefix(bucket_name, prefix, delimiter=None, file_substr=None):
    """Lists all the blobs in the bucket that begin with the prefix.

    This can be used to list all blobs in a "folder", e.g. "public/".

    The delimiter argument can be used to restrict the results to only the
    "files" in the given "folder". Without the delimiter, the entire tree under
    the prefix is returned. For example, given these blobs:

        a/1.txt
        a/b/2.txt

    If you specify prefix ='a/', without a delimiter, you'll get back:

        a/1.txt
        a/b/2.txt

    However, if you specify prefix='a/' and delimiter='/', you'll get back
    only the file directly under 'a/':

        a/1.txt

    As part of the response, you'll also get back a blobs.prefixes entity
    that lists the "subfolders" under `a/`:

        a/b/
    """

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    # Note: The call returns a response only when the iterator is consumed.
    file_list = []
    if file_substr is None:
        for blob in blobs:
            file_list.append(blob.name)
    else:
        for blob in blobs:
            if file_substr in blob.name:
                file_list.append(blob.name)

    # if delimiter:
    #     print("Prefixes:")
    #     for prefix in blobs.prefixes:
    #         print(prefix)
    
    return file_list


def copy_blob_client(
    bucket_name, blob_name, destination_bucket_name, destination_blob_name, 
    project_name = "ggn-nmfs-usamlr-dev-7b99"
):
    """
    Copies a blob from one bucket to another, with a new name.
    This function creates the connection to the client - 
    This is necessary for eg parallel runs, where you cannot pass the client directly
    
    https://cloud.google.com/storage/docs/samples/storage-copy-file#storage_copy_file-python
    """
    storage_client = storage.Client(project_name)

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)
    # if destination_bucket.blob(destination_blob_name).exists(storage.Client(project_name)):
    #     return
    # else:
    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
        #if_generation_match=destination_generation_match_precondition,
    )
    
