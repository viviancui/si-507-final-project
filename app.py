from flask import Flask, render_template, url_for, request, Markup, redirect
import requests
from plotly.offline import plot
# import plotly.graph_objs
from plotly.graph_objs import Scatter
from plotly.graph_objs import Bar
import model
import data_spotify
import data_database
import billboard
import musixmatch_request
import json
import os

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('login.html')

@app.route("/posttoken", methods=['GET', 'POST'])
def posttoken():
    token = request.form["token"]
    model.add_token(token) #using the add_entry function in model.py file
    top_artist_json = data_spotify.get_top_artists(model.get_token())
    artist_list = data_spotify.get_artist_list(top_artist_json)
    return render_template("/top10bands.html", artist_list = artist_list)

@app.route("/postband", methods=['GET', 'POST'])
def postband():
    band = request.form["band"]
    band_list = data_database.get_band_list()
    if band not in band_list:
        data_database.populate_Database(band)
        model.add_band_name(band)
        # model.wordJson(band)
        return render_template("/specificband.html", band=band)
    else:
        model.add_band_name(band)
        # model.wordJson(band)
        return render_template("/specificband.html", band=band)

@app.route("/postbillboard", methods=['GET', 'POST'])
def postbillboard():
    page_text = billboard.get_page_cache()
    title_list = billboard.get_data(page_text)
    genre_list = musixmatch_request.genre_distribution(title_list)
    genre_tuple = musixmatch_request.genre_count(genre_list)
    my_plot_div = plot([Bar(x=genre_tuple[0], y=genre_tuple[1])], output_type='div')
    return render_template("/billboard.html", div_placeholder= Markup(my_plot_div), billboard_list=title_list)

# @app.route("/posttop10", methods=['GET', 'POST'])
# def posttop10():
#     band = request.form["Slayer"]
#     model.wordJson(band)
#     f = open('bubblechart.json', 'r')
#     f_text = f.read()
#     data = json.dumps(f_text)
#     return render_template('bubblechart.html', data=data)

# @app.route("/bubblechart/<band>", methods=['GET', 'POST'])
@app.route("/bubblechart/<band>")
def posttop10(band):
    band_list = data_database.get_band_list()
    if band not in band_list:
        data_database.populate_Database(band)
        model.add_band_name(band)
        bubble_tuple = model.word_count(band)
        my_plot_div = plot([Bar(x=bubble_tuple[0], y=bubble_tuple[1])], output_type='div')
        return render_template("/wordcount.html", div_placeholder= Markup(my_plot_div), band=band)
    else:
        model.add_band_name(band)
        bubble_tuple = model.word_count(band)
        my_plot_div = plot([Bar(x=bubble_tuple[0], y=bubble_tuple[1])], output_type='div')
        return render_template("/wordcount.html", div_placeholder= Markup(my_plot_div), band=band)
    # model.wordJson(band)
    # f = open('bubblechart_1.json', 'r')
    # f_text = f.read()
    # data = json.dumps(f_text)
    # return render_template('bubblechart.html', data=data)

@app.route("/specificband/<band>")
def getband(band):
    return render_template("/specificband.html", band=band)

@app.route('/postreleaseyear', methods=['GET', 'POST'])
def releaseyear():
    name = model.get_band_name()
    tuple = model.releaseYear(name)
    my_plot_div = plot([Scatter(x=tuple[0], y=tuple[1])], output_type='div')
    return render_template('releaseyear.html',
                           div_placeholder= Markup(my_plot_div), band=name
                          )

@app.route('/posttrack', methods=['GET', 'POST'])
def tracklength():
    # error = None
    # if request.method == 'POST':
    name = model.get_band_name()
    tuple = model.trackLength(name)
    my_plot_div = plot([Scatter(x=tuple[0], y=tuple[1])], output_type='div')
    return render_template('tracklength.html',
                           div_placeholder= Markup(my_plot_div), band=name
                          )
    # elif request.method == "GET":
    #     return redirect(url_for('/tracklength.html', error=error))


@app.route('/postbubble', methods=['GET', 'POST'])
def bubble_chart():
    band = model.get_band_name()
    bubble_tuple = model.word_count(band)
    my_plot_div = plot([Bar(x=bubble_tuple[0], y=bubble_tuple[1])], output_type='div')
    return render_template("/wordcount.html", div_placeholder= Markup(my_plot_div), band=band)

    # return redirect('localhost:8000/bubblechart.html')
    # f = open('bubblechart_1.json', 'r')
    # f_text = f.read()
    # data = json.dumps(f_text)
    # # band = model.get_band_name()
    # # model.wordJson(band)
    # return render_template('bubblechart.html', data=data)




    # with open('bubblechart.json') as json_data:
    #     d = json.load(json_data)

    # # error = None

    # # if request.method == 'POST':
    #     # return render_template('/bubblechart.html')
    #
    # elif request.method == "GET":
    #     return redirect(url_for('/', error=error))
    # # return render_template('/bubblechart.html')
    #
    # df = pd.read_csv('data').drop('Open', axis=1)
    # chart_data = df.to_dict(orient='records')
    # chart_data = json.dumps(chart_data, indent=2)
    # data = {'chart_data': chart_data}

    # return render_template("bubblechart.html", data=d)

if __name__ == '__main__':
    if not os.path.exists('whatdidtheysay.db'):
        data_database.create_db()   #using the init() function in the database.py file
    else:
        pass
    app.run(debug=True)
    # app.run(app.run( port=8000),debug=True)
