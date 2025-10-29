#!/bin/bash
# Warten, bis Postgres erreichbar ist

set -e

host="db"
port="5432"

echo "⏳ Waiting for Postgres ($host:$port)..."

while ! nc -z $host $port; do
  sleep 1
done

echo "✅ Postgres is up - executing command"
exec "$@"
