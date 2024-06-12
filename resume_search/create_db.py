import os

import parse_generic 
import parse_static

from openai.lib.azure import AzureOpenAI

def read_resumes():
    pass

def save_to_elastic():
    pass

if __name__ == "__main__":
    resumes = read_resumes()
    parsed_resumes_generic = parse_generic.parse_resume_with_llm()
    parsed_resumes_static = parse_static.parse_resume_with_llm()

    save_to_elastic(parsed_resumes_generic)
    save_to_elastic(parsed_resumes_static)
