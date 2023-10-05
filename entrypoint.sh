#!/bin/sh

# Function to check PostgreSQL availability
wait_for_postgres() {
    echo "Waiting for PostgreSQL..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
}

# Check if the database is PostgreSQL
if [ "$DATABASE" = "postgres" ]
then
    wait_for_postgres
fi

# Run Alembic migrations
alembic upgrade head

# You can add other commands here as needed

exec "$@"