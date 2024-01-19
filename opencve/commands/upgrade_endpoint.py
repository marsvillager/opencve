from pathlib import Path

import click
from flask.cli import with_appcontext


from opencve.commands import ensure_config
from opencve.configuration import config
import psycopg2

import uuid

from opencve.configuration import (
    DEFAULT_CONFIG,
    DEFAULT_WELCOME_FILES,
    OPENCVE_CONFIG,
    OPENCVE_HOME,
    OPENCVE_WELCOME_FILES,
)
import json


@click.command()
@ensure_config
@with_appcontext
def upgrade_endpoint():
    """upgrade endpoints in database."""
    database_uri = config.get("core", "database_uri")
    db_info = database_uri.split(":")
    database = db_info[3].split("/")[1]
    user = db_info[1].split("/")[2]
    password = db_info[2].split("@")[0]
    host = db_info[2].split("@")[1]
    port = db_info[3].split("/")[0]

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)

    cursor=conn.cursor()

    records = []

    with open('/app/records.jsonl', 'r') as f:
        for line in f:
            records.append(json.loads(line.strip()))
    
    for record in records:
        uuid_value = uuid.uuid4()

        sql = '''
        INSERT INTO endpoints (id ,mac, json) VALUES ('{0}','{1}','{2}') ON CONFLICT (mac) DO UPDATE SET json = EXCLUDED.json
        '''.format(uuid_value,record["MAC Address"],json.dumps(record))
        
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()