import os
import subprocess
import logging
from google.cloud import storage

TMP_FOLDER = '/tmp'
OUTPUT_BUCKET = os.environ['GCS_OUTPUT_BUCKET']


def main(data, context=None):
    gcs = storage.Client(project=os.environ['GCP_PROJECT'])
    bucket_name = data['bucket']
    file_name = data['name']
    if file_name[-4:] != '.pdf':
        logging.error("input file is not pdf")
        return
    input_filepath = os.path.join(TMP_FOLDER, file_name)
    bucket = gcs.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(input_filepath)

    output_filename = file_name.rsplit('.', 1)[0]
    output_filename += '-%d'
    output_filename += '.png'
    output_filepath = os.path.join(TMP_FOLDER, output_filename)

    cmd = f'gs -dSAFER -dNOPAUSE -dBATCH -sDEVICE=png16m -r600 -sOutputFile="{output_filepath}" {input_filepath}'.split(
        ' ')
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    stdout, stderr = p.communicate()
    error = stderr.decode('utf8')
    if error:
        logging.error(error)
        return

    for filename in os.listdir(TMP_FOLDER):
        if filename[-4:] == '.png':
            full_path = os.path.join(TMP_FOLDER, filename)
            output_bucket = gcs.bucket(OUTPUT_BUCKET)
            output_blob = output_bucket.blob(filename)
            output_blob.upload_from_filename(full_path)
            logging.info(f'uploaded file: {filename}')
            os.remove(full_path)

    if os.path.exists(input_filepath):
        os.remove(input_filepath)
    return


if __name__ == '__main__':
    data = {
        'bucket': '',
        'name': ''
    }
    main(data)
