from pyspark.sql import SparkSession
import os

# AWS credentials can be pulled from env or IAM role on EMR/EC2
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize SparkSession with S3 support
spark = SparkSession.builder \
    .appName("Spark to S3 Example") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Create a sample DataFrame
data = [("Alice", 30), ("Bob", 28), ("Catherine", 35)]
columns = ["name", "age"]
df = spark.createDataFrame(data, columns)

# S3 output path (example)
output_path = "s3a://your-bucket-name/spark-output/sample-data"

# Write DataFrame to S3 in Parquet format
df.write.mode("overwrite").parquet(output_path)

print("Data successfully written to S3.")

spark.stop()
