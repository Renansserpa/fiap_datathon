import os
from typing import Any

import pandas as pd
from data_pipeline.model import predict_model, prepare_for_predict, train
from fastapi import APIRouter, Body, HTTPException

router = APIRouter(
    prefix="/ml",
    tags=["ml"]
)

# Lista de colunas esperadas para a vaga
VAGA_COLUMNS = [
    'id_vaga', 'data_requicisao', 'limite_esperado_para_contratacao',
    'titulo_vaga', 'vaga_sap', 'cliente', 'solicitante_cliente',
    'empresa_divisao', 'requisitante', 'analista_responsavel',
    'tipo_contratacao', 'prazo_contratacao', 'objetivo_vaga',
    'prioridade_vaga', 'origem_vaga', 'superior_imediato', 'nome',
    'telefone', 'pais', 'estado', 'cidade', 'bairro', 'regiao',
    'local_trabalho', 'vaga_especifica_para_pcd', 'faixa_etaria',
    'horario_trabalho', 'nivel profissional', 'nivel_academico',
    'nivel_ingles', 'nivel_espanhol', 'outro_idioma', 'areas_atuacao',
    'principais_atividades', 'competencia_tecnicas_e_comportamentais',
    'demais_observacoes', 'viagens_requeridas', 'equipamentos_necessarios',
    'valor_venda', 'valor_compra_1', 'valor_compra_2', 'data_inicial',
    'data_final', 'habilidades_comportamentais_necessarias',
    'nome_substituto', 'categoria_contratacao'
]


@router.post("/train")
def train_endpoint():
    """
    Treina o modelo usando o Parquet em app/parquet/ e config.yml.
    """
    try:
        base_path = os.path.dirname(__file__)
        config_path = os.path.join(base_path, "config.yml")

        from omegaconf import OmegaConf
        conf = OmegaConf.load(config_path)

        train(conf.parameters)
        return {"status": "training completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict")
def predict_endpoint(vaga: dict[str, Any] = Body(...)):
    """
    Recebe um JSON com chaves iguais às colunas de vagas e retorna previsão única.
    """
    # Validação de colunas
    missing = set(VAGA_COLUMNS) - vaga.keys()
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Chaves ausentes no JSON: {sorted(missing)}"
        )

    # Cria DataFrame com uma única linha da vaga
    df_input = pd.DataFrame([vaga])

    try:
        df_input = prepare_for_predict(df_input)
        preds = predict_model(df_input)
        return {"predictions": preds}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))