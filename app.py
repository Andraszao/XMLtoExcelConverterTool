"""Job XML Converter - Flask web app for converting gzipped XML to Excel.

This application provides two conversion methods:
1. URL input: Fetch and convert remote .xml.gz files
2. File upload: Convert local .xml.gz files

Author: James (Inchworm Games)
License: MIT
"""

from flask import Flask, request, send_file, render_template_string
import gzip
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import os
from io import BytesIO

app = Flask(__name__)

# HTML template with embedded CSS for main interface
# Provides gradient UI with dual input methods: URL and file upload
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Job XML Converter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
                         Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 16px;
            padding: 48px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        h1 {
            font-size: 28px;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 8px;
            text-align: center;
        }

        .subtitle {
            color: #718096;
            text-align: center;
            margin-bottom: 40px;
            font-size: 15px;
        }

        .form-section {
            margin-bottom: 32px;
        }

        label {
            display: block;
            font-weight: 500;
            color: #4a5568;
            margin-bottom: 8px;
            font-size: 14px;
        }

        input[type="text"], input[type="file"] {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 15px;
            transition: all 0.2s;
            background: #f7fafc;
        }

        input[type="text"]:focus, input[type="file"]:focus {
            outline: none;
            border-color: #667eea;
            background: white;
        }

        input[type="text"]::placeholder {
            color: #a0aec0;
        }

        button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 14px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 12px;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        .divider {
            text-align: center;
            margin: 32px 0;
            position: relative;
            color: #a0aec0;
            font-size: 14px;
        }

        .divider::before,
        .divider::after {
            content: '';
            position: absolute;
            top: 50%;
            width: 40%;
            height: 1px;
            background: #e2e8f0;
        }

        .divider::before {
            left: 0;
        }

        .divider::after {
            right: 0;
        }

        .file-input-wrapper {
            position: relative;
        }

        input[type="file"] {
            cursor: pointer;
        }

        input[type="file"]::file-selector-button {
            background: #edf2f7;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            margin-right: 12px;
            cursor: pointer;
            font-weight: 500;
            color: #4a5568;
        }

        input[type="file"]::file-selector-button:hover {
            background: #e2e8f0;
        }

        @media (max-width: 600px) {
            .container {
                padding: 32px 24px;
            }

            h1 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Job XML Converter</h1>
        <p class="subtitle">Transform your job XML files into clean Excel spreadsheets</p>

        <form method="POST" action="/convert-url" class="form-section">
            <label>Paste URL to .gz file</label>
            <input type="text" name="url" placeholder="https://example.com/jobs.xml.gz" required>
            <button type="submit">Convert from URL</button>
        </form>

        <div class="divider">or</div>

        <form method="POST" action="/convert-file"
              enctype="multipart/form-data" class="form-section">
            <label>Upload .gz file</label>
            <div class="file-input-wrapper">
                <input type="file" name="file" accept=".gz" required>
            </div>
            <button type="submit">Convert from File</button>
        </form>
    </div>
</body>
</html>
'''


def process_gz_content(gz_data):
    """Process gzipped XML content and generate Excel file.

    Args:
        gz_data (bytes): Gzipped XML content

    Returns:
        tuple: (output_filepath: str, job_count: int)

    Raises:
        gzip.BadGzipFile: If gz_data is not valid gzip
        ET.ParseError: If XML is malformed
    """
    # Decompress gzip to XML string
    with gzip.open(BytesIO(gz_data), 'rt', encoding='utf-8') as f:
        xml_content = f.read()

    # Parse XML and extract job data
    root = ET.fromstring(xml_content)
    jobs = []
    for job in root.findall('.//job'):  # Find all <job> elements recursively
        # Convert each child element to dict entry (tag: text)
        job_data = {child.tag: child.text for child in job}
        jobs.append(job_data)

    # Convert to DataFrame and export to Excel
    df = pd.DataFrame(jobs)
    output_file = 'jobs_output.xlsx'
    df.to_excel(output_file, index=False)  # No row indices

    return output_file, len(jobs)


@app.route('/')
def home():
    """Render main application interface.

    Returns:
        str: Rendered HTML template
    """
    return render_template_string(HTML)


@app.route('/convert-url', methods=['POST'])
def convert_url():
    """Download and convert XML.gz file from URL.

    Form Data:
        url (str): URL to .xml.gz file

    Returns:
        File: Excel file download (jobs.xlsx)

    Raises:
        requests.RequestException: If URL fetch fails
        Various: From process_gz_content (gzip, XML, pandas errors)
    """
    url = request.form['url']

    # Fetch remote file
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for 4xx/5xx status

    # Process and generate Excel
    output_file, job_count = process_gz_content(response.content)

    print(f"Converted {job_count} jobs from URL")
    return send_file(
        output_file,
        as_attachment=True,
        download_name='jobs.xlsx')


@app.route('/convert-file', methods=['POST'])
def convert_file():
    """Convert uploaded XML.gz file to Excel.

    Form Data:
        file (FileStorage): Uploaded .xml.gz file

    Returns:
        File: Excel file download (jobs.xlsx)

    Raises:
        Various: From process_gz_content (gzip, XML, pandas errors)
    """
    file = request.files['file']

    # Read uploaded file into memory
    gz_data = file.read()

    # Process and generate Excel
    output_file, job_count = process_gz_content(gz_data)

    print(f"Converted {job_count} jobs from upload")
    return send_file(
        output_file,
        as_attachment=True,
        download_name='jobs.xlsx')


if __name__ == '__main__':
    # Read port from environment (Heroku, Railway, etc.) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Bind to all interfaces for container/cloud deployment
    app.run(host='0.0.0.0', port=port)
