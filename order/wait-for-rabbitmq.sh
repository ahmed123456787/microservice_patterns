#!/bin/bash 
set -e

until rabbitmq-diagnostics ping; do
  >&2 echo "RabbitMQ is unavailable - sleeping"
  sleep 1
done
>&2 echo "RabbitMQ is up - executing command"
exec "$@"