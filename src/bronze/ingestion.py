"""
Bronze Layer - Ingesta de eventos en tiempo real
Append only, datos crudos con metadata de ingesta
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType
from typing import Dict
import json

def write_bronze(df: DataFrame, table_name: str) -> None:
    """
    Escribe un batch de eventos a Bronze con metadata de ingesta

    Args:
    df: DataFrame con eventos crudos
    table_name: nombre de la tabla destino
    """

    (
        df
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_pipeline_version", F.lit("1.0.0"))
        .write
        .format("delta")
        .mode("append")
        .option("mergeSchema", "true")
        .saveAsTable(f"bronze_{table_name}")
    )

def ingest_batch(eventos: Dict[str, list], spark: SparkSession) -> Dict[str, int]:
    """
    Ingesta un batch de eventos de las 3 fuentes a Bronze.

    Args:
    eventos: Diccionario con los eventos de las 3 fuentes
    spark: SparkSession
    Returns:    
    Diccionario con el número de eventos ingestados por fuente
    """

    resultados = {}

    if eventos.get("pagos"):
        df_pagos = spark.createDataFrame(eventos["pagos"])
        write_bronze(df_pagos, "pagos")
        resultados["compras"] = len(eventos["compras"])

    if eventos.get("pagos"):
        df_pagos = spark.createDataFrame(eventos["pagos"])
        write_bronze(df_pagos, "pagos")
        resultados["pagos"] = len(eventos["pagos"])

    if eventos.get("inventario"):
        df_inventario = spark.createDataFrame(eventos["inventario"])
        write_bronze(df_inventario, "inventario")
        resultados["inventario"] = len(eventos["inventario"])

    return resultados



