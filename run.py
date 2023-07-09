from application import create_app
from routes.index import main as index_blueprint
from routes.index import update_subdomains_task
from routes.domain import main as domain_blueprint
from routes.subdomains import main as subdomain_blueprint
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

# register blueprints
app.register_blueprint(index_blueprint)
app.register_blueprint(domain_blueprint)
app.register_blueprint(subdomain_blueprint)

scheduler = BackgroundScheduler()
# scheduler.add_job(update_subdomains_task, 'interval', seconds=24)

scheduler.start()
print("Scheduler started!")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
