import re
from typing import Optional

from google.cloud import storage

from boadata.core.data_node import DataNode
from boadata.core.data_tree import DataTree


@DataTree.register_tree
class BlobNode(DataTree):
    node_type = "GoogleBlob"

    def __init__(
        self,
        parent: Optional[DataNode] = None,
        *,
        blob: Optional[storage.Blob] = None,
        uri: Optional[str] = None,
    ):
        if blob:
            uri = f"gs://{blob.bucket}/{blob.name}"
        super().__init__(parent=parent, uri=uri)

    @property
    def title(self):
        return self.object_name

    @property
    def bucket_name(self) -> str:
        return self.uri.split("://", 1)[1].split("/", 1)[0]

    @property
    def object_name(self) -> str:
        return self.uri.rsplit("/", 1)[1]

    @property
    def object_path(self) -> str:
        return self.uri.split("://", 1)[1].split("/", 1)[1]

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        return re.match("^gs://[a-zA-Z0-9\\-\\.]+/[a-zA-Z0-9\\-\\./]+/$", uri)

    def load_children(self):
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        for blob in client.list_blobs(
            bucket, max_results=1000, prefix=self.object_path
        ):
            self.add_child(BlobNode(parent=self, blob=blob))


@DataTree.register_tree
class BucketNode(DataTree):
    node_type = "GoogleCloudBucket"

    @property
    def bucket_name(self) -> str:
        return self.uri.split("://", 1)[1]

    @property
    def title(self):
        return self.bucket_name

    @classmethod
    def accepts_uri(cls, uri):
        return re.match("^gs://[a-zA-Z0-9\\-\\.]+$", uri)

    def load_children(self):
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        for blob in client.list_blobs(bucket, max_results=1000):
            self.add_child(BlobNode(parent=self, blob=blob))


@DataTree.register_tree
class CloudStorage(DataTree):
    node_type = "GoogleCloudStorage"

    def load_children(self):
        client = storage.Client()
        for bucket in client.list_buckets():
            self.add_child(BucketNode(self, uri=f"gs://{bucket.name}"))

    @classmethod
    def accepts_uri(cls, uri):
        return uri == "gs://"

    @property
    def title(self):
        return "Google Cloud Storage"
