# File Downloader

This application allows you to download files from a list of URLs specified in an Excel or CSV file.

## How to Use

1. Install the necessary dependencies using Poetry:

   ```shell
   poetry install
   ```
2. Run the application:

   ```shell
   poetry run python main.py
   ```

4. Select an Excel or CSV file containing the URLs for downloading and choose a folder to save the files.

5. Specify the column number containing the URLs and the number of parallel downloads.

6. Click the "Download" button to initiate the file downloads.

## Dependencies
- Python 3.11
- requests
- pandas
- tkinter
- tqdm
