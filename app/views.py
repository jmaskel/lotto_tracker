from flask import Blueprint, render_template, jsonify  # Import jsonify here
from .scraper import scrape_data

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/data')
def data():
    scraped_data = scrape_data()
    return jsonify(scraped_data)
