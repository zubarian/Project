# ECS781P: CLOUD COMPUTING MINI PROJECT
I have made an app that gets the exchage rates for today using the base currency as USD.

BGN = Bulgarian lev
NZD = New Zealand dollar
CAD = Canadian dollar
CHF = Swiss franc
GBP = Pound sterling
EUR = Euro

And many more!


# Show pods
kubectl get pods



# Creating a table in Cassandra 

Use the following commands:

gcloud config set compute/zone europe-west2-b
export PROJECT_ID="$(gcloud config get-value project -q)"
docker pull cassandra:latest
docker run --name cassandra-test -d cassandra:latest

docker cp rates.csv cassandra-test:/home/rates.csv

kubectl exec -it cassandra-btktq cqlsh

CREATE KEYSPACE pokemon WITH REPLICATION =
{'class' : 'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE exchangerates.stats (base text,
rates text PRIMARY KEY, date text);

COPY exchangerates.stats(base,rates,date) FROM 'rates.csv' WITH DELIMITER=',' AND HEADER=TRUE;

#  scale up number of nodes via our replication-controller
kubectl scale rc cassandra --replicas=3

# check that the ring has been formed between all of the Cassandra instances
kubectl exec -it cassandra-btktq nodetool status
