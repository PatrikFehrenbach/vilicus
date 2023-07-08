from flask import Blueprint, render_template, request, jsonify
from models import domains_collection, subdomains_collection, Domain,Subdomain
from bson.json_util import dumps
import tldextract
from werkzeug.utils import secure_filename
import os
from application import create_app
import requests
import logging
import threading
from .subdomains import get_subdomains
import threading
from .index import get_subdomains

app = create_app()

# Create a Blueprint instance
API_KEY = ""
BASE_URL = "https://api.securitytrails.com/v1"

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET'])
def index():
    # Get all domains from the database
    domains_data = Domain.get_all_domains()

    # Convert each domain in domains_data to a Domain object and assign the timestamp of the last subdomain added to the last_updated attribute
    domains = []
    for domain_data in domains_data:
        domain = Domain(domain_data['name'])
        domain.id = domain_data['_id']
        domain.subdomains_count = domain_data.get('subdomains_count', 0)

        # Get the last updated time of the domain
        last_subdomain = subdomains_collection.find_one(
            {'domain_id': domain.id},
            projection={'added_at': 1},
            sort=[('added_at', -1)]
        )
        domain.last_updated = last_subdomain['added_at'] if last_subdomain else None
        domains.append(domain)

    return render_template('index.html', domains=domains)


@main.route('/add_domain', methods=['POST'])
def add_domain():
    name = request.json.get('name')
    if not name:
        return jsonify({'message': 'No domain name provided'}), 400
    domain = Domain(name)
    domain.save()
    try:
        # Call the get_subdomains function
        subdomains = get_subdomains(name)
        logging.info(f'Subdomains added for {name}: {subdomains}')  # Log the added subdomains
        return jsonify({'message': 'Domain and its subdomains added successfully!', 'subdomains': subdomains}), 201
    except Exception as e:
        logging.error(f'Error while getting subdomains for {name}: {e}')
        return jsonify({'message': 'Domain added, but failed to get its subdomains'}), 201



@main.route('/reset', methods=['GET'])
def reset_database():
    domains_collection.delete_many({})
    subdomains_collection.delete_many({})
    return jsonify({"message": "Database has been reset"})

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    domain_results = domains_collection.find({'name': {'$regex': query}})
    subdomain_results = subdomains_collection.find({'name': {'$regex': query}})
    # Combine results and convert to JSON
    all_results = list(domain_results) + list(subdomain_results)
    all_results_json = dumps(all_results)
    return all_results_json

@main.route('/upload_subdomains', methods=['POST'])
def upload_subdomains():
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Open the file and read the subdomains
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
            subdomain_names = f.read().splitlines()

        # Add each subdomain to the database
        domain_obj = None  # Define domain_obj with a default value
        for name in subdomain_names:
            # Extract the main domain name and subdomain from each domain in the list using tldextract
            extracted = tldextract.extract(name)
            print(extracted)
            main_domain = "{}.{}".format(extracted.domain, extracted.suffix)
            print(main_domain)
            subdomain_name = extracted.subdomain
            subdomain_name_with_main_domain = "{}.{}".format(subdomain_name, main_domain)
            print(subdomain_name_with_main_domain)
            print(subdomain_name)

            # Check if the main domain exists in the database
            domain = domains_collection.find_one({'name': main_domain})
            if domain is None:
                # If not, add it to the database
                domain = Domain(main_domain)
                domain.save()
                print("Domain %s added successfully!" % main_domain)
                # Create the Domain object
                domain_obj = Domain(name=domain.name)
                domain_obj.id = domain.id
            else:
                # If yes, create a Domain object for it
                domain_obj = Domain(name=domain['name'])
                domain_obj.id = domain['_id']

            # Add the subdomain
            domain_obj.add_subdomain(subdomain_name_with_main_domain)

        return 'Subdomains uploaded successfully!', 200
    else:
        return 'File not allowed', 400

def update_subdomains_task():
    # Read the domains from the file
    with open('domains_to_monitor.txt', 'r') as file:
        domains = file.read().splitlines()

    for domain_name in domains:
        # Get the domain object from the database
        domain_object = Domain.get_by_name(domain_name)
        
        # If the domain does not exist in the database, create a new one and save it
        if not domain_object:
            domain_object = Domain(domain_name)
            domain_object.save()

        # Get the subdomains from the API
        print("Getting subdomains for %s" % domain_object.name)
        subdomains = get_subdomains(domain_object.name)





