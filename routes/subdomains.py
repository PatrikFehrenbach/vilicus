# routes/subdomain.py
from flask import request, Blueprint, jsonify, render_template
from models import subdomains_collection, Subdomain, domains_collection, Domain
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime, timedelta
import logging
import requests
from models import Domain
from .utils import get_subdomains

main = Blueprint('subdomain_main', __name__)  # Create a Blueprint instance

@main.route('/add_subdomain/<string:main_domain>', methods=['POST'])
def add_subdomain(main_domain):
    # Retrieve the domain document from the database using the main domain name
    domain = domains_collection.find_one({'name': main_domain})
    if not domain:
        return 'Main domain not found', 404

    # Create the Domain object
    domain_obj = Domain(name=domain['name'])
    domain_obj.id = domain['_id']  # set the id of the domain object

    # Get the subdomain name from the request body
    subdomain_name = request.json.get('subdomain_name')

    if not subdomain_name:
        return 'No subdomain name provided', 400

    # Add the subdomain
    response_message = domain_obj.add_subdomain(subdomain_name)
    if "successfully" in response_message:
        return response_message, 201
    else:
        return response_message, 409  # conflict


@main.route('/update_subdomain/<string:main_domain>/<string:subdomain_name>', methods=['POST'])
def update_subdomain(main_domain, subdomain_name):
    new_name = request.json.get('name')
    if not new_name:
        return 'No new subdomain name provided', 400
    domain = domains_collection.find_one({'name': main_domain})
    if not domain:
        return 'Main domain not found', 404
    subdomain = subdomains_collection.find_one({'name': subdomain_name, 'domain_id': domain['_id']})
    if not subdomain:
        return 'Subdomain not found', 404
    subdomain_obj = Subdomain(domain_id=domain['_id'], name=new_name)
    subdomain_obj.id = subdomain['_id']
    subdomain_obj.update()
    return 'Subdomain updated successfully!'

@main.route('/delete_subdomain/<string:main_domain>/<string:subdomain_name>', methods=['POST'])
def delete_subdomain(main_domain, subdomain_name):
    domain = domains_collection.find_one({'name': main_domain})
    if not domain:
        return 'Main domain not found', 404
    subdomain = subdomains_collection.find_one({'name': subdomain_name, 'domain_id': domain['_id']})
    if not subdomain:
        return 'Subdomain not found', 404
    subdomain_obj = Subdomain(domain_id=domain['_id'], name='')
    subdomain_obj.id = subdomain['_id']
    subdomain_obj.delete()
    return 'Subdomain deleted successfully!'

@main.route('/subdomains/export', methods=['GET'])
def export_subdomains():
    subdomains = list(subdomains_collection.find())
    returm_only_name = [subdomain['name'] for subdomain in subdomains]
    return dumps(returm_only_name), 200


@main.route('/<string:domain_name>/subdomains/export', methods=['GET'])
def export_subdomains_by_domain(domain_name):
    domain = domains_collection.find_one({'name': domain_name})
    if not domain:
        return 'Domain not found', 404
    subdomains = subdomains_collection.find({'domain_id': domain['_id']})
    names = [subdomain['name'] for subdomain in subdomains]
    return jsonify(names)

@main.route('/subdomains/search', methods=['GET'])
def search_subdomain():
    query = request.args.get('q')
    search_results = subdomains_collection.find({'name': {'$regex': query}})
    only_name = [subdomain['name'] for subdomain in search_results]
    return jsonify(dumps(only_name))
    #return jsonify(dumps(search_results))

@main.route('/lastupdated', methods=['GET'])
def get_last_updated():
    # Calculate the time 30 minutes ago
    half_hour_ago = datetime.utcnow() - timedelta(minutes=1)

    # Query the database for any subdomains added after half_hour_ago
    new_subdomains = list(subdomains_collection.find({"added_at": {"$gte": half_hour_ago}}))

    # Convert the query result to JSON and return it
    return dumps(new_subdomains)

@main.route('/sort_subdomains')
def sort_subdomains():
    domains = Domain.get_all_domains()
    domains = sorted(domains, key=lambda domain: domain.subdomains_count, reverse=True)
    summary = Domain.get_summary()
    return render_template('index.html', domains=domains, summary=summary)

