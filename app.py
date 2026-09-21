import os
import json
from dotenv import load_dotenv
from google import genai
from prompt import LINUX_LOG_ANALYZER_PROMPT
from schemas import LogAnalysis

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def main():
    #log = "Permission denied: cannot access /var/log/syslog"
    log = "Connection refused: database server 10.10.20.15:5432"
    prompt = LINUX_LOG_ANALYZER_PROMPT.format(log=log)
    #print(prompt)
    print("Sending request...")

    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        #input="Say hello in one word."
        input = prompt
    )
    
    print("Response received!")

    print(interaction.output_text)
    
    response_text = interaction.output_text
    
    response_data = json.loads(response_text)
    llm_response = LogAnalysis(**response_data)
    
    print ("Validated LLM Response:")
    print(llm_response)


if __name__ == "__main__":
    main()