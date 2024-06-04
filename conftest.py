import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="module")
def spark_session():
    return SparkSession.builder.getOrCreate()