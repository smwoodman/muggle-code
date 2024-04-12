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
    # print("Blobs:")
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


def move_blob(storage_client, bucket_name, blob_name, destination_bucket_name, destination_blob_name):
    """
    Moves a blob from one bucket to another with a new name.
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # blob_name = "your-object-name"
    # The ID of the bucket to move the object to
    # destination_bucket_name = "destination-bucket-name"
    # The ID of your new GCS object (optional)
    # destination_blob_name = "destination-object-name"
    
    """
    # SMW: moved storage_client to an argument, so it isn't generated each time=
    # storage_client = storage.Client()

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    # There is also an `if_source_generation_match` parameter, which is not used in this example.
    destination_generation_match_precondition = 0

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name, if_generation_match=destination_generation_match_precondition,
    )
    source_bucket.delete_blob(blob_name)

    print(
        "Blob {} in bucket {} moved to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )
    
def copy_blob(
    source_bucket, blob_name, destination_bucket, destination_blob_name,
):
    """
    Copies a blob from one bucket to another with a new name.
    https://cloud.google.com/storage/docs/samples/storage-copy-file#storage_copy_file-python
    """
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    # destination_bucket_name = "destination-bucket-name"
    # destination_blob_name = "destination-object-name"

    # storage_client = storage.Client()

    # source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    # destination_bucket = storage_client.bucket(destination_bucket_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to copy is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    # There is also an `if_source_generation_match` parameter, which is not used in this example.
    destination_generation_match_precondition = 0

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
        #if_generation_match=destination_generation_match_precondition,
    )

    # print(
    #     "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
    #         source_blob.name,
    #         source_bucket.name,
    #         blob_copy.name,
    #         destination_bucket.name,
    #     )
    # )
    
def copy_blob_if_new(
    source_bucket, blob_name, destination_bucket, destination_blob_name
):
    """
    Wrapper around copy_blob - 
    only try to copy blob if destination blob does not already exist
    """
    # destination_bucket = storage_client.bucket(destination_bucket_name)
    if destination_bucket.blob(destination_blob_name).exists():
        return
    else:
        copy_blob(source_bucket, blob_name, 
                  destination_bucket, destination_blob_name)
        
def copy_blob_client_ifnew(
    project_name, bucket_name, blob_name, destination_bucket_name, destination_blob_name
):
    """
    Copies a blob from one bucket to another with a new name.
    https://cloud.google.com/storage/docs/samples/storage-copy-file#storage_copy_file-python
    """
    storage_client = storage.Client(project_name)

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)
    if destination_bucket.blob(destination_blob_name).exists():
        return
    else:
         blob_copy = source_bucket.copy_blob(
            source_blob, destination_bucket, destination_blob_name
            #if_generation_match=destination_generation_match_precondition,
        )
    

def move_blob_wrapper(file_old):
    storage_client = storage.Client()
    bucket_name = "amlr-imagery-proc-dev"
    file_new = file_old.replace("/images/", "/images-ffPCG/").replace("/output/", "/")

    # return [bucket_name, file_old, bucket_name, file_new]
    move_blob(storage_client, bucket_name, file_old, bucket_name, file_new)
    
    
    
    
def rsync_build_run(src, bucket_name_src, bucket_name_dest, print_only=False):
    # i_orig = i
    x = src
    x = x.replace(f"gs://{bucket_name_src}/gliders/2022", 
                  f"gs://{bucket_name_dest}/FREEBYRD/2023")
    x = x.replace("/shadowgraph/", "/")
    x = x.replace("/regions", "")
    x = x.replace("/images/", "/regions/")
    dest = x

    run_list = ["gcloud", "storage", "rsync", "-r", src, dest]
    
    if print_only:
        return(" ".join(run_list))
    else:
        # return("tmp")
        run_out = subprocess.run(run_list, capture_output=True)
        if run_out.returncode != 0:
            print(f'Error')
            print(f'ARGS:\n{run_out.args}')
            print(f'STDERR:\n{run_out.stderr}')
            return(f'ERROR: {run_out.args}')
        else:
            return(f'Success: {run_out.args}')
        