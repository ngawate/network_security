import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.utils.main_utils.utils import load_numpy_array_data, save_object, load_object, evaluate_models
from networksecurity.entity.artifact_entity import ModelTrainerArtifact
from networksecurity.utils.ml_utils.metric.classification_mertric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
import mlflow

class ModelTrainer:

    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self, best_model, classfication_metric):
        with mlflow.start_run():
            f1_score = classfication_metric.f1_score
            precision_score = classfication_metric.precision_score
            recall_score = classfication_metric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            mlflow.sklearn.log_model(best_model, "model")
        
    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier()
            }

            params = {
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128]
                    },
                "Decision Tree": {
                    'criterion': ['gini', 'entropy', 'log_loss']
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85],
                    'n_estimators': [8, 16, 32, 64]
                },
                "Logistic Regression": {},
                "AdaBoost" : {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'n_estimators': [8, 16, 32, 64]
                }
            }

            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models, params)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            logging.info(f'Best Model Name -> {best_model_name}')
            logging.info(f'Best Model Score -> {best_model_score}')

            best_model = models[best_model_name]

            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            classfication_train_metric = get_classification_score(y_train, y_train_pred)
            classfication_test_metric = get_classification_score(y_test, y_test_pred)

            self.track_mlflow(best_model, classfication_train_metric)
            self.track_mlflow(best_model, classfication_test_metric)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)

            os.makedirs(model_dir_path, exist_ok=True)

            Network_Model = NetworkModel(preprocessor, best_model)

            save_object(self.model_trainer_config.trained_model_file_path, obj = Network_Model)
            
            save_object("final_model/model.pkl", best_model)

            model_trainer_artifact = ModelTrainerArtifact(self.model_trainer_config.trained_model_file_path, classfication_train_metric, classfication_test_metric)

            logging.info(model_trainer_artifact)

            return model_trainer_artifact

        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e, sys)
        
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],                
            )

            logging.info('Initiating Model Traininig')

            model_trainer_artifact = self.train_model(X_train, y_train, X_test, y_test)

            return model_trainer_artifact

        except Exception as e:
            logging.error(e)
            raise NetworkSecurityException(e, sys)
     