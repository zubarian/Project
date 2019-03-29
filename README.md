# ECS781P: CLOUD COMPUTING MINI PROJECT
I have made an app that gets the exchange rates for today using the base currency as USD.

BGN = Bulgarian lev
NZD = New Zealand dollar
CAD = Canadian dollar
CHF = Swiss franc
GBP = Pound sterling
EUR = Euro

And many more!

# Preparing for cluster deployment
gcloud config set project MY_PROJECT_ID
gcloud config set compute/zone us-central1-b

export PROJECT_ID="$(gcloud config get-value project -q)"
docker build -t gcr.io/${PROJECT_ID}/hello-app:v1 .

gcloud auth configure-docker
docker push gcr.io/${PROJECT_ID}/hello-app:v1

docker run --rm -p 8080:8080 gcr.io/${PROJECT_ID}/hello-app:v1

# Preparing a container cluster
gcloud container clusters create hello-cluster --num-nodes=3
gcloud compute instances list

# Deploying our application
kubectl run hello-web --image=gcr.io/${PROJECT_ID}/hello-app:v1 --port 8080

# Show pods
kubectl get pods

kubectl expose deployment hello-web --type=LoadBalancer --port 80 --target-port 8080
kubectl get service

# Scaling up our application
kubectl scale deployment hello-web --replicas=3
kubectl get deployment hello-web

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
