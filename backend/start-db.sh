#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting Docker Compose services..."
docker-compose up -d

echo -e "\n📊 Waiting for PostgreSQL to be ready..."
until docker exec eckho_db pg_isready -U eckho_user -d eckho_wfm >/dev/null 2>&1; do
    sleep 1
done

echo -e "\n✅ Database is ready!"
echo -e "\n🔗 PostgreSQL Connection Info:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  Database: eckho WFM"
echo "  Username: eckho_user"
echo "  Password: eckho_password"

echo -e "\n🌐 pgAdmin is available at: http://localhost:5050"
echo "  Email: admin@eckho.com"
echo "  Password: admin123"

echo -e "\n🛑 To stop the services, run: docker-compose down"
