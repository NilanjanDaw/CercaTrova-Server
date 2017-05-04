# CercaTrova
Design Lab project
- Server side code repository

## Important Links
- [Server Repository](https://github.com/NilanjanDaw/CercaTrova-Server)
- [Emergency User Application Repository](https://github.com/NilanjanDaw/CercaTrova-Client)
- [Emergency Personnel Application Repository](https://github.com/NilanjanDaw/CercaTrova-Personnel)
- [CercaTrova Documentation](https://github.com/NilanjanDaw/CercaTrova-Documentation)

## Setup Instructions
Please follow the following Setup Instructions carefully to create the main Server
- Download and install PostgreSQL EnterpriseDB v9.6.2 (.exe for Windows/ .run for Linux)
```bash
$ cd <folder_location>/
$ chmod 755 <file_name>.run
$ sudo ./<file_name>.run
```
- Install PostGIS  v2.3.2 using stackbuilder bundled with above installer.Select spatial extension and run the rest of the wizard.
- (Windows Only) Download and install OSgeo4W.
- (Linux Only) Install GDAL
```bash
sudo apt-get install libgdal-dev
```
- Start psql command prompt. Create a new database named cerca_trova and a new user named admin with password 'admin' and grant all rights to database cerca_trova.

```sql
create user admin with password ‘admin’;
create database cerca_trova;
grant all privileges on database cerca_trova to admin;
```
- Login to new database with new user credentials and enable PostGIS extension. Be careful not to enable PostGIS in postgres database. Some of the extensions might fail dont worry.

```sql
-- Enable PostGIS (includes raster)
CREATE EXTENSION postgis;
-- Enable Topology
CREATE EXTENSION postgis_topology;
-- Enable PostGIS Advanced 3D
-- and other geoprocessing algorithms
CREATE EXTENSION postgis_sfcgal;
-- fuzzy matching needed for Tiger
CREATE EXTENSION fuzzystrmatch;
-- rule based standardizer
CREATE EXTENSION address_standardizer;
-- example rule data set
CREATE EXTENSION address_standardizer_data_us;
-- Enable US Tiger Geocoder
CREATE EXTENSION postgis_tiger_geocoder;
-- routing functionality
CREATE EXTENSION pgrouting;
-- spatial foreign data wrappers
CREATE EXTENSION ogr_fdw;

-- LIDAR support
CREATE EXTENSION pointcloud;
-- LIDAR Point cloud patches to geometry type cases
CREATE EXTENSION pointcloud_postgis;
```
- Install virtualenv
```bash
$ pip install virtualenv
```
- create project folder
```bash
$ cd <location>
$ mkdir <folder_name>
```
- cd to folder and create and enable python virtualenv
```bash
$ virtualenv <folder_name> 
$ source /bin/activate
```
- Pull the project repository from remote server
```
$ git pull https://github.com/NilanjanDaw/CercaTrova-Server.git
```
- Install dependencies
```bash
$ pip install -r requirements.txt
```
- cd to cerca_trova folder within repository. Add host URL to allowed in "settings.py"
```python
ALLOWED_HOSTS = [
  ...,
  <HOST_URL>,
]
```
- cd to repository root folder. Migrate databases and start Server
```bash
$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:8000
```
