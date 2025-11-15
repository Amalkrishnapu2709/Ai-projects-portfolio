
import os
import sys
import requests
import datetime
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv() 

#  Set the default output folder name
OUTPUT_FOLDER = "output_summaries"
API_MODEL = "gemini-2.5-flash-preview-09-2025"

# Placeholder for the API Key check (required for the code structure)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("FATAL ERROR: GEMINI_API_KEY environment variable not found.")
    print("Please set it in your .env file or your environment.")
    sys.exit(1)



def get_safe_filename(url):
    """Generates a safe filename based on the URL path and current timestamp."""
    
    # 1. Parse the URL to get the clean path segment
    parsed_url = urlparse(url)
    # Get the last segment of the path (e.g., 'b2b-growth-strategies')
    path_segment = parsed_url.path.strip('/').split('/')[-1]
    
    if not path_segment:
        path_segment = 'summary'

    # 2. Sanitize the segment to be file-system friendly
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', path_segment)
    
    # 3. Prepend a timestamp for uniqueness
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"{timestamp}_{safe_name}.txt"


def scrape_blog_content(url):
    """
    Fetches and cleans content from a given URL, using a robust User-Agent header.
    (Integrated from your previous script)
    """
    try:
        # Use a User-Agent header to mimic a browser, avoiding common blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Fetching content from: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements (scripts, styles, nav, header, footer)
        for element in soup(["script", "style", "nav", "header", "footer"]):
            element.decompose()
        
        # Get all visible text from the body
        raw_text = soup.body.get_text()
        
        # Clean up multiple newlines and spaces, ensuring text is scannable
        clean_text = re.sub(r'\n\s*\n', '\n\n', raw_text.strip())
        
        return clean_text
        
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during scraping: {e}")
        return None

def generate_linkedin_post(content, blog_url):
    """
    Calls the Gemini API to generate the professional LinkedIn post 
    using the detailed copywriter prompt from your previous script.
    """
    
    # Detailed LinkedIn Copywriter Prompt (Integrated from your previous script)
    user_query = f"""
You are an expert LinkedIn copywriter specializing in B2B tech and professional content.
Your task is to transform the provided blog post content into a single, highly engaging LinkedIn post.

Your post must adhere to the following rules:
1.  **Structure:** The post must have a strong Hook, 3-5 key takeaways, and a clear Call-to-Action (CTA).
2.  **Format:** Use professional, conversational language. Incorporate line breaks (double newlines) and relevant emojis (like 💡, ✅, 🚀, or a bullet point emoji) to make it highly scannable.
3.  **Length:** Keep the post concise, aiming for a length that is engaging without being overly long (ideally no more than 15-20 lines total).
4.  **Hashtags:** Include 4-6 highly relevant, specific hashtags at the end.
5.  **CTA:** Ensure the Call-to-Action specifically uses the provided blog URL.
6.  **Output:** Return ONLY the text of the LinkedIn post. Do not include any introduction, conclusion, or commentary.

---

**BLOG POST CONTENT:**

{content}

---

**Generated LinkedIn Post (CTA URL: {blog_url}):**
"""
    
    # Use the local API key for the fetch call
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/{API_MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        # No separate system instruction needed, as the user_query is highly detailed
    }
    
    print("Sending content to Gemini for LinkedIn post generation...")

    try:
        response = requests.post(apiUrl, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        
        result = response.json()
        
        # Extract the generated text
        text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Generation Failed.')
        return text

    except requests.RequestException as e:
        print(f"Gemini API Request Error: {e}")
        return "Failed to communicate with the Gemini API."
    except Exception as e:
        print(f"An error occurred while processing the API response: {e}")
        return "Failed to parse API response."


def main():
    """Main function to orchestrate the scraping, generation, and saving."""
    
    blog_url = input("Please enter the blog link (URL) you want to summarize: ")
    print("-" * 30)
    
    # 1. Scrape Content
    scraped_content = scrape_blog_content(blog_url)
    
    if not scraped_content:
        print("Scraping failed or no content found. Exiting.")
        return

    # Print a preview of the scraped content
    print(f"Successfully scraped content (First 300 characters):\n'{scraped_content[:300].strip().replace('\n', ' ')}...'")
    print("-" * 30)

    # 2. Generate Post (Function renamed to reflect single output)
    generated_text = generate_linkedin_post(scraped_content, blog_url)
    
    # Format the final output string
    final_output = f"""
--- START GENERATED CONTENT ---
Blog URL: {blog_url}
Generation Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{generated_text}

--- END GENERATED CONTENT ---
"""
    
    # 3. Save Output to File
    try:
        # Create folder if it doesn't exist
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        
        # Determine the file path
        filename = get_safe_filename(blog_url)
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        
        # Write the content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_output)

        # 4. Success message
        print("\n" + "=" * 50)
        print("🚀 GENERATED LINKEDIN POST 🚀")
        print("=" * 50)
        
        # Display the core generated text in the console
        print(generated_text.strip())
        
        print("\n" + "=" * 50)
        print(f"✅ Full output saved to: {filepath}")
        print(f"Folder created/used: {os.path.abspath(OUTPUT_FOLDER)}")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nFATAL ERROR: Could not save file to disk. {e}")
        
if __name__ == "__main__":
    main()
