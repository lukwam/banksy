"""Banksy app."""
import json
from datetime import timedelta
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from google.cloud import firestore
from google.cloud import storage

app = Flask(__name__)


def copy_object(bucket_name, object_name, dest_bucket_name, dest_object_name):
    """Copy an object from one bucket to another."""
    client = storage.Client()
    source_bucket = client.bucket(bucket_name)
    source_blob = source_bucket.blob(object_name)
    dest_bucket = client.bucket(dest_bucket_name)
    source_uri = f"gs://{bucket_name}/{object_name}"
    dest_uri = f"gs://{dest_bucket_name}/{dest_object_name}"
    print(f"Copying {source_uri} to {dest_uri}...")
    return source_bucket.copy_blob(
        source_blob,
        dest_bucket,
        dest_object_name
    )


def delete_object(bucket_name, object_name):
    """Delete an object."""
    client = storage.Client()
    return client.bucket(bucket_name).blob(object_name).delete()


def get_image(start_after=None, start_before=None):
    """Return the next image from Firestore."""
    client = firestore.Client()
    collection = "incoming"
    ref = client.collection(collection)
    if start_after:
        ref = ref.order_by("blob_id")
        ref = ref.start_after({"blob_id": start_after})
    elif start_before:
        ref = ref.order_by("blob_id", direction=firestore.Query.DESCENDING)
        ref = ref.start_after({"blob_id": start_before})
    for result in ref.limit(1).stream():
        return result.to_dict()


def get_signed_url(image):
    """Return a signed url for the given object."""
    bucket_name = image["bucket"]
    object_name = image["object_name"]
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="GET",
    )


def render_theme(body):
    """Render the theme."""
    return render_template(
        "theme.html",
        body=body,
    )


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    start_after = request.args.get("start_after")
    start_before = request.args.get("start_before")
    first = False
    if not start_after and not start_before:
        first = True
    image = get_image(
        start_after=start_after,
        start_before=start_before,
    )
    if not image:
        image = get_image()
    url = None
    if image:
        url = get_signed_url(image)
    body = render_template(
        "index.html",
        first=first,
        image=image,
        url=url,
    )
    return render_theme(body)


@app.route('/banksy/<blob_id>')
def banksy(blob_id):
    """Confirm an incoming image as Banksy."""
    dest_bucket_name = "lukwam-banksy-confirmed"
    dest_object_name = f"{blob_id}.jpg"

    # get the incoming firestore record
    client = firestore.Client()
    incoming_ref = client.collection("incoming").document(blob_id)
    incoming = incoming_ref.get().to_dict()
    bucket_name = incoming["bucket"]
    object_name = incoming["object_name"]

    # copy the blob to the banksy bucket
    blob = copy_object(
        bucket_name,
        object_name,
        dest_bucket_name,
        dest_object_name
    )

    # create the new firestore record
    banksy_id = blob.id.split("/")[-1]
    data = {
        "id": banksy_id,
        "banksy": True,
        "bucket": blob.bucket.name,
        "content_type": blob.content_type,
        "crc32c": blob.crc32c,
        "labels": incoming["labels"],
        "label_annotations": incoming["label_annotations"],
        "md5_hash": blob.md5_hash,
        "object_name": blob.name,
        "size": blob.size,
        "storage_class": blob.storage_class,
        "time_created": blob.time_created,
        "uri": f"gs://{blob.bucket.name}/{blob.name}",
    }
    client.collection("banksy").document(banksy_id).set(data)

    # delete the old image
    delete_object(bucket_name, object_name)

    # delete the old firestore record
    incoming_ref.delete()

    return redirect(f"/?start_after={blob_id}")


@app.route('/notbanksy/<blob_id>')
def notbanksy(blob_id):
    """Confirm an image as NOT Banksy."""
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
