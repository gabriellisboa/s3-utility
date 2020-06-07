# S3 utility
This project aims to fetch this specific information about all your s3 buckets all the regions. This informations are:

- Name

- Creation date

- Number of files

- Total size of files in KB

- Last modified date of the most recent file

- How much the storage costs (calculates considering all storage types using curent s3 billing value from pricing API)

You need to have aws-cli configured at your local environment and credentials with pricing, s3 and cloudwatch permissions. Boto3 will automatcaly use your local awscli credentials.
You can pass the --extra-info tag to show extra info about the bucket.


### To run:

```sh

$ cd s3-utility/

$ sudo docker image build -t s3-utility:1.0 .

$ sudo docker container run -i s3-utility:1.0

```

### TODOS:
- Test against account with lots of files and buckets;
- Unit testing;
- Filter buckets: support prefixes;
- Additional info for bucket with --extra-info
- Parallelize buckets creation in main