from pathlib import Path

import click
from flask.cli import with_appcontext
from flask_migrate import upgrade
import re

from opencve.commands import ensure_config
from opencve.configuration import config
import psycopg2


import opencve.views.LLM


@click.command()
@ensure_config
@with_appcontext
def upgrade_result():
    """upgrade results in database."""
    database_uri = config.get("core", "database_uri")
    db_info = database_uri.split(":")
    database = db_info[3].split("/")[1]
    user = db_info[1].split("/")[2]
    password = db_info[2].split("@")[0]
    host = db_info[2].split("@")[1]
    port = db_info[3].split("/")[0]

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cursor=conn.cursor()

    cursor.execute("select id,json from cves where cve_id in ('CVE-2019-9510','CVE-2018-13807','CVE-2022-46141','CVE-2020-1560','CVE-2019-19300','CVE-2021-34527','CVE-2023-5178');")
    cve_list=cursor.fetchall()
    
    cursor.execute("select id,json from endpoints")
    endpoint_list=cursor.fetchall()
    
    for cve_record in cve_list:
        for endpoint_record in endpoint_list:
            #覆盖
            reason=opencve.views.LLM.opencve_chat(str(cve_record[1]["configurations"]),str(endpoint_record))
            
            possibility=-1
            pattern = r'(\d+(\.\d+)?)%'

            matches = re.findall(pattern, reason.split("Possibility",1)[-1])
	
            if matches:
                possibility = int(float(matches[0][0]))

            replace_reason='''INSERT INTO results (cve_id, endpoint_id, reason,possibility) VALUES ('{0}' ,'{1}' ,'{2}' ,{3} ) ON CONFLICT (cve_id, endpoint_id) DO UPDATE SET reason = EXCLUDED.reason , possibility= EXCLUDED.possibility
            '''.format(cve_record[0],endpoint_record[0],reason.replace("'"," "),possibility)
            
            cursor.execute(replace_reason)
        conn.commit()

    cursor.close()
    conn.close()