import boto3
import pdfplumber
import os

#AWS S3 details 
bucket_name = "mypdfdocument"
pdf_file = "coffee.pdf"
txt_location = "./text.txt"

session = boto3.Session(profile_name='default')
s3 = session.client("s3")

s3.download_file(bucket_name, pdf_file, "temp.pdf")

# Extract text from the PDF and save it as a TXT file
with pdfplumber.open("temp.pdf") as pdf:
    with open(txt_location, 'w', encoding='utf-8') as txt_file:
        for page in pdf.pages:
            txt_file.write(page.extract_text() + '\n')

os.remove("temp.pdf")

print("Text has been extracted and saved successfully")


