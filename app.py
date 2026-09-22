import os
import json
from dotenv import load_dotenv
from google import genai
from prompt import LINUX_LOG_ANALYZER_PROMPT
from schemas import LogAnalysis
from pydantic import ValidationError
from google.genai.errors import APIError
from pathlib import Path
from collections import deque

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
""""
def read_log_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if not content.strip():
            raise ValueError("Log file is empty.")
        return content
    
    except (FileNotFoundError, PermissionError, OSError, ValueError) as e:
        print(f"Error reading log file: {e}")
        return None
        """

def read_last_n_lines(file_path, max_lines=500):
    log_path = Path(file_path)
    if max_lines <= 0:
        raise ValueError("max_lines must be a positive integer.")
    
    if not log_path.is_file():
        raise FileNotFoundError(f"Error: The provided path is not a file.")
    
    if not log_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        with log_path.open('r',encoding='utf-8',errors="replace") as file:
            lines = deque(file, maxlen=max_lines)
            content = ''.join(lines)
            if not content.strip():
                raise ValueError("Log file is empty.")
                return None
            return content
    except (PermissionError, OSError, ValueError) as e:
        print(f"Error reading log file: {e}")
        return None
    
def analyze_log(log_content):

    prompt = LINUX_LOG_ANALYZER_PROMPT.format(
        log=log_content
    )

    try:
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": LogAnalysis.model_json_schema()
            }
        )

        # Extract Gemini's JSON response
        output_text = interaction.output_text

        if not output_text:
            print("Error: Gemini returned an empty response.")
            return None

        # Validate JSON against our Pydantic model
        result = LogAnalysis.model_validate_json(output_text)

        return result

    except APIError as error:
        print(f"Gemini API error: {error}")
        return None

    except ValidationError as error:
        print(f"Response validation failed: {error}")
        return None

def main():
    file_path = input("Enter the path to the log file: ").strip()
    
    if not file_path:
        print("Error: File path cannot be empty.")
        return
    
    log_content = read_last_n_lines(file_path, max_lines=500)
    if log_content is None:
        print("Log analysis cancelled..")
        return
    print("\nLog file loaded successfully.")
    print("Sending logs to Gemini for analysis...\n")
    
    llm_response = analyze_log(log_content)
    
        
    print("\nValidated Log Analysis:")
    print("Root Cause:", llm_response.root_cause)
    print("Category:", llm_response.category.value)
    print("Confidence:", llm_response.confidence_level.value)
    print("Evidence:", llm_response.evidence)
        
    

if __name__ == "__main__":
    main()