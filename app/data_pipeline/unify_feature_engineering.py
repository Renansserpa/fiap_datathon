import re

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import (
    MaxAbsScaler,
    MinMaxScaler,
    RobustScaler,
    StandardScaler,
)


def data_unify(applicants, prospects, vagas):

    applicants = applicants.add_prefix("applicants_")
    prospects = prospects.add_prefix("prospects_")
    vagas = vagas.add_prefix("vagas_")

    united_data = pd.merge(
        prospects,
        vagas,
        left_on="prospects_vaga_id",
        right_on="vagas_id_vaga",
        how="inner"
    )

    united_data = pd.merge(
        united_data,
        applicants,
        left_on="prospects_codigo",
        right_on="applicants_infos_basicas_codigo_profissional",
        how="inner"
    )

    united_data = united_data[united_data['prospects_situacao_candidado'].isin([
        "Não Aprovado pelo Cliente",
        "Contratado pela Decision",
        "Não Aprovado pelo RH",
        "Não Aprovado pelo Requisitante",
        "Sem interesse nesta vaga",
        "Contratado como Hunting",
        "Aprovado",
        "Recusado",
        "Proposta Aceita"
        ])
    ]

    mapa_target = {
                'Não Aprovado pelo Cliente': 0,
                'Contratado pela Decision': 1,
                'Não Aprovado pelo RH': 0,
                'Não Aprovado pelo Requisitante': 0,
                'Sem interesse nesta vaga': 0,
                'Contratado como Hunting': 1,
                'Aprovado': 1,
                'Recusado': 0,
                'Proposta Aceita': 1
            }

    # Aplicar o mapeamento em novas colunas
    united_data['prospects_situacao_candidado'] = united_data['prospects_situacao_candidado'].map(mapa_target)
    united_data = united_data.rename(columns={'prospects_situacao_candidado': 'target'})
    united_data = united_data.set_index('applicants_id_applicants')

    return united_data


class vagas_features_engineering:

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa a classe com um DataFrame.

        :param df: DataFrame contendo os dados das vagas.
        """
        self.df = df.copy()
        self.input_column_names = df.columns

    def titulo_vaga(self) -> None:
        """Descrição aqui"""

        mapa_palavras_chave_titulo = {
            'key_SAP': r'SAP',
            'key_SD': r'\bSD\b',
            'key_MM': r'\bMM\b',
            'key_ABAP': r'\bABAP\b',
            'key_AMS': r'AMS',
            'key_JAVA': r'java',
            'key_ORACLE': r'oracle',
            'key_CLOUD': r'cloud|AWS|Azure',
            'key_EBS': r'\bEBS\b',
            'key_DBA': r'\bDBA\b',
            'key_PROXXI': r'\bPROXXI\b',
            'key_C_HASH': r'C#',
            'key_OPERATIONS': r'Operations|Operações',
            'key_PMO': r'\bPMO\b|projetos',
            'key_ADM': r'\b(Adm|Administ|Administrativo|Administrador)\b',
            'key_MARKETING': r'market',
            'key_TI': r'\bTI\b',
            'key_SALESFORCE': r'Salesforce',
            'key_PROJETOS': r'Projetos',
            'key_DADOS': r'Dados|Data',
            'key_SECURITY': r'\b(Segurança|Security|Cyber)\b',
            'key_WEB': r'\bWeb\b',
            'key_SCRUM': r'\bScrum\b',
            'key_SERVICE': r'Service',
            'key_REACT_NATIVE_ANGULAR': r'\b(react|native|angular)',
            'key_NET': r'.Net',
            'key_Analista': r'Analista|Analyst',
            'key_DEVOPS': r'devops',
            'key_PYTHON': r'\bpython\b',
            'key_C_PLUS_PLUS': r'C\+\+',
            'key_COBOL': r'Cobol',
            'key_ANDROID': r'Android',
            'key_SQL': r'SQL',
            'key_fiscal': r'fiscal|contábil|contabilidade',
            'key_software': r'Software|Front|FullStack|back'
        }

        # Criação de colunas binárias que informam palavras chave ou não
        for coluna, regex_pattern in mapa_palavras_chave_titulo.items():
            self.df[coluna] = self.df['prospects_titulo'].str.contains(regex_pattern, regex=True, case=False).astype(int)

    @staticmethod
    def map_nivel(titulo: str) -> str:
        niveis_dict = {
            "Estágio/Trainee": r"estagi|trainee",
            "Assistente": r"assistente",
            "Júnior": r"junior|\bjr\b",
            "Pleno": r"pleno|\bpl\b",
            "Sênior": r"senior|\bsr\b|sênior|\bsn\b",
            "Coordenação": r"coordenador|líder",
            "Gerência": r"gerente|manager",
            "Diretoria": r"diretor"
        }

        for nivel, padrao in niveis_dict.items():
            if re.search(padrao, titulo):
                return nivel

        return "Outros"

    def nivel_vaga(self) -> None:
        """Descrição aqui"""

        mapeamento_numerico = {
            "Outros": 0,
            "Estágio/Trainee": 0,
            "Assistente": 1,
            "Júnior": 2,
            "Pleno": 3,
            "Sênior": 4,
            "Coordenação": 5,
            "Gerência": 6,
            "Diretoria": 7
        }

        self.df['nivel_vaga'] = self.df['prospects_titulo'].apply(self.map_nivel)
        self.df['nivel_vaga'] = self.df['nivel_vaga'].map(mapeamento_numerico)

    def tipo_contratacao(self) -> None:
        """Descrição aqui"""

        mapa_palavras_chave_tipo = {
            'tipo_escolha_do_candidato': r'candidato poderá escolher',
            'tipo_CLT': r'clt',
            'tipo_PJ': r'pj',
            'tipo_cooperado': r'cooperado',
            'tipo_estagio': r'estagiário',
            'tipo_hunting': r'hunting',
            'tipo_misto': r'^.*[,]|(?=.*\bclt\b)(?=.*\bpj\b)(?=.*\bcooperado\b)(?=.*\bestagiário\b)(?=.*\bhunting\b).*',
        }

        # Criação de colunas binárias que informam palavras chave ou não
        for coluna, regex_pattern in mapa_palavras_chave_tipo.items():
            self.df[coluna] = self.df['vagas_tipo_contratacao'].str.contains(regex_pattern, regex=True, case=False).astype(int)

    def linguas_vaga(self) -> None:
        """Descrição aqui"""

        mapa_linguas = {
            'Nenhum': 0,
            'Básico': 1,
            'Intermediário': 2,
            'Avançado': 3,
            'Técnico': 3,
            'Fluente': 4
        }

        # Aplicar o mapeamento em novas colunas
        self.df['score_ingles'] = self.df['vagas_nivel_ingles'].map(mapa_linguas)
        self.df['score_espanhol'] = self.df['vagas_nivel_espanhol'].map(mapa_linguas).fillna(int(0))

    def create_all(self) -> pd.DataFrame:

        self.titulo_vaga()
        self.nivel_vaga()
        self.tipo_contratacao()
        self.linguas_vaga()

        return self.df.drop(columns=self.input_column_names, errors='ignore')


def applicants_features_engineering(df: pd.DataFrame, description_column: str) -> pd.DataFrame:

    text_series = df[description_column]
    # Using a smaller model suitable for Portuguese
    model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2')
    embeddings = model.encode(text_series.tolist())

    # Create a DataFrame from the embeddings
    embedding_df = pd.DataFrame(embeddings, columns=[f'embedd_{i}' for i in range(1, 512 + 1)], index=df.index)

    return embedding_df


def normalize_dataframe(df, method='minmax'):

    # Escolhe o scaler com base no método
    if method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'standard':
        scaler = StandardScaler()
    elif method == 'robust':
        scaler = RobustScaler()
    elif method == 'maxabs':
        scaler = MaxAbsScaler()
    else:
        raise ValueError("Método inválido. Escolha entre: 'minmax', 'standard', 'robust', 'maxabs'.")

    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)