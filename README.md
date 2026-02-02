# Job XML Converter

A Flask web application that converts gzipped XML job feeds into Excel spreadsheets. Accepts both URL inputs and file uploads.

## Features

- **URL Input**: Fetch and convert `.xml.gz` files directly from URLs
- **File Upload**: Upload local `.xml.gz` files for conversion
- **Excel Output**: Clean, structured Excel files with all job data
- **Modern UI**: Responsive, gradient-styled interface
- **Fast Processing**: Efficient XML parsing and Excel generation

## Tech Stack

- **Backend**: Flask (Python)
- **Data Processing**: pandas, xml.etree.ElementTree
- **File Handling**: gzip, requests
- **Export Format**: Excel (.xlsx)

## Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd job-xml-converter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running Locally

Start the Flask development server:

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Using the Application

**Option 1: Convert from URL**
1. Paste the URL of a `.xml.gz` file
2. Click "Convert from URL"
3. Download the generated Excel file

**Option 2: Convert from Upload**
1. Click "Choose File" and select a local `.xml.gz` file
2. Click "Convert from File"
3. Download the generated Excel file

### Expected XML Structure

The application expects XML in the following format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jobs>
  <job>
    <title>Software Engineer</title>
    <company>Example Corp</company>
    <location>Remote</location>
    <description>Job description here</description>
    <!-- Additional fields -->
  </job>
  <!-- More jobs -->
</jobs>
```

All child elements within `<job>` tags will be extracted as columns in the Excel output.

## Deployment

### Environment Variables

- `PORT`: Server port (default: 5000)

### Heroku Deployment

1. Create a `Procfile`:
```
web: python app.py
```

2. Ensure `requirements.txt` is up to date

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Railway/Render Deployment

Both platforms auto-detect Flask apps. Ensure:
- `requirements.txt` is present
- Port is read from environment: `port = int(os.environ.get('PORT', 5000))`

## Dependencies

- Flask: Web framework
- pandas: Data manipulation and Excel export
- openpyxl: Excel file writing (pandas dependency)
- requests: HTTP requests for URL downloads

## Error Handling

The application handles:
- Invalid URLs (HTTP errors)
- Malformed XML files
- Empty job feeds
- File upload errors

## Development

### Adding Features

The application structure supports easy extensions:
- Modify `process_gz_content()` to change data processing logic
- Update HTML template for UI changes
- Add new routes for additional functionality

## Security Notes

- File uploads are processed in memory (no permanent storage)
- URL downloads use requests with default timeouts
- Consider adding file size limits for production use
- Implement rate limiting for public deployments

## License

MIT License

## Contributing

# Contributing to Job XML Converter

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

## Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Testing
Before submitting:
1. Test both URL and file upload functionality
2. Test with various XML structures
3. Verify Excel output quality
4. Check error handling with invalid inputs

## Pull Request Process
1. Update README.md if you've added features
2. Ensure all tests pass
3. Write a clear PR description explaining:
   - What changes you made
   - Why you made them
   - How to test them

## Areas for Contribution

### Potential Improvements
- Add unit tests
- Implement file size limits
- Add CSV export option
- Support additional XML schemas
- Improve error messages
- Add progress indicators for large files
- Implement batch processing
- Add data validation
- Create Docker container
- Add API documentation

### Bug Reports
When reporting bugs, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Sample XML file (if possible)
- Error messages
- Environment details (OS, Python version)

### Feature Requests
For feature requests, describe:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered
- How it benefits other users

## Questions?

Feel free to open an issue for questions or clarifications.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Keep discussions professional
