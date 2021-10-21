This demo uses the request/reply pattern.

The C++ program receives image paths from the Python program, read barcodes with [Dynamsoft Barcode Reader](https://www.dynamsoft.com/barcode-reader/overview/) and sends the decoding results back to the Python program.

The C++ program's code is in [this repo](https://github.com/xulihang/BarcodeReader_CommandLine/tree/main/DBR) while the Python program's is the `decode.py` file.