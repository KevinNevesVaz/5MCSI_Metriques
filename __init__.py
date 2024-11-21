from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)
                                                                                                                                    
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm
  
@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

# Route pour récupérer les données des commits
@app.route('/commits-data/')
def commits_data():
    # URL de l'API GitHub
    api_url = "https://api.github.com/repos/KevinNevesVaz/5MCSI_Metriques/commits"

    # Effectuer la requête pour récupérer les commits
    response = requests.get(api_url)
    if response.status_code != 200:
        return jsonify({"error": "Impossible de récupérer les données de l'API GitHub"}), 500

    # Extraire les dates des commits
    commits = response.json()
    commit_minutes = []
    for commit in commits:
        date_str = commit['commit']['author']['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        commit_minutes.append(date_obj.minute)  # Extraire la minute

    # Compter les occurrences de chaque minute
    commit_count = Counter(commit_minutes)

    # Convertir le résultat en un format JSON
    results = [{"minute": minute, "count": count} for minute, count in sorted(commit_count.items())]
    return jsonify(results=results)

# Route pour afficher le fichier HTML
@app.route('/commits/')
def commits():
    return render_template("commits.html")
  
if __name__ == "__main__":
  app.run(debug=True)
