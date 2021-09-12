"""Banksy app."""
from datetime import timedelta
from flask import Flask
from flask import render_template
from flask import request
from google.cloud import firestore
from google.cloud import storage

app = Flask(__name__)


def get_next_image(start_after=None, start_before=None):
    """Return the next image from Firestore."""
    client = firestore.Client()
    collection = "images"
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
    image = get_next_image(
        start_after=start_after,
        start_before=start_before,
    )
    if not image:
        image = get_next_image()
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
