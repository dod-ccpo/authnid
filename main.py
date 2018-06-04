from authnid.app import app

print(app.config['PORT'])
if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=app.config['PORT'])
