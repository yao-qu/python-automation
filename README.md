# 1 Kindle clippings to CSV file
Recently started reading books on Kindle and wanted to review the highlights made, although Amazon provides a web service for viewing those highlights, they are only available for books bought from the Kindle Store. For highlights made on imported books, they are only stored on the device. This python script reads the `My Clipping.txt` file and convert it to a CSV for easy viewing.


`python3 KindleClipping.py --i "My Clippings.txt" --o "Output.csv" --e 0`

`--i` input txt filename, this is the Kindle Clippings txt file

`--o` output CSV filename

`--e` 0 if file already exists, add new highlights to the existing file, 1 to create a new CSV file

Tested on `My Clipping.txt` generated on PaperWhite 3 English version

Connect Kindle to computer and copy `My Clipping.txt` from `documents` under `Kindle`
