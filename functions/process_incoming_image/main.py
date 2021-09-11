"""Process an incoming image."""
import json
from google.cloud import firestore
from google.cloud import storage
from google.cloud import vision


def detect_label_annotations(uri):
    """Return the labels detected by the Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    response = client.label_detection(image=image)
    label_annotations = {}
    labels = []
    for label in response.label_annotations:
        label_annotations[label.description] = {
            "mid": label.mid,
            "description": label.description,
            "score": label.score,
            "topicality": label.topicality,
        }
        labels.append(label.description)
    return labels, label_annotations


def save_to_firestore(blob):
    """Save information about a blob to firestore."""
    client = firestore.Client()
    collection = "images"
    doc_id = blob.id.split("/")[-1]
    ref = client.collection(collection).document(doc_id)
    labels = blob.metadata.get("labels") if blob.metadata else "None"
    label_annotations = blob.metadata.get("label_annotations") if blob.metadata else "None"
    ref.set({
        "bucket": blob.bucket.name,
        "content_type": blob.content_type,
        "crc32c": blob.crc32c,
        "labels": eval(labels),
        "label_annotations": eval(label_annotations),
        "md5_hash": blob.md5_hash,
        "object_name": blob.name,
        "size": blob.size,
        "storage_class": blob.storage_class,
        "time_created": blob.time_created,
        "uri": f"gs://{blob.bucket.name}/{blob.name}",
    })


def process_incoming_image(event, context):
    """Process an incoming image."""
    bucket_name = event["bucket"]
    object_name = event["name"]

    # get label annotations from vision api
    uri = f"gs://{bucket_name}/{object_name}"
    labels, label_annotations = detect_label_annotations(uri)

    # update object metatdata
    client = storage.Client()
    blob = client.bucket(bucket_name).get_blob(object_name)
    blob.metadata = {
        "labels": labels,
        "label_annotations": label_annotations,
    }
    blob.patch()

    # save object in firestore
    save_to_firestore(blob)


if __name__ == "__main__":
    class Context:
        event_id = "1234567890"
        event_type = "OBJECT_FINALIZE"
    event = {
        "bucket": "lukwam-banksy-incoming",
        "name": "Bristol-Totterdown2400.jpeg",
        "metageneration": "123456",
        "timeCreated": "2021-01-15T01:30:15.01Z",
        "updated": "",
    }
    process_incoming_image(event, Context())
