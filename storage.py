from supabase import create_client, Client
import os
from dotenv import load_dotenv
from main_logging import logger

load_dotenv()
BUCKET_NAME = "bill-scraper"

url = os.getenv('SUPABASE_API_URL')
key = os.getenv('SUPABASE_ANON_KEY')

supabase: Client = create_client(url, key)
bucket_name: str = "bill-scraper"


def list_bucket_items():
    res = supabase.storage.from_(bucket_name).list()
    logger.info(f"Listing items in {bucket_name}:")
    for x in res:
        print(x)


def upload_to_bucket(folder, file):
    """
    Uploads an image file to bill-scraper bucket at Supabase. For use of generated screenshots during automation process
    :param folder: tnb or air
    :param file: Screenshot image file to be uploaded with relative directories
    """
    base_name = os.path.basename(file)
    extension = os.path.splitext(base_name)[1][1:]

    # for png files, upload to the e.g. tnb/file_name.png
    # for html files, upload to the e.g. html/tnb/file_name.html
    path = f"{folder}/{base_name}" if extension == "png" else f"html/{folder}/{base_name}"
    content_type = f"image/{extension}" if extension == "png" else f"text/{extension}"
    res = supabase.storage.from_(bucket_name).upload(
        path=path,
        file=file,
        file_options={"content-type": content_type}
    )
    logger.info(f"Status of file upload: {res}")
    # print("Skipping saving screenshot to supabase")

# upload_to_bucket("screenshots/air/air-20230703-225055.png")
# # upload_to_bucket("QR_CODE.jpeg")
# list_bucket_items()
