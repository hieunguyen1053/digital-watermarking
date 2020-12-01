# digital_watermarking
Implementation of algorithms DCT, DWT watermarking.

### Install all dependencies:

`pip install -r requirements.txt`

### 1. Embedding watermark into a cover:

`python main.py --origin path_cover_image --ouput path_output_image`

Example:

> `python main.py --origin cover.jpg --ouput watermarked.jpg`
> 1. Then choice a type from "DCT" or "DWT".
> 2. After that, choice "embedding".

### 2. Extracting watermark from a watermarked image:

`python main.py --origin path_watermarked_image --ouput path_extracted_signature`

Example:

> `python main.py --origin watermarked.jpg --ouput signature.jpg`
> 1. Then choice a type from "DCT" or "DWT".
> 2. After that, choice "extracting".

### 3. Attacking a watermarked image:

`python main.py --origin path_watermarked_image --ouput path_attacked_image`

Example:

> `python main.py --origin watermarked.jpg --ouput watermarked.jpg`
> 1. Then choice "Attack".
> 2. After that, choice a type attack.
