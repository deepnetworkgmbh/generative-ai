import os
import json
import csv
import glob
from openai import AzureOpenAI
from pypdf import PdfReader


parameters_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": 'The name of the applicant. If no name is provided, return "not_stated".',
        },
        "education": {
            "type": "array",
            "description": 'The education institutes applicant has attended. If no education information is provided, return [].',
            "items": {
                "type": "string"
            }
        },
        "work_experience": {
            "type": "array",
            "description": 'The past work experience of the applicant. If no work experience information is provided, return [].',
            "items": {
                "type": "string"
            }
        },
    },
    "required": ["name", "education", "work_experience"],
}
function_schema = {
    "name": "structure_resume",
    "description": "Creates a structured object from an applicant's resume",
    "parameters": parameters_schema,
}
system_message = (
    "You are an assistant that parses the resumes of applicants."
)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-09-01-preview"
)


parsed_resumes = {}
os.chdir("./resume_parser/resume-pdf")
for resume in glob.glob("*.pdf"):
    reader = PdfReader(resume)
    buffer = "Resume: "
    for page in reader.pages:
        buffer += page.extract_text() + "\n"
    
    response = client.chat.completions.create(
        model="test-deployment",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": buffer},
        ],
        functions=[function_schema],
        function_call={"name": function_schema["name"]},
    )
    args = json.loads(response.choices[0].message.function_call.arguments)
    parsed_resumes[args["name"]+"-resume"] = args
    
os.chdir("..")
with open('output.json', 'w') as file:
    json.dump(parsed_resumes, file)
"""
with open('output.csv', 'w') as output_file:
    csv_writer = csv.writer(output_file)
    first = True
    for resume in parsed_resumes:
        if first:
            header = resume.keys()
            csv_writer.writerow(header)
            first = False

        csv_writer.writerow(resume.values())
"""