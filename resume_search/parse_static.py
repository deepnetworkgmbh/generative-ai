import os

from openai import AzureOpenAI
from openai import OpenAI

SYSTEM_MESSAGE = """
Your task is to create sql code at the end.
Use the given skills list and the given job description. 
Omit any comments or additional text.
Assign scores between 0-10 to each skill in the list based on its importance for the job description. 
If skill does not exist in the job description assign 0. 
Act as skills are column names and the scores are minimum thresholds and create a sql select query that lists the id column. 
Do not include skills with 0 points in the query. 
Use "AND" instead of "+". 
"""

SKILLS = """
python
java
cpp
javascript
html_css
ruby
php
csharp
swift
go
kotlin
typescript
rust
scala
r
matlab
bash_shell_scripting
git_github
docker
kubernetes
aws_amazon_web_services
azure
google_cloud_platform_gcp
terraform
ansible
jenkins
ci_cd
agile_scrum_methodologies
tdd
bdd
unit_testing
integration_testing
automation_testing
microservices_architecture
restful_apis
graphql
soap
json
xml
nosql_databases
relational_databases
data_structures_and_algorithms
object_oriented_programming_oop
functional_programming
devops
network_security
cloud_computing
software_design_patterns
systems_design
"""


def ask_gpt(messages):
    openai_client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2023-12-01-preview",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    response = openai_client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
        messages=messages
    )
    result = response.choices[0].message.content

    print(result)

    return result

def parse_resume_with_llm():
    pass

def create_query(job_description):
    test = """
Senior Java Full Stack Developer

We are looking for a highly experienced and motivated Senior Java Full Stack Developer to join our dynamic team. The ideal candidate will have extensive experience in developing and maintaining high-quality web applications using Java/J2EE technologies, front-end frameworks, and cloud platforms. The candidate will be responsible for designing, developing, and implementing robust, scalable, and high-performance applications.

Responsibilities:
Application Development:

Design, develop, and maintain web-based applications using Java/J2EE, Spring, Hibernate, and other related technologies.
Develop front-end components using HTML5, CSS3, JavaScript, AngularJS, React.js, and other frameworks.
Cloud and Microservices:

Implement microservices architecture using Spring Boot, Spring Cloud, and Docker.
Deploy applications on cloud platforms such as AWS and Pivotal Cloud Foundry.
CI/CD and DevOps:

Implement Continuous Integration and Continuous Deployment (CI/CD) processes using Jenkins, Maven, and Git.
Utilize Docker for containerization and manage deployments on cloud environments.
Database Management:

Design and manage relational and NoSQL databases, including MySQL, Oracle, MongoDB, and Cassandra.
Develop complex SQL queries, stored procedures, and triggers.
Web Services and APIs:

Develop and consume RESTful and SOAP web services.
Ensure secure and efficient communication between services.
Agile Methodologies:

Work in an Agile environment, participating in daily stand-ups, sprint planning, and retrospectives.
Collaborate with cross-functional teams to gather and analyze requirements.
Technical Leadership:

Mentor junior developers and provide guidance on best practices and coding standards.
Conduct code reviews to ensure code quality and adherence to standards.
Qualifications:
Technical Skills:

Proficient in Java, J2EE, Spring, Hibernate, and related frameworks.
Strong front-end development skills with HTML5, CSS3, JavaScript, AngularJS, and React.js.
Experience with AWS services such as EC2, S3, ELB, Auto-Scaling, and DynamoDB.
Hands-on experience with CI/CD tools like Jenkins and Maven.
Knowledge of database management and SQL, with experience in Oracle, MySQL, MongoDB, and Cassandra.
Experience with web services (REST and SOAP) and API development.
Familiarity with Docker, Kubernetes, and other containerization technologies.
Soft Skills:

Excellent problem-solving and analytical skills.
Strong communication and collaboration abilities.
Ability to work independently and as part of a team.
Experience with Agile methodologies and practices.
Experience:
Minimum of 8 years of experience in IT with a focus on Java/J2EE technologies and web application development.
Proven track record of designing and implementing complex, scalable web applications.
Experience with cloud platforms, microservices architecture, and DevOps practices.
This role offers an exciting opportunity to work on cutting-edge technologies and contribute to the success of innovative projects. If you are passionate about technology and enjoy solving complex problems, we would love to hear from you.
"""

    message_content = f"SKILLS:\n{SKILLS}\nJOB DESCRIPTION:\n{test}\n"
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": message_content}
    ]

    return ask_gpt(messages)
    

def search(parsed_description):
    pass