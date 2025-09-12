import os
import sys
from networksecurity.entity.artifact_entity import ClassificationMertricArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(y_true, y_pred) -> ClassificationMertricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        classfication_metric = ClassificationMertricArtifact(
            f1_score = model_f1_score,
            precision_score = model_precision_score,
            recall_score = model_recall_score
        )

        return classfication_metric
    
    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(e, sys)