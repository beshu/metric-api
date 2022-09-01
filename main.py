from flask import Flask, request
import helpers

app = Flask(__name__)
helpers.run_database(app)
helpers.register_metric_api(app)

if __name__ == "__main__":
    app.run()
