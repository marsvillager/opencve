from pathlib import Path

import click
from flask.cli import with_appcontext
from flask_migrate import upgrade



from opencve.commands import ensure_config
from opencve.configuration import config
import psycopg2
import csv

from opencve.configuration import (
    DEFAULT_CONFIG,
    DEFAULT_WELCOME_FILES,
    OPENCVE_CONFIG,
    OPENCVE_HOME,
    OPENCVE_WELCOME_FILES,
)

@click.command()
@ensure_config
@with_appcontext
@click.argument('possibility')

def export_victim(possibility):
    """export victims in database."""
    database_uri = config.get("core", "database_uri")
    db_info = database_uri.split(":")
    database = db_info[3].split("/")[1]
    user = db_info[1].split("/")[2]
    password = db_info[2].split("@")[0]
    host = db_info[2].split("@")[1]
    port = db_info[3].split("/")[0]

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor=conn.cursor()

    header = ['MAC', 'endpoint_json', 'Cve_id', 'cve_json','reason','possibility(%)']

    sql='''
        select endpoints.mac,endpoints.json,cves.cve_id,cves.json,results.reason,results.possibility
        from endpoints,cves,results
        where endpoints.id=results.endpoint_id and cves.id=results.cve_id and results.possibility >= '{0}'
    '''.format(possibility)

    cursor.execute(sql)
    victims=cursor.fetchall()
    try:
        f=open(OPENCVE_HOME + '/victim.csv', 'x') 
    except FileExistsError:
        f=open(OPENCVE_HOME + '/victim.csv', 'w')

    writer = csv.writer(f)
    writer.writerow(header)
    for victim in victims:
        writer.writerow(victim)

    cursor.close()
    conn.close()
    f.close()