from flask import Blueprint, request, jsonify
from app.models import add_document_to_db, search_documents, summarize_content
from app.utils import query_llm, handle_file_upload
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/add_document', methods=['POST'])
def add_document():
    try:
        title = request.form['title']
        content = request.form['content']
        file = request.files.get('file')

        file_path = handle_file_upload(file)

        add_document_to_db(title, content, file_path)
        return jsonify({"message": "Document added successfully"}), 200
    except Exception as e:
        logging.error(f"Error adding document: {e}")
        return jsonify({"error": "Failed to add document"}), 500

@main_routes.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query', '')
        results = search_documents(query)

        if not results:
            return jsonify({"message": "No documents found matching the query."}), 404

        summaries = []
        for title, content in results:
            prompt = f"Summarize the following document about {title}:\n\n{content}\n\nSummary:"
            summary = query_llm(prompt)
            summaries.append({"title": title, "summary": summary})

        return jsonify(summaries), 200
    except Exception as e:
        logging.error(f"Error searching documents: {e}")
        return jsonify({"error": "Failed to search documents"}), 500

@main_routes.route('/summarize', methods=['POST'])
def summarize_file():
    try:
        content = request.form['content']
        summary = summarize_content(content)
        return jsonify({"summary": summary}), 200
    except Exception as e:
        logging.error(f"Error summarizing file: {e}")
        return jsonify({"error": "Failed to summarize document"}), 500
