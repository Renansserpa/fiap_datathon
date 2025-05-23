# %%
import os

import mlflow
import pandas as pd
from data_pipeline.data_cleaning import (
    CleanApplicants,
    CleanProspects,
    CleanVagas,
)
from data_pipeline.data_loading import DataLoader
from data_pipeline.unify_feature_engineering import (
    data_unify,
    normalize_dataframe,
    vagas_features_engineering,
)
from omegaconf import OmegaConf
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# Caminho do script
file_path = os.path.dirname(__file__)

# Leitura do arquivo de configuração (parâmetros do modelo)
conf = OmegaConf.load(os.path.join(file_path, "config.yml"))

# Configuração do nome do experimento via MLFlow
mlflow.set_experiment("fiap-datathon-exp")


# Função de treinamento
def train(params):

    loader = DataLoader(file_path)
    prospects = loader.load_prospects("prospects.json")
    vagas = loader.load_vagas("vagas.json")
    aplicants = loader.load_applicants("applicants.json")

    prospects = CleanProspects(prospects).clean_all()
    vagas = CleanVagas(vagas).clean_all()
    aplicants = CleanApplicants(aplicants).clean_all()

    df_unido = data_unify(aplicants, prospects, vagas)

    df_unido_gerado = vagas_features_engineering(df_unido).create_all()

    df_embedding = pd.read_parquet(os.path.join(file_path, 'applicants_embeddings.parquet'))

    df = pd.concat([df_unido_gerado,
                    df_embedding,
                    df_unido['target']], axis=1
    )

    with mlflow.start_run():
        # Obtenção de features
        features = df.columns.to_list()[1:-1]
        target = df.columns.to_list()[-1]

        # Separação de conjunto de treinamento e de testes
        df_train, df_test = train_test_split(df, test_size=0.3, random_state=23)

        # Treinamento do modelo
        mlflow.log_params(params)
        clf = XGBClassifier(**params)
        clf.fit(df_train[features], df_train[target])

        # Registro do modelo no MLFlow
        signature = mlflow.models.infer_signature(df_train[features], clf.predict(df_train[features]))
        mlflow.sklearn.log_model(
            sk_model=clf,
            artifact_path="sklearn-model",
            signature=signature,
            input_example=df_train[features].iloc[:2],
            registered_model_name="xgboost-fiap-datathon-model",
        )

        # Cálculo de F1 Score
        y_train_pred_class = clf.predict(df_train[features])
        y_test_pred_class = clf.predict(df_test[features])
        f1_score_train_weighted = f1_score(df_train[target], y_train_pred_class, average='weighted')
        f1_score_test_weighted = f1_score(df_test[target], y_test_pred_class, average='weighted')

        # Log metric via MLFlow
        mlflow.log_metric("f1_score_train_weighted", f1_score_train_weighted)
        mlflow.log_metric("f1_score_test_weighted", f1_score_test_weighted)

        # Apresentação de resultados no terminal
        print(f"f1_score_train_weighted: {f1_score_train_weighted}")
        print(f"f1_score_test_weighted:  {f1_score_test_weighted }")


def prepare_for_predict(vaga_informada: pd.DataFrame):

    df_embedding = pd.read_parquet(os.path.join(file_path, 'applicants_embeddings.parquet'))
    vaga_limpa = CleanVagas(vaga_informada)\
                    .clean_all()\
                    .add_prefix("vagas_")\
                    .rename(columns={'vagas_titulo_vaga': 'prospects_titulo'})

    vaga_com_features = vagas_features_engineering(vaga_limpa).create_all()

    vaga_normalizada = normalize_dataframe(vaga_com_features)

    df_vaga_replicada = pd.concat([vaga_normalizada] * df_embedding.shape[0], ignore_index=True)

    return pd.concat([df_vaga_replicada.reset_index(drop=True), df_embedding.reset_index(drop=True)], axis=1)


# Função destinada à predição
def predict_model(df):
    """
    Faz previsões usando o modelo treinado.
    """

    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    model_name = "xgboost-fiap-datathon-model"

    client = mlflow.client.MlflowClient()
    version = max((int(i.version) for i in client.get_latest_versions("xgboost-fiap-datathon-model")))
    model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{version}")

    df['probabilidade_aprovacao'] = model.predict_proba(df)
    return df.sort_values(by='probabilidade_aprovacao', ascending=False).head(10).to_list()