# models.py
from pymongo import MongoClient,DESCENDING

client = MongoClient('mongodb://admin:admin123@mongodb:27017/')
db = client['recon']
domains_collection = db['domains']
subdomains_collection = db['subdomains']
from datetime import datetime

# Create index
subdomains_collection.create_index([("added_at", DESCENDING)])
subdomains_collection.create_index('domain_id')
subdomains_collection.create_index([('domain_id', 1), ('added_at', -1)])



# models.py
from bson.objectid import ObjectId

class Domain:
    def __init__(self, name):
        self.name = name
        self.subdomains_count = 0
        self.id = None  # The ID assigned by MongoDB.
        self.subdomains = []  # Define subdomains here
        self.last_updated = None  # Define last_updated here

    def subdomain_count(self):
        return self.subdomains_count

    def get_all_domains():
        domains = domains_collection.find({})
        return domains
    
    def last_updated(self):
        # Get the most recent subdomain of this domain
        subdomain_data = subdomains_collection.find({'domain_id': self.id}).sort('added_at', -1).limit(1)

        subdomain_data = list(subdomain_data)

        # If there is a subdomain, return the added_at of it (the most recently added),
        # otherwise return None
        return subdomain_data[0]['added_at'] if subdomain_data else None


    def save(self):
        existing_domain = domains_collection.find_one({'name': self.name})
        if existing_domain:
            return "Domain already exists"
        else:
            domain_data = {'name': self.name, 'subdomains': []}
            domain_id = domains_collection.insert_one(domain_data).inserted_id
            self.id = domain_id

    def update(self):
        existing_domain = domains_collection.find_one({'_id': ObjectId(self.id)})
        if existing_domain:
            domains_collection.update_one({'_id': ObjectId(self.id)}, {'$set': {'name': self.name}})
            return "Domain updated successfully"
        else:
            return "Domain not found"

    def delete(self):
        domains_collection.delete_one({'_id': ObjectId(self.id)})
        subdomains_collection.delete_many({'domain_id': self.id})

    def add_subdomain(self, subdomain):
        existing_subdomain = subdomains_collection.find_one({'name': subdomain, 'domain_id': self.id})
        if not existing_subdomain:
            subdomain_obj = Subdomain(self.id, subdomain)
            subdomain_obj.save()
            self.subdomains_count += 1  # Increase the count.
            self.last_updated = datetime.utcnow()  # Update last_updated with the current time
            domains_collection.update_one({'_id': ObjectId(self.id)}, {'$inc': {'subdomains_count': 1}, '$set': {'last_updated': self.last_updated}})  # Update the count and last_updated in the database.
            return "Subdomain added successfully"
        else:
            return "Subdomain already exists"


    def remove_subdomain(self, subdomain):
        subdomains_collection.delete_one({'name': subdomain, 'domain_id': self.id})
        self.subdomains_count -= 1  # Decrease the count.
        domains_collection.update_one({'_id': ObjectId(self.id)}, {'$inc': {'subdomains_count': -1}})  # Update the count in the database.


    def get_subdomains(self):
        subdomains_data = subdomains_collection.find({'domain_id': self.id})
        self.subdomains = [Subdomain(subdomain['domain_id'], subdomain['name']) for subdomain in subdomains_data]
        return self.subdomains
    
    @staticmethod
    def get_summary():
        domain_count = domains_collection.count_documents({})
        subdomain_count = subdomains_collection.count_documents({})
        return {'domain_count': domain_count, 'subdomain_count': subdomain_count}
    
    @staticmethod
    def get_by_name(name):
        domain_data = domains_collection.find_one({'name': name})
        if domain_data:
            domain = Domain(name)
            domain.id = domain_data['_id']
            domain.subdomains_count = domain_data.get('subdomains_count', 0)
            return domain
        else:
            return None

class Subdomain:
    def __init__(self, domain_id, name):
        self.domain_id = domain_id
        self.name = name
        self.added_at = datetime.utcnow()  # the timestamp for when the subdomain is created
        self.id = None  # Store the subdomain ID

    def save(self):
        subdomains_collection.insert_one({
            'domain_id': self.domain_id,
            'name': self.name,
            'added_at': self.added_at
        })
    def update(self):
        subdomains_collection.update_one({'_id': self.id}, {'$set': {'name': self.name}})

    def get_total_subdomains(self):
        return subdomains_collection.count_documents({})
    

    def delete(self):
        subdomains_collection.delete_one({'_id': self.id})

    def update_domain_subdomains(domain_id, subdomains):
        domain = Domain.get_by_id(domain_id)
        if domain:
            for subdomain_name in subdomains:
                subdomain = Subdomain(domain_id, subdomain_name)
                existing_subdomain = subdomains_collection.find_one({'name': subdomain_name, 'domain_id': domain_id})
                if not existing_subdomain:  # Check if subdomain already exists
                    subdomain.save()
        else:
            print("Domain not found")

    def get_subdomains(self):
        subdomains = subdomains_collection.find({'domain': self.name})
        return subdomains

    @staticmethod
    def get_by_domain_id(domain_id):
        return subdomains_collection.find({'domain_id': domain_id})
