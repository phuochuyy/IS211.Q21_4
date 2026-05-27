# Create database user for Surrealist UI on the local node.
# Run this once after SurrealDB container is running.

curl.exe -X POST -u "root:root" `
  -H "surreal-ns: ddbs" `
  -H "surreal-db: plant_paradise" `
  -H "Accept: application/json" `
  -d "DEFINE USER ui_admin ON DATABASE PASSWORD 'ui_admin_123' ROLES OWNER;" `
  http://127.0.0.1:8000/sql
