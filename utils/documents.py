from pathlib import Path

job_ads_directory = Path("./job_ads/")
cvs_directory = Path("./cvs/")

job_ad_files = sorted(list(job_ads_directory.glob("*.txt")))
cv_files = sorted(list(cvs_directory.glob("*.txt")))

job_ad_texts = []
cv_texts = []


for file_name in job_ad_files:
    try:
        with open(file_name) as file_handler:
            job_ad_text = file_handler.read()
            job_ad_texts.append(job_ad_text)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} not found. Please check the path.")

for file_name in cv_files:
    try:
        with open(file_name) as file_handler:
            cv_text = file_handler.read()
            cv_texts.append(cv_text)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} not found. Please check the path.")
