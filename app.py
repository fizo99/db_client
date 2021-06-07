#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from scripts import db

DEVELOPMENT_ENV = True

app = Flask(__name__)


@app.route('/')
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
    schema = db.getTableStructure(dbName, tableName)
    data = db.getTableData(dbName, tableName)
    return render_template('table_data_filled.html', tableName=tableName, schema=schema['resultList'],
                           data=data['resultList'])


@app.route('/table/create', methods=['GET', 'POST'])
def table_create_template():
    if request.method == 'GET':
        return render_template('table_create.html')
    else:
        dbName = request.headers.get('dbName')
        tableName = request.headers.get('tableName')
        tableContent = request.json

        if dbName == None or tableName == None \
                or tableContent == None or dbName not in db.getDatabaseNames():
            return jsonify(success=False)
        else:
            result = db.createTable(dbName, tableName, tableContent)
            if result["type"] == "ok":
                return jsonify(success=True)
            else:
                print(result)
                return jsonify(success=False)


@app.route('/table/modify', methods=['DELETE', 'PUT'])
def table_modify():
    if request.method == "DELETE":
        dbName = request.headers.get('dbName')
        tableName = request.headers.get('tableName')
        columnName = request.json['columnName']

        if dbName == None or tableName == None \
                or columnName == None or dbName not in db.getDatabaseNames():
            return jsonify(success=False)
        else:
            result = db.deleteColumn(dbName, tableName, columnName)
            result2 = db.deleteTable(dbName, tableName + "_old")

            if result["type"] == "ok":
                return jsonify(success=True)
            else:
                return jsonify(success=False)
    else:
        dbName = request.headers.get('dbName')
        tableName = request.headers.get('tableName')
        columnName = request.json['columnName']
        dataType = request.json['dataType']
        result = db.addColumn(dbName, tableName, columnName, dataType)

        if result["type"] == "ok":
            return jsonify(success=True)
        else:
            return jsonify(success=False)


@app.route('/table/data/modify', methods=['DELETE', 'PUT'])
def table_data_modify():
    dbName = request.headers.get('dbName')
    tableName = request.headers.get('tableName')
    values = request.json['values']

    if dbName == None or tableName == None \
            or dbName not in db.getDatabaseNames() or values == None:
        return jsonify(success=False)

    if request.method == "DELETE":
        columns = request.json['columnNames']

        if columns == None:
            return jsonify(success=False)
        else:
            result = db.deleteRow(dbName, tableName, columns, values)
            return jsonify(success=True)
    else:
        result = db.insertRow(dbName, tableName, values)
        return jsonify(success=True)


@app.route('/table', methods=['GET'])
def get_tables():
    dbName = request.headers.get('dbName')
    return db.getTableNames(dbName)


@app.route('/database', methods=['GET'])
def get_databases():
    return jsonify(db.getDatabaseNames()), 201


@app.route('/table/schemas', methods=['GET'])
def get_table_schema():
    dbName = request.headers.get('dbName')
    tableName = request.headers.get('tableName')
    return db.getTableStructure(dbName, tableName)


@app.route('/query', methods=['POST'])
def custom_query():
    dbName = request.headers.get('dbName')
    queryString = request.json['query']
    result = db.query(dbName, queryString)
    if result['type'] == "ok":
        return jsonify(output=result['msg'], success=True)
    else:
        return jsonify(output=result['msg'], success=False)


@app.route('/database/create/<dbname>')
def dbcreator(dbname):
    result = db.createDB(dbname)
    if result['type'] == 'ok':
        return result, 201
    else:
        return result, 400


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
