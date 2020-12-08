"""AWS tools."""

import json
import boto3
import pyinputplus as pyip

s3 = boto3.client("s3")
response = s3.list_buckets()
buckets = [bucket["Name"] for bucket in response["Buckets"]]


def list_buckets():
    """Print all buckets."""

    print("\nlist of buckets")
    for num, bucket in enumerate(buckets, 1):
        print(f"{num}. {bucket}")


def keys(bucket_name, prefix="/", delimiter="/"):

    prefix = prefix[1:] if prefix.startswith(delimiter) else prefix
    bucket = boto3.resource("s3").Bucket(bucket_name)
    return (_.key for _ in bucket.objects.filter(Prefix=prefix))


def list_empty_buckets():
    """Scan all buckets and print any that don't contain any objects."""

    print("\nthe following buckets are empty")
    for bucket in buckets:
        _exhausted = object()
        try:
            if next(keys(bucket), _exhausted) == _exhausted:
                print(f"*  {bucket}: is empty")
        except Exception as e:
            print(f"Error: {bucket} - {e}")
    print(f"\nscanned {len(buckets)} buckets\n")


options_map = {
    1: list_buckets,
    2: list_empty_buckets,
}

while True:
    print("\nplease select an option below or nothing to exit\n")
    for num, action in options_map.items():
        print(num, action.__name__)
    user_choice = pyip.inputInt("> ", min=1, blank=True)
    if user_choice != "":
        options_map[user_choice]()
    else:
        print("\nsession complete\n")
        break
