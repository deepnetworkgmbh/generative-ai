import parse_static
import parse_generic 

def read_job():
    pass

def main_generic():
    parsed_description = parse_generic.create_query(job_description)
    results = parse_generic.search(parsed_description)
    return results

def main_static(job_description):
    parsed_description = parse_static.create_query(job_description)
    results = parse_static.search(parsed_description)
    return results

if __name__ == "__main__":
    job_description = read_job()

    #print("generic:"+ main_generic(job_description))
    main_static(job_description)
    