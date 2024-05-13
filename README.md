<p align="center">
  <img alt="OpenCVE" src="https://raw.githubusercontent.com/opencve/opencve/master/logo.png">
</p>
<p align="center">
  <a href="https://github.com/opencve/opencve/actions?query=workflow%3ATests"><img alt="Tests" src="https://github.com/opencve/opencve/workflows/Tests/badge.svg"></a>
  <a href="https://www.python.org/"><img alt="Python versions" src="https://img.shields.io/badge/python-3.7%2B-blue.svg"></a>
  <a href="https://github.com/python/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/opencve/opencve/master/opencve1.png" width="270" height="150">
  <img src="https://raw.githubusercontent.com/opencve/opencve/master/opencve2.png" width="270" height="150">
  <img src="https://raw.githubusercontent.com/opencve/opencve/master/opencve3.png" width="270" height="150">
  <img src="https://raw.githubusercontent.com/opencve/opencve/master/opencve4.png" width="270" height="150">
  <img src="https://raw.githubusercontent.com/opencve/opencve/master/opencve5.png" width="270" height="150">
  <img src="https://raw.githubusercontent.com/opencve/opencve/master/opencve6.png" width="270" height="150">
</p>

----------------

Try **for free** OpenCVE on [https://www.opencve.io](https://www.opencve.io) or check [documentation](https://docs.opencve.io) to install it yourself.

## What is OpenCVE

**OpenCVE** is a platform used to locally import the list of CVEs and perform searches on it (by vendors, products, CVSS, CWE...).

Users subscribe to vendors or products, and OpenCVE alerts them when a new CVE is created or when an update is done in an existing CVE.

## Features

- **Explore** the CVE database and filter the results by Vendor, Product, CVSS score or CWE
- **Subscribe** to vendors and products extracted from CPE
- **Be notified** for new CVE and for CVE updates based on subscriptions
- **Analyse** all CVE details (vendors, products, CVSS score, CPE, CWE, References...)
- **Create** custom tags (unread, important, devteam...) to organize the CVE list
- **Display** the history of each CVE and see their last changes in the homepage
- **Retrieve** the last changes in custom reports
- **Customize** the notification settings (frequency, filter by CVSS score...)
- **Integrate** OpenCVE with your own tools using the Rest API

You can use **for free** these features on the public instance: [https://www.opencve.io](https://www.opencve.io).

## How does it work

OpenCVE uses the [JSON feed](https://nvd.nist.gov/vuln/data-feeds#JSON_FEED) provided by the [NVD](https://nvd.nist.gov/) to update the local list of CVEs.

After an initial import, a background task is regularly executed to synchronize the local copy with the NVD feed. If a new CVE is added, or if a change is detected, the subscribers of the related vendors and products are alerted.

<p align="center">
  <img src="https://raw.githubusercontent.com/opencve/opencve/master/how-it-works.png">
</p>

Read the [How It Works](https://docs.opencve.io/how-it-works/) guide to learn in details how OpenCVE works.

## Requirements

OpenCVE works with **Python >=3.7**.

It uses the JSONB feature for performance, so you will need a **PostgreSQL** instance to store the data (CVE, Users, Vendors, Products, Subscriptions, ...). Other engines are not supported.

The **pg_trgm** module of PostgreSQL is required to let you search in the CVEs list. The [upgrade-db](https://docs.opencve.io/commands/#upgrade-db) command will enable it for you, but you can also do it yourself if you prefer (`CREATE EXTENSION pg_trgm`). From PostgreSQL 13 this module is considered as trusted, meaning it can be installed by non-superusers with the CREATE privilege.

Celery is used to periodically fetch the NVD database and update the list of CVEs. For that you will need a broker : we recommend you **Redis** for the ease of installation. Futhermore it is possible that future versions of OpenCVE will use a cache feature, in that case the Redis requirement will already be filled for you.

During the import of initial data OpenCVE will download and parse huge files, like the CPE dictionnary. For that we recommend you **3.5G RAM** at least.

## Installation

```cmd
git clone https://github.com/marsvillager/opencve.git
git checkout -b discover origin/cve_discover

# 进入虚拟环境
pip install -r requirements.txt
python setup.py install

# 注：MaskupSafe 和 Werkzeug 根据本地 python 版本可能存在版本不合适问题（官方 3.8.17），可以先安装最新版本的 MaskupSafe 和 Werkzeug，成功安装 opencve 之后再卸载之前版本并安装 MaskupSafe 和 Werkzeug
pip install opencve

# Configuration file
export OPENCVE_HOME=./conf
opencve init

# Initialize the database
vim ~/opencve/opencve.cfg
...
database_uri = postgresql://john:mysupersecret@servername:5432/opencve
...
export FLASK_APP=./opencve/app.py
flask db upgrade

# Import the data
opencve import-data				#录入cve数据
opencve upgrade-endpoint		#通过读/conf/records.jsonl录入主机信息
opencve upgrade-result			#通过LLM进行匹配度分析

# Export the data
opencve export-affected-cves	#筛选单主机受cve影响列表（输出到/conf下，命名为'{mac}_affected_cves.json'）
- endpoint mac address:			#mac地址
- the possibility threshold:	#possibility阈值设定
opencve export-victim [POSSIBILITY]		#筛选全局范围受cve影响列表（输出到/conf下，为victim.csv）

# Start the workers
vim ~/opencve/opencve.cfg
...
celery_broker_url = redis://127.0.0.1:6379/0
celery_result_backend = redis://127.0.0.1:6379/1
...
opencve celery worker -l INFO
opencve celery beat -l INFO

# Create an admin
opencve create-user john john.doe@example.com --admin

# Start the webserver
opencve webserver -b [ip:port]
```

## 配置文件路径问题

`./opencve/commands/upgrade_endpoint.py` 中 `upgrade_endpoint()` 函数：

- Manual 路径是 `OPENCVE_HOME + '/records.jsonl'`（`OPENCVE_HOME=./conf`）

## 注意事项说明

/opencve/views/LLM.py

目前采用的是智谱在线的glm4模型，其中的key是短时有效的。后续需要更改为本地LLM与langchain框架接入需要更改相关代码，prompt已在此文件中给出。



/opencve/commands/upgrade_result.py

测试阶段未将所有的cve以及主机通过LLM进行分析

```python
cursor.execute("select id,json from cves where cve_id in ('CVE-2019-9510','CVE-2018-13807','CVE-2022-46141','CVE-2020-1560','CVE-2019-19300','CVE-2021-34527','CVE-2023-5178');")
```

源代码如上，从中可以看出我们只用了七个cve用作测试，后续大规模进行分析需要改动。如下

```python
cursor.execute("select id,json from cves;")
```
