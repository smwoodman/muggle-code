"""
Miscellaneous functions for managing files in GCS buckets

Documentation for common arguments:
header_src: the source 'bucket name + project + year'.  
    Replaced in the path by header_dest
header_dest: the destination 'bucket name + project + year'. 
    Repalces `header_src` in the destination path
"""

import subprocess


def replace_path(file_src, file_substr, header_src, header_dest):
    """
    Replace GCS path text, for moving files
    from the old AMLR bucket, amlr-imagery-proc-dev, to the new
    bucket, amlr-gliders-imagery-proc-dev

    file_src:    The file source string
    file_substr: The file substring
    header_ : see top of the file
    """
    x = file_src
    x = x.replace(f"{header_src}", f"{header_dest}")
    if (file_substr == "jpgorig-regions"):
        x = x.replace("/shadowgraph/images", f"/{file_substr}")
    else:
        x = x.replace("/shadowgraph/images", f"/images{file_substr}")

    x = x.replace("/output", "")

    return x

def rsync_imagery_proc_regions(path_src, header_src, header_dest, text_only = False):
    """
    Build and execute `gcloud storage rsync` command for moving 'region'
    folders from the old AMLR bucket, amlr-imagery-proc-dev, to the new
    bucket, amlr-gliders-imagery-proc-dev

    path_src: the source bucket path
    header_ : see top of the file
    text_only: boolean flag for if the command should actually be run
    """

    # i_orig = i
    x = path_src
    x = x.replace(f"gs://{header_src}", f"gs://{header_dest}")
    x = x.replace("/shadowgraph/", "/")
    x = x.replace("/regions", "")
    x = x.replace("/images/", "/regions/")
    path_dest = x

    run_list = ["gcloud", "storage", "rsync", "-r", path_src, path_dest]
    
    if text_only:
        return(" ".join(run_list))
    else:
        run_out = subprocess.run(run_list, capture_output=True)
        if run_out.returncode != 0:
            print(f'Error')
            print(f'ARGS:\n{run_out.args}')
            print(f'STDERR:\n{run_out.stderr}')
            return(f'ERROR: {run_out.args}')
        else:
            return(f'Success: {run_out.args}')
        
