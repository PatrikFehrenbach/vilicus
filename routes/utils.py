# utils.py
import requests
import logging
from models import Domain
import os

API_KEY = os.getenv("SECURITYTRAILS")
BASE_URL = "https://api.securitytrails.com/v1"

def get_subdomains(domain):
    subdomains = []

    url = f"{BASE_URL}/domain/{domain}/subdomains?children_only=false&include_inactive=false"
    headers = {"accept": "application/json", "APIKEY": API_KEY}
    response = requests.get(url, headers=headers)
    logging.info(response)
    data = response.json()
    limit_reached = data.get("meta", {}).get("limit_reached")
    logging.info("Limit reached: %s % limit_reached")
    logging.info(data)
    domain_object = Domain.get_by_name(domain) 

    # Check if limit has been reached after first request
    if data.get("meta", {}).get("limit_reached") == True:
        logging.info("Limit reached, using scroll API for Domain %s" % domain)
        url = f"{BASE_URL}/domains/list?include_ips=false&scroll=true"
        payload = {"query": f"apex_domain = \"{domain}\""}
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        scroll_id = data.get("meta", {}).get("scroll_id")
        total_pages = data.get("meta", {}).get("total_pages")

        if scroll_id and total_pages:
            current_page = 1
            while current_page < total_pages:
                url = f"{BASE_URL}/scroll/{scroll_id}"
                response = requests.get(url, headers=headers)
                data = response.json()

                for record in data.get("records", []):
                    subdomain = record.get("hostname")
                    if subdomain:
                        subdomains.append(f"{subdomain}.{domain}")
                        domain_object.add_subdomain(f"{subdomain}.{domain}")

                current_page += 1
    else:
        # If limit not reached, add subdomains from initial response
        subdomains.extend(f"{subdomain}.{domain}" for subdomain in data.get("subdomains", []))
        for subdomain_name in subdomains:
            print("Adding subdomain %s" % subdomain_name)
            domain_object.add_subdomain(subdomain_name)
            logging.info("Subdomain %s added successfully!" % subdomain_name)
    return subdomains
