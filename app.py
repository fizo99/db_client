#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from scripts import db

DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "somedata": 'aaa',
    "name": "Peter's Starter Template for a Flask Web App",
    "description": "A basic Flask app using bootstrap for layout",
    "author": "Peter Simeth",
    "html_title": "Peter's Starter Template for a Flask Web App",
    "project_name": "Starter Template",
    "keywords": "flask, webapp, template, basic"
}


@app.route('/')
def index():
    databases = db.getDatabaseNames()
    return render_template('index.html', databases=databases, len=len(databases))


@app.route('/tables/<dbName>')
def tables(dbName):
    tables = db.getTableNames(dbName)
    return render_template('tables.html', tables=tables['resultList'], len=len(tables['resultList']))


@app.route('/schemas/<dbName>/<tableName>')
def schema(dbName,tableName):
    tableSchema = db.getTableStructure(dbName,tableName)
    return render_template('schema.html', rows=tableSchema['resultList'], len=len(tableSchema['resultList']))

@app.route('/schemas/new/<dbName>/<tableName>')
def newtableschema(dbName,tableName):
    return render_template('newtable.html', tableName = tableName)



@app.route('/data')
def data():
    return render_template('data.html', app_data=app_data)

@app.route('/database/create/<dbname>')
def dbcreator(dbname):
    result = db.createDB(dbname)
    if result['type'] == 'ok':
        return result, 201
    else:
        return result, 400


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
