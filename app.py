from flask import Flask, render_template, request


import data


app = Flask(__name__)

# Data is mapped in data.py
data.main()
data_map = data.get_data()
sorted_keys = data.get_sorted_keys()
inverted_dependencies = data.get_inverted_dependencies()


@app.route('/')
def index():
    # The index of sorted package names.
    return render_template("index.html", packages=sorted_keys)


@app.route('/package.html', methods=['GET', 'POST'])
def package():

    # A individual package with all needed information.
    selected_package = request.args.get("type")
    # If no dependencies or inverted dependencies = None they get set as an empty array.
    return render_template("package.html", package=selected_package,
                           dependencies=data_map.get(selected_package).get("Depends", []),
                           inverted_dependencies=inverted_dependencies.get(selected_package, []),
                           description=data_map[selected_package]["Description"], keys=sorted_keys,
                           title=selected_package)


if __name__ == '__main__':
    app.run(debug=True)
