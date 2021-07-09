FROM cassandra:latest

COPY ./scripts/entry-point.sh /entry-point.sh
COPY ./scripts/keyspace.cql /scripts/keyspace.cql

ENTRYPOINT ["/entry-point.sh"]

CMD ["cassandra", "-f"]