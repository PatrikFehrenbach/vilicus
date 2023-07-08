from flask import request, Blueprint, jsonify, redirect, url_for
from models import domains_collection, Domain, subdomains_collection, Subdomain
from bson.objectid import ObjectId


main = Blueprint('domain_main', __name__)  # Create a Blueprint instance

@main.route('/add_domain', methods=['POST'])
def add_domain():
    name = request.json.get('name')
    if not name:
        return 'No domain name provided', 400
    domain = Domain(name)
    domain.save()
    return 'Domain added successfully!', 201

@main.route('/update_domain/<string:domain_name>', methods=['POST'])
def update_domain(domain_name):
    new_name = request.json.get('name')
    if not new_name:
        return 'No new domain name provided', 400
    domain = domains_collection.find_one({'name': domain_name})
    if not domain:
        return 'Domain not found', 404
    domain_obj = Domain(name=new_name)
    domain_obj.id = domain['_id']
    domain_obj.update()
    return 'Domain updated successfully!'

@main.route('/delete_domain/<string:domain_name>', methods=['POST'])
def delete_domain(domain_name):
    domain = domains_collection.find_one({'name': domain_name})
    if not domain:
        return 'Domain not found', 404
    domain_obj = Domain('')
    domain_obj.id = domain['_id']
    domain_obj.delete()
    return 'Domain deleted successfully!'

from bson.json_util import dumps

@main.route('/domains/export', methods=['GET'])
def export_domains():
    domains = list(domains_collection.find())
    return dumps(domains), 200

@main.route('/domains/search', methods=['GET'])
def search_domain():
    query = request.args.get('q')
    search_results = domains_collection.find({'name': {'$regex': query}})
    only_name = [domain['name'] for domain in search_results]
    return jsonify(dumps(search_results))
