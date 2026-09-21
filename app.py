import os
import json
from dotenv import load_dotenv
from google import genai
from prompt import LINUX_LOG_ANALYZER_PROMPT
from schemas import LogAnalysis
from pydantic import ValidationError
from google.genai.errors import APIError

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

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


def main():
    #log = "Permission denied: cannot access /var/log/syslog"
    #log = "Connection refused: database server 10.10.20.15:5432"
    log = read_log_file("sample.log")
    if log is None:
        print("Log analysis cancelled.")
        exit()
    prompt = LINUX_LOG_ANALYZER_PROMPT.format(log=log)
    #print(prompt)
    print("Sending request...")
    
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

    
        print("Response received!")

        print(interaction.output_text)
        
        response_text = interaction.output_text
        
        llm_response = LogAnalysis.model_validate_json(response_text)
        
        print("\nValidated Log Analysis:")
        print("Root Cause:", llm_response.root_cause)
        print("Category:", llm_response.category.value)
        print("Confidence:", llm_response.confidence_level.value)
        print("Evidence:", llm_response.evidence)
        
    except APIError as error:
        print("API Error:", error)
    except json.JSONDecodeError as error:
        print("Invalid JSON Error:", error)
    except ValidationError as error:
        print("LLMValidation Error:", error)
    except Exception as error:
        print("An unexpected error occurred:", error)

if __name__ == "__main__":
    main()