#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from scripts import db

DEVELOPMENT_ENV = True

app = Flask(__name__)


## TEMPLATES

@app.route('/', methods=['GET'])
def index():
    databases = db.getDatabaseNames()
    return render_template('index.html', databases=databases, len=len(databases))


@app.route('/table/modify', methods=['GET'])
def table_modify_template():
    return render_template('table_modify.html')


@app.route('/table/data', methods=['GET'])
def table_data_template():
    return render_template('table_data.html')


@app.route('/customquery', methods=['GET'])
def custom_query_template():
    return render_template('custom_query.html')


@app.route('/table/data/<tableName>', methods=['GET'])
def table_data_template_filled(tableName):
    dbName = request.headers.get('dbName')
    try:
        schema = db.getTableStructure(dbName, tableName)
        data = db.getTableData(dbName, tableName)
        print(schema, data)
        return render_template('table_data_filled.html', tableName=tableName, schema=schema, data=data)
    except Exception as e:
        return jsonify(success=False, msg=e.args[0])


@app.route('/table/create', methods=['GET', 'POST'])
def table_create_template():
    if request.method == 'GET':
        return render_template('table_create.html')
    else:
        dbName = request.headers.get('dbName')
        tableName = request.headers.get('tableName')
        tableContent = request.json
        print(dbName, tableName, tableContent)
        try:
            db.createTable(dbName, tableName, tableContent)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, msg=e.args[0])


@app.route('/table/modify', methods=['DELETE', 'PUT'])
def table_modify():
    dbName = request.headers.get('dbName')
    tableName = request.headers.get('tableName')
    columnName = request.json['columnName']
    if request.method == "DELETE":
        try:
            db.deleteColumn(dbName, tableName, columnName)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, msg=e.args[0])
    else:
        dataType = request.json['dataType']
        try:
            db.addColumn(dbName, tableName, columnName, dataType)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, msg=e.args[0])


@app.route('/table/data/modify', methods=['DELETE', 'PUT'])
def table_data_modify():
    dbName = request.headers.get('dbName')
    tableName = request.headers.get('tableName')
    values = request.json['values']

    if request.method == "DELETE":
        columns = request.json['columnNames']
        try:
            db.deleteRow(dbName, tableName, columns, values)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, msg=e.args[0])
    else:
        try:
            db.insertRow(dbName, tableName, values)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, msg=e.args[0])


@app.route('/table', methods=['GET'])
def get_tables():
    dbName = request.headers.get('dbName')
    try:
        return jsonify(success=True, names=db.getTableNames(dbName))
    except Exception as e:
        return jsonify(success=False, msg=e.args[0])


@app.route('/database', methods=['GET'])
def get_databases():
    return jsonify(db.getDatabaseNames()), 201


@app.route('/table/schemas', methods=['GET'])
def get_table_schema():
    dbName = request.headers.get('dbName')
    tableName = request.headers.get('tableName')
    try:
        return jsonify(success=True, schemas=db.getTableStructure(dbName, tableName))
    except Exception as e:
        return jsonify(success=False, msg=e.args[0])


@app.route('/query', methods=['POST'])
def custom_query():
    dbName = request.headers.get('dbName')
    queryString = request.json['query']
    try:
        db.query(dbName, queryString)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, msg=e.args[0])


@app.route('/database/create/<dbname>')
def dbcreator(dbname):
    try:
        db.createDB(dbname)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, msg=e.args[0])


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
