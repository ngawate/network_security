from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
import sys

if __name__ == "__main__":
    try:
        train_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(train_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('Intiate Data Ingestion')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info('Data Initiation is completed')

        data_validation_config = DataValidationConfig(train_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info('Data Validation Initiate')
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info('Data Validation Completed')

        data_transformation_config = DataTransformationConfig(train_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info('Intiate Data Transformation')
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info('Data Transformation Completed')

    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(e, sys)