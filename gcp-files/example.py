# https://codeburst.io/creating-local-python-packages-with-init-py-aa19f1e9e80f

from filemgmt import rsync_imagery_proc_regions
# from time_pkg import ssep
# from print_pkg.printer import hello
# from print_pkg.printer import output
    
def main():
    x = rsync_imagery_proc_regions(
        "gs://amlr-imagery-proc-dev/gliders/2022/amlr08-20220513/shadowgraph/images/Dir0047/regions", 
        "amlr-imagery-proc-dev/gliders/2022", 
        "amlr-gliders-imagery-proc-dev/SANDIEGO/2022", 
        text_only=True
    )

    print(x)

if __name__ == "__main__":
    main()