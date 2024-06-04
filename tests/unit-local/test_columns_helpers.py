import pytest
from chispa.dataframe_comparer import assert_df_equality
from pyspark.sql import SparkSession
from helpers.columns_helpers import add_missing_columns, columns_except, dataframe_except_columns

@pytest.fixture(scope="module")
def spark_session():
    return SparkSession.builder.getOrCreate()

def test_columns_except(spark_session):
    original_df = spark_session.createDataFrame(
        [[1, 2, 3, 4]], schema="col1 int, col2 int, col3 int, col4 int")
    new_cols = columns_except(original_df, ["col2", "col4"])
    assert new_cols == ["col1", "col3"]

def test_dataframe_except_columns(spark_session):
    original_df = spark_session.createDataFrame(
        [[1, 2, 3, 4]], schema="col1 int, col2 int, col3 int, col4 int")
    new_df = dataframe_except_columns(original_df, ["col2", "col4"])
    expected_df = spark_session.createDataFrame([[1, 3]], schema="col1 int, col3 int")
    assert_df_equality(new_df, expected_df, ignore_nullable=True)


def test_add_missing_columns(spark_session):
    df1 = spark_session.createDataFrame([[1, 2]], schema="col1 int, col2 int")
    df2 = spark_session.createDataFrame([[1, "2", 3.0]], schema="col1 int, col4 string, col5 double")
    new_df = add_missing_columns(df1, df2)
    expected_df = spark_session.createDataFrame([[1, 2, None, None]],
                                                schema="col1 int, col2 int, col4 string, col5 double")
    assert_df_equality(new_df, expected_df, ignore_nullable=True)
