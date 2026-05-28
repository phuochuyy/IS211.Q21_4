# Local test
curl.exe -X POST -u "root:root" -H "surreal-ns: ddbs" -H "surreal-db: plant_paradise" -H "Accept: application/json" -d "RETURN 'Local SurrealDB is running';" http://127.0.0.1:8000/sql

# CN1 -> test
curl.exe -X POST -u "root:root" -H "surreal-ns: ddbs" -H "surreal-db: plant_paradise" -H "Accept: application/json" -d "RETURN 'Connected to CN1';" http://26.41.51.255:8000/sql

# CN2 -> test
curl.exe -X POST -u "root:root" -H "surreal-ns: ddbs" -H "surreal-db: plant_paradise" -H "Accept: application/json" -d "RETURN 'Connected to CN2';" http://26.201.116.10:8000/sql

# CN3 -> test
curl.exe -X POST -u "root:root" -H "surreal-ns: ddbs" -H "surreal-db: plant_paradise" -H "Accept: application/json" -d "RETURN 'Connected to CN3';" http://26.105.5.3:8000/sql
