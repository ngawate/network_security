from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
        train_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(train_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('Intiate Data Ingestion')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(e, sys)