This demo uses the push/pull pattern to read barcodes from images.

How to use:

1. Start consumers. You can start a consumer on an Android device with the Android app or on a PC device by running the `consumer.py` file.
2. Start the server. It will start a result collector at startup.
3. Visit <http://127.0.0.1:5111/>. Choose a folder where barcode images exist, create a session and start it. It will start a producer to dispatch decoding tasks to idle consumers.

