from flask import Flask, render_template, request, make_response, jsonify, url_for, redirect, session
from flask_paginate import Pagination
from requester import get_all_resources
from operator import itemgetter

import settings

app = Flask(__name__)
resources = get_all_resources()
app.config.update(
    SECRET_KEY='starwars',
)


@app.route("/", methods=['GET', 'POST'])
def index(limit=10):
    if request.method == 'POST':
        for resource in settings.RESOURCES:
            value = request.form.get(resource)
            if not value:
                continue

            url = value.split(',')[0]
            last_filter = value.split(',')[1]
            session['LAST_FILTER'] = last_filter

            if url:
                data = resources[resource].get(url)
                filtered_data = data.get(settings.RESOURCES_FILTER[resource])
                people = []
                for people_url in filtered_data:
                    people.append(resources['people'].get(people_url))
                session['PEOPLE'] = people
                break
    
    if 'PEOPLE' in session:
        people = session['PEOPLE']
    
    else:
        people = session['PEOPLE'] = list(resources['people'].values())
    
    page = int(request.args.get('page', 1))
    start = (page - 1) * limit
    end = page * limit if len(people) > page * limit else len(people)
    paginate = Pagination(page=page, total=len(people), css_framework='bootstrap4')


    return render_template(
        'index.html', 
        people=people[start:end+1], 
        paginate=paginate, 
        resources=resources, 
        last_filter=session['LAST_FILTER'] if 'LAST_FILTER' in session else None
    )


@app.route("/clear", methods=["GET"])
def clear():
    session.clear()
    return redirect("/")


@app.route("/order", methods=["GET"])
def order_by():
    key = request.args.get('key')
    
    if key in session:
        session[key] = not session[key]
    else:
        session[key] = False

    people = session['PEOPLE']
    session['PEOPLE'] = sorted(people, key=settings.ORDER_FUNCITIONS[key], reverse=session[key])
    return redirect('/')


@app.route("/starships", methods=["GET", "POST"])
def starships():
    all_starships = list(resources['starships'].values())
    sorted_starships = sorted(all_starships, key=itemgetter('score'), reverse=True)
    return render_template("starships.html", starships=sorted_starships)
