name := "Simple Project"

version := "1.0"

scalaVersion := "2.12.10"

libraryDependencies ++= Seq(
	"org.apache.spark" %% "spark-sql" % "3.1.2",
	"org.apache.spark" %% "spark-graphx" % "3.1.2"
)
