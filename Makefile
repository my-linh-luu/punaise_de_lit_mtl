export FLASK_APP=index.py
export FLASK_DEBUG=True

run:
		raml2html doc.raml > templates/doc.html
		flask run