# 🤖 AI Content Summarizer

A Flask web application that uses Google's Gemini AI to generate intelligent summaries from text input or web URLs.

## ✨ Features

- **Text Summarization**: Input any text and get an AI-generated summary
- **URL Processing**: Paste any URL and get a summary of the webpage content
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Error Handling**: Robust error handling for API failures and invalid URLs
- **Mobile Friendly**: Fully responsive design that works on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Google Gemini API key (free tier available)

### Installation

#### Option 1: Using pip (Traditional)

1. **Clone or navigate to the project directory**
   ```bash
   cd week3/flask_aws_gemini
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

#### Option 2: Using uv (Modern, Fast)

1. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone or navigate to the project directory**
   ```bash
   cd week3/flask_aws_gemini
   ```

3. **Install dependencies** (uv will automatically create a virtual environment)
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   SECRET_KEY=your-secret-key-for-flask
   FLASK_ENV=development
   ```

   ⚠️ **Important**: The `GEMINI_API_KEY` is **required** - the application will not start without it.

5. **Run the application**
   
   **Using pip/traditional setup:**
   ```bash
   python main.py
   ```
   
   **Using uv:**
   ```bash
   uv run python main.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Required |
| `SECRET_KEY` | Flask secret key for sessions | `your-secret-key-here` |
| `FLASK_ENV` | Flask environment | `development` |

## 📡 API Endpoints

### `GET /`
- **Description**: Serves the main application page
- **Response**: HTML page with the summarization interface

### `POST /summarize`
- **Description**: Processes text or URL for summarization
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "content": "Your text or URL here"
  }
  ```
- **Response**:
  ```json
  {
    "summary": "Generated summary...",
    "source_type": "Text|URL",
    "source": "Original content or URL"
  }
  ```

### `GET /health`
- **Description**: Health check endpoint for deployment monitoring
- **Response**: `{"status": "healthy"}`

## 🏗️ Project Structure

```
flask_aws_gemini/
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies (pip)
├── pyproject.toml      # Project configuration (uv)
├── uv.lock             # Locked dependency versions (uv)
├── templates/
│   └── index.html      # Main web interface
└── README.md           # This file
```

## 🌐 Deployment to AWS EC2

### 1. Prepare Your EC2 Instance

```bash
# Update system
sudo yum update -y

# Install Python 3.9+
sudo yum install python3 python3-pip -y

# Install Git
sudo yum install git -y
```

### 2. Clone and Setup Application

```bash
# Clone your repository
git clone <your-repo-url>
cd flask_aws_gemini

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Set up environment variables (create .env file or export)
echo "GEMINI_API_KEY=your_actual_api_key" > .env
echo "SECRET_KEY=your_production_secret_key" >> .env
echo "FLASK_ENV=production" >> .env

# OR export directly:
# export GEMINI_API_KEY="your_actual_api_key"
# export SECRET_KEY="your_production_secret_key"
# export FLASK_ENV="production"
```

### 3. Run with Gunicorn (Production)

```bash
# Install Gunicorn
pip3 install gunicorn

# Run the application
gunicorn --bind 0.0.0.0:5000 main:app
```

### 4. Set up as a Service (Optional)

Create `/etc/systemd/system/flask-summarizer.service`:

```ini
[Unit]
Description=Flask Summarizer App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/flask_aws_gemini
Environment=GEMINI_API_KEY=your_api_key
Environment=SECRET_KEY=your_secret_key
Environment=FLASK_ENV=production
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-summarizer
sudo systemctl start flask-summarizer
```

### 5. Configure Security Group

- Open port 5000 in your EC2 security group
- For production, consider using a reverse proxy (nginx) and SSL

## 🔒 Security Considerations

- **API Keys**: Never commit API keys to version control. Use `.env` files and add `.env` to `.gitignore`
- **Environment Variables**: The application will fail to start if `GEMINI_API_KEY` is not provided
- **HTTPS**: Use HTTPS in production
- **Rate Limiting**: Consider implementing rate limiting for API endpoints
- **Input Validation**: The app includes basic input validation and sanitization
- **Content Length**: URL content is limited to 5000 characters for performance
- **Virtual Environment**: Always use a virtual environment to isolate dependencies

## 🐛 Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY environment variable is required" Error**
   - Ensure you have created a `.env` file with your API key
   - Verify the `.env` file is in the same directory as `main.py`
   - Check that your API key is valid and active

2. **"Invalid API Key" Error**
   - Verify your Gemini API key is correct
   - Check that the API key has the necessary permissions
   - Ensure the API key is not expired

3. **URL Processing Fails**
   - Some websites block automated requests
   - Check if the URL is accessible
   - Verify the website allows scraping

4. **Module Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

5. **Port Already in Use**
   - Change the port in `main.py`: `app.run(port=5001)`
   - Or kill the process using the port

## 📝 Usage Examples

### Text Summarization
```
Input: "Artificial intelligence has been making significant strides in recent years. Machine learning algorithms are becoming more sophisticated, enabling computers to perform tasks that traditionally required human intelligence. These advances are transforming industries from healthcare to finance, creating new opportunities while also raising important ethical considerations about the future of work and society."

Output: "The text discusses recent advances in artificial intelligence and machine learning, highlighting their growing sophistication and transformative impact across industries like healthcare and finance. It also notes the emergence of both new opportunities and ethical concerns regarding employment and societal implications."
```

### URL Summarization
```
Input: "https://example.com/long-article"
Output: Summary of the article content from the webpage

Note: The application extracts text content from the webpage and generates a comprehensive summary focusing on main points and key insights.
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- [Google Gemini AI](https://ai.google.dev/) - AI model documentation
- [Google AI Studio](https://aistudio.google.com/app/apikey) - Get your API key
- [Flask Documentation](https://flask.palletsprojects.com/) - Web framework
- [uv Documentation](https://docs.astral.sh/uv/) - Modern Python package manager
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/) - Cloud deployment
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web scraping library
