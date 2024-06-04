
This repository is based on https://github.com/alexott/dlt-files-in-repos-demo and used to demonstrate running tests locally and against a remote Databricks environment

It's not productionised code and just used for demonstration purposes. 

# Setup instructions

1. Install JDK 11 locally (e.g. brew install openjdk@11)
1. Make sure java has been added to your path (see instructions when installing via homebrew)
1. Download and extract Spark locally: https://spark.apache.org/downloads.html
1. Run from terminal:

   `cd <extracted spark directory>`

   `./sbin/start-connect-server.sh --packages org.apache.spark:spark-connect_2.12:3.5.1` : This will start Spark running locally

   Optional: `tail -f <<fill in log name from console>>` : This will keep track of the logs coming from spark

1. Install poetry for Python package management (e.g. `brew install poetry`)
1. Download dependecies: `poetry init`

# Running unit tests
Unit test run against the local version of spark that has been set up above.
Note: unit tests shouldn't attempt to read from tables, isolate that code separately and test with integration test.

Run from terminal: `export SPARK_REMOTE="sc://localhost" && poetry run pytest tests/unit-local --junit-xml=test-local.xml --cov`

These can also be run/debugged from your IDE with 'Pytest Runner for Visual Studio Code' extension

# Running integration tests against a remote spark cluster
Integration tests run against a remote Databricks cluster and use Spark Connect rather than DB connect

1. Generate a personal access token in databricks: https://docs.databricks.com/en/dev-tools/auth/pat.html#databricks-personal-access-tokens-for-workspace-users
1. Get the cluster id for your Databricks cluster, e.g. go to Databricks UI -> Compute -> click on your cluster -> get id from url. If URL is https://myworkspace.databricks.com/compute/clusters/1601-182128-dcbte51m?o=1444828305810485 , the cluster id is 1601-182128-dcbte51m
1. Set access token as an environment variable, run this from terminal: `export DATABRICKS_TOKEN=<<your personal access token>>`
1. To run tests: `export SPARK_REMOTE="sc://my-databricks-workspace.databricks.com:443/;token=$DATABRICKS_TOKEN;x-databricks-cluster-id=<<your cluster id>>" && poetry run pytest tests/integration --junit-xml=test-local.xml --cov`

These can also be run/debugged from your IDE with 'Pytest Runner for Visual Studio Code' extension

# Notes on using Spark Connect
- Had issues with dbconnect library not being compatible with pyspark library, which meant it's difficult to run unit-tests locally. To work around this, using Spark Connect instead of DB Connect. See https://docs.databricks.com/en/dev-tools/databricks-connect/python/troubleshooting.html#conflicting-pyspark-installations
- Need to be using at least 3.4 version of pypark to be able to use Spark Connect (e.g. 3.5.1 used here). More details: https://spark.apache.org/docs/latest/spark-connect-overview.html
- Need the extra Spark Connect dependencies that aren't included in pyspark by default. See https://spark.apache.org/docs/latest/api/python/getting_started/install.html
      To get poetry to work with this, needed to add them explicitly:

      py4j = "^0.10.9.7"
      pandas = "^1.0.5"
      pyarrow = "^16.1.0"
      numpy = "^1.15"
      grpcio = "^1.48"
      grpcio-status = "^1.48"
      googleapis-common-protos="^1.56.4"

