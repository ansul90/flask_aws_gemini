import os
import re
import requests
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")
genai.configure(api_key=GEMINI_API_KEY)

def is_valid_url(url):
    """Check if the provided string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_text_from_url(url):
    """Extract text content from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:5000]  # Limit to first 5000 characters
    
    except Exception as e:
        raise Exception(f"Error extracting text from URL: {str(e)}")

def generate_summary_with_gemini(content, content_type="text"):
    """Generate summary using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if content_type == "url":
            prompt = f"Please provide a comprehensive summary of the following web content. Focus on the main points, key insights, and important information:\n\n{content}"
        else:
            prompt = f"Please provide a clear and concise summary of the following text. Extract the main points and key information:\n\n{content}"
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        raise Exception(f"Error generating summary with Gemini: {str(e)}")

@app.route('/')
def index():
    """Home page with input form"""
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """Handle summarization request"""
    try:
        input_content = request.json.get('content', '').strip()
        
        if not input_content:
            return jsonify({'error': 'Please provide some content to summarize'}), 400
        
        # Check if input is a URL or text
        if is_valid_url(input_content):
            # Extract text from URL
            try:
                extracted_text = extract_text_from_url(input_content)
                summary = generate_summary_with_gemini(extracted_text, "url")
                return jsonify({
                    'summary': summary,
                    'source_type': 'URL',
                    'source': input_content
                })
            except Exception as e:
                return jsonify({'error': f'Failed to process URL: {str(e)}'}), 400
        else:
            # Process as text
            summary = generate_summary_with_gemini(input_content, "text")
            return jsonify({
                'summary': summary,
                'source_type': 'Text',
                'source': input_content[:100] + '...' if len(input_content) > 100 else input_content
            })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for AWS deployment"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
