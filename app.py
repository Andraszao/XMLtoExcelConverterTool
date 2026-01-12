# app.py
from flask import Flask, request, send_file, render_template_string
import gzip
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import os
from io import BytesIO

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Job XML Converter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        input[type="text"], input[type="file"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            box-sizing: border-box;
        }
        button {
            background: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        .divider {
            text-align: center;
            margin: 20px 0;
            color: #999;
        }
    </style>
</head>
<body>
    <h1>Convert Job XML to Excel</h1>
    
    <form method="POST" action="/convert-url">
        <label>Paste URL to .gz file:</label>
        <input type="text" name="url" placeholder="https://example.com/jobs.xml.gz" required>
        <button type="submit">Convert from URL</button>
    </form>
    
    <div class="divider">— OR —</div>
    
    <form method="POST" action="/convert-file" enctype="multipart/form-data">
        <label>Upload .gz file:</label>
        <input type="file" name="file" accept=".gz" required>
        <button type="submit">Convert from File</button>
    </form>
</body>
</html>
'''

def process_gz_content(gz_data):
    """Process gzipped XML content and return Excel file"""
    # Decompress
    with gzip.open(BytesIO(gz_data), 'rt', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Parse XML
    root = ET.fromstring(xml_content)
    jobs = []
    for job in root.findall('.//job'):
        job_data = {child.tag: child.text for child in job}
        jobs.append(job_data)
    
    # Create Excel
    df = pd.DataFrame(jobs)
    output_file = 'jobs_output.xlsx'
    df.to_excel(output_file, index=False)
    
    return output_file, len(jobs)

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/convert-url', methods=['POST'])
def convert_url():
    url = request.form['url']
    
    # Download the file
    response = requests.get(url)
    response.raise_for_status()
    
    # Process it
    output_file, job_count = process_gz_content(response.content)
    
    print(f"Converted {job_count} jobs from URL")
    return send_file(output_file, as_attachment=True, download_name='jobs.xlsx')

@app.route('/convert-file', methods=['POST'])
def convert_file():
    file = request.files['file']
    
    # Read file content
    gz_data = file.read()
    
    # Process it
    output_file, job_count = process_gz_content(gz_data)
    
    print(f"Converted {job_count} jobs from upload")
    return send_file(output_file, as_attachment=True, download_name='jobs.xlsx')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))