python manage.py dumpdata accounts.MyRoles --indent 2 > role.json
python manage.py loaddata entm/fixtures/organization_init.json


# service postgresql-9.6 restart

create user scada with password 'scada';

create database waterwork;

grant all privileges on database waterwork to scada;


--------------------------------
install postgis 
#postgis
yum install binutils

1.Installing Geospatial libraries
./configure
make
make install


Program Description Required    Supported Versions
GEOS    Geometry Engine Open Source Yes 3.6, 3.5, 3.4
PROJ.4  Cartographic Projections library    Yes (PostgreSQL and SQLite only)    4.9, 4.8, 4.7, 4.6, 4.5, 4.4
GDAL    Geospatial Data Abstraction Library Yes 2.2, 2.1, 2.0, 1.11, 1.10, 1.9
GeoIP   IP-based geolocation library    No  2
PostGIS Spatial extensions for PostgreSQL   Yes (PostgreSQL only)   2.4, 2.3, 2.2, 2.1
SpatiaLite  Spatial extensions for SQLite   Yes (SQLite only)   4.3, 4.2, 4.1, 4.0
wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2


ref:https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/geolibs/




wget ftp://xmlsoft.org/libxml2/libxml2-git-snapshot.tar.gz

#configure postgis-2.4.4
./configure --with-pgconfig=/usr/pgsql-9.6/bin/pg_config --with-gdalconfig=/usr/local/bin/gdal-config --with-geosconfig=/usr/local/bin/geos-config --with-xml2config=/usr/local/libxml2-2.9.7/bin/xml2-config 

#威尔沃阿里云配置postgis安装
./configure --with-pgconfig=/usr/pgsql-9.6/bin/pg_config --with-gdalconfig=/usr/local/gdal-1.11.2/bin/gdal-config --with-geosconfig=/usr/local/geos-3.4.2/bin/geos-config --with-xml2config=/usr/local/libxml2-2.9.7/bin/xml2-config --with-projdir=/usr/local/proj-4.9.1/


postgres=# CREATE EXTENSION postgis;
ERROR:  could not load library "/usr/pgsql-9.6/lib/postgis-2.4.so": libgeos_c.so.1: cannot open shared object file: No such file or directory

resolred:  Setting system library path
$ sudo echo /usr/local/lib >> /etc/ld.so.conf
echo /usr/local/geos-3.4.2/lib/ >> /etc/ld.so.conf
echo /usr/local/proj-4.9.1/lib/ >> /etc/ld.so.conf
echo /usr/local/gdal-1.11.2/lib/ >> /etc/ld.so.conf
$ sudo ldconfig


File "/opt/app/Virvo/venv/lib/python3.6/site-packages/django/contrib/gis/db/backends/postgis/base.py", line 26, in prepare_database
    cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")

cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
change into 
try:
    cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
except:
    pass




apache virtualhost



LoadModule wsgi_module "c:/users/hp/envs/djproject/lib/site-packages/mod_wsgi/server/mod_wsgi.pyd"
WSGIPythonHome "c:/users/hp/envs/djproject"

#Django项目的路径
WSGIPythonPath D:/pengwl/webapp/waterwork


NameVirtualHost *:8099

<VirtualHost *:8099>
    #ServerAdmin admin@bsc2000.com
    ServerName bsc2000.com
    ServerAlias bsc2000

    
    #WSGIPythonHome "c:/users/hp/envs/djproject"


    #Django项目中wsgi.py的路径
    WSGIScriptAlias / D:/pengwl/webapp/waterwork/waterwork/wsgi.py



    #配置wsgi.py的访问权限
    <Directory D:/pengwl/webapp/waterwork/waterwork >
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    #Alias /robots.txt /path/to/waterwork/static/robots.txt
    #Alias /favicon.ico /path/to/myproject/static/favicon.ico

    Alias /media/ D:/pengwl/webapp/waterwork/media/
    Alias /static/ D:/pengwl/webapp/waterwork/static/
    <Directory D:/pengwl/webapp/waterwork/static>
        Require all granted
        Order deny,allow
        Allow from all
    </Directory>

    <Directory D:/pengwl/webapp/waterwork/media>
        Require all granted
        Order deny,allow
        Allow from all
    </Directory>

    #WSGIDaemonProcess www.myproject.com display-name=myproject user=myuser group=myuser processes=2 threads=15
    #WSGIDaemonProcess django processes=2 threads=12 python-path=c:/users/hp/envs/djproject

   
    #WSGIProcessGroup www.myproject.com
    ErrorLog "D:/pengwl/webapp/waterwork/apache_logs/error_log
    CustomLog "D:/pengwl/webapp/waterwork/apache_logs/access_log" common
</VirtualHost>
create database waterwork character set utf8mb4 collate utf8mb4_general_ci;



pip install virtualenvwrapper-win
mkvirtualenv djproject

mod_wsgi-express module-config 




q=HdbFlowData.day_hourly.search('064811210390','2018-09-24')

from legacy.models import HdbFlowData


treeDemo 
    organization
        "name":o.name,
        "id":o.cid,
        "pId":o.pId,
        "districtid":'',
        "type":"group",
    dma
        "name":d["dma_name"],
        "id":d["pk"],
        "districtid":d["pk"],
        "pId":o.cid,
        "type":"dma",
    station
        "name":s['username'],
        "id":s['pk'],
        "districtid":'',
        "pId":o.cid,
        "type":"station",
        "dma_no":'',

        "commaddr":commaddr,