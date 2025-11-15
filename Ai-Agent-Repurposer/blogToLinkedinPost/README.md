Blog Content Summarizer and Social Media Post Generator
📄 Project Description
This Python script is designed to automate the process of turning long-form blog content into concise, actionable summaries suitable for social media platforms like LinkedIn. It leverages web scraping to extract text from any provided URL and utilizes the Gemini API (via the google-genai library) for advanced natural language processing tasks, such as summarization and creative text generation.
✨ Features
Web Scraping: Fetches and extracts clean text content from a specified blog URL.
Gemini API Integration: Uses the Google Gemini model for sophisticated summarization and post generation.
Environment Variable Security: Securely manages the API key using the .env file for development environments.Interactive Command Line: Prompts the user for the blog URL directly in the console.

🛠️ Prerequisites
Before you begin, ensure you have the following installed:
Python 3.8+
A Gemini API Key.
 You can obtain one from Google AI Studio.
 
 📦 Setup and InstallationFollow these steps to set up the project environment:
 1. Clone the Repository (or setup the files)Ensure your main.py script and the new .env file are in the same folder.2. Install Required Python LibrariesThis project uses google-genai for the AI calls, requests for fetching the content, and python-dotenv for reading environment variables.pip install google-genai requests beautifulsoup4 python-dotenv
 3. Configure Your API Key (Crucial Step)The script is designed to securely load your API key from an environment file, which is the standard practice for development.Create a file named .env in the root directory of your project (next to main.py).Add your Gemini API key to this file in the following format:GEMINI_API_KEY="YOUR_API_KEY_HERE"
 (Replace YOUR_API_KEY_HERE with your actual key.)4. Update main.py to Load the .env FileTo make sure your script  recognizes the .env file, include the following lines at the very top of your main.py:# main.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Rest of your imports and code follow...
from google import genai
# ... etc.
🚀 UsageExecute the script from your terminal:python main.py
The script will prompt you for the URL:Please enter the blog link (URL) you want to summarize: 

Enter the full URL (e.g., https://www.onsaas.me/blog/b2b-growth-strategies) and press Enter.The output will first show the content being scraped, followed by the Gemini-generated summary and social media post.💡 Output ExampleThis is an example of the structured output you can expect after running the script:------------------------------
Fetching content from: [https://www.onsaas.me/blog/b2b-growth-strategies](https://www.onsaas.me/blog/b2b-growth-strategies)
Successfully scraped content (First 300 characters):
'Software ReviewsBlog ...'
------------------------------
🚀 Gemini AI Generated Content 🚀

--- SUMMARY (for internal use) ---

The blog post outlines 12 practical B2B growth strategies, focusing on modern approaches like ICP refinement, content marketing that drives revenue, optimizing the sales-marketing handoff, and leveraging customer success as a growth engine.

--- LINKEDIN POST (Ready to share) ---

12 B2B Growth Strategies for 2025: Stop guessing and start driving real revenue! 📈

We just broke down the core strategies that are separating the market leaders from the laggards this year, including:
1. Refining your ICP (stop selling to everyone).
2. Turning Customer Success into a repeatable sales channel.
3. Optimizing the crucial handoff between Sales and Marketing.

Read the full deep dive here: [LINK_URL]

#B2BMarketing #SaaSGrowth #SalesStrategy #GeminiAI
------------------------------
🚧 Challenges FacedThis section documents the primary technical challenge encountered during initial setup, providing clarity for future users.Initial API Key Authentication IssueThe primary challenge encountered during initial setup was the failure of the script to automatically load the GEMINI_API_KEY from the local .env file.Problem: Standard Python environment execution (e.g., python main.py) does not automatically read variables from a .env file.Initial Temporary Fix: The key was successfully set directly via the PowerShell command line ($env:GEMINI_API_KEY="...") for single-session use.Permanent Solution: To ensure reliable and portable API key management, the python-dotenv library was introduced. Adding from dotenv import load_dotenv; load_dotenv() at the start of main.py explicitly loads the variables, resolving the authentication failure permanently.📁 Project Structure/
├── main.py             # The main script containing the scraping and AI logic.
├── .env                # File containing the secret GEMINI_API_KEY (DO NOT commit this file).
└── README.md           # This documentation file.
