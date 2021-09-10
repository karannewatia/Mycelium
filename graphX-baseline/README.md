### How to run graphX baseline

1. Run `sbt package`
2. Run `$SPARK_DIR/bin/spark-submit --class "AggregateMessagesExample" --master local[4] target/scala-2.12/simple-project_2.12-1.0.jar`