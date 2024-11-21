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

@app.route('/commits/')
def commits():
    # URL de l'API GitHub
    url = "https://api.github.com/repos/KevinNevesVaz/5MCSI_Metriques/commits"
    
    # Requête pour récupérer les commits
    response = requests.get(url)
    commits_data = response.json()
    
    # Extraire les minutes de chaque commit
    minutes = []
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        minutes.append(date_object.minute)
    
    # Compter le nombre de commits par minute
    commit_counts = Counter(minutes)
    
    # Transformer les données en liste pour le graphique
    results = [{"minute": minute, "count": count} for minute, count in commit_counts.items()]
    
    # Retourner les données au format JSON pour le graphique
    return jsonify(results=results)

@app.route('/commits-graph/')
def commits_graph():
    # Retourne le fichier HTML pour afficher le graphique
    return render_template("commits.html")
  
if __name__ == "__main__":
  app.run(debug=True)
