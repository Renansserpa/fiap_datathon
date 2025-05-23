
import pandas as pd


class CleanApplicants:
    """Classe para realizar a limpeza e conversão de tipos no DataFrame de aplicantes."""

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa a classe com um DataFrame.

        :param df: DataFrame contendo os dados dos aplicantes.
        """
        self.df = df.copy()

        # Colunas que devem ser tratadas como tipo texto
        self.colunas_str = [
            "telefone_recado", "telefone", "infos_basicas_objetivo_profissional",
            "infos_basicas_inserido_por", "infos_basicas_email", "infos_basicas_local",
            "infos_basicas_sabendo_de_nos_por", "infos_basicas_nome", "data_aceite",
            "nome", "cpf", "fonte_indicacao",
            "email", "email_secundario", "telefone_celular",
            "sexo", "estado_civil", "pcd",
            "endereco", "skype", "url_linkedin",
            "facebook", "titulo_profissional", "area_atuacao",
            "conhecimentos_tecnicos", "certificacoes", "outras_certificacoes",
            "nivel_profissional", "nivel_academico", "nivel_ingles",
            "nivel_espanhol", "outro_idioma", "instituicao_ensino_superior",
            "cursos", "download_cv", "qualificacoes",
            "experiencias", "outro_curso", "email_corporativo",
            "cargo_atual", "projeto_atual", "cliente",
            "unidade", "nome_superior_imediato", "email_superior_imediato",
            "cv_pt", "cv_en"
        ]

        # Colunas que devem ser tratadas como tipo data
        self.colunas_data = [
            "infos_basicas_data_criacao", "infos_basicas_data_atualizacao", "data_nascimento",
            "data_admissao", "data_ultima_promocao"
        ]

        # Colunas que devem ser tratadas como tipo inteiro
        self.colunas_int = [
            "infos_basicas_codigo_profissional", "id_applicants", "id_ibrati"
        ]

    def clean_remuneracao(self) -> None:
        """Limpa e converte a coluna 'remuneracao' para float."""
        self.df["remuneracao"] = (
            self.df["remuneracao"]
            .astype(str)
            .str.lower()
            .str.extract(r"mensal\s*/\s*([\d.,]+)", expand=False)  # Captura o número após 'mensal /'
            .fillna("0")  # Se não encontrar, substitui por 0
            .str.replace(".", "", regex=False)  # Remove pontos
            .str.replace(",", ".", regex=False)  # Substitui vírgula por ponto
            .astype(float)
        )

    def convert_to_string(self) -> None:
        """Converte as colunas especificadas para string."""
        for col in self.colunas_str:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str)

    def convert_to_datetime(self) -> None:
        """Converte as colunas especificadas para datetime."""
        for col in self.colunas_data:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce", dayfirst=True)

    def convert_to_int(self) -> None:
        """Converte as colunas especificadas para int."""
        for col in self.colunas_int:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").fillna(0).astype(int)

    def clean_all(self) -> pd.DataFrame:
        """Executa todas as funções de limpeza."""
        self.clean_remuneracao()
        self.convert_to_string()
        # self.convert_to_datetime()
        self.convert_to_int()

        return self.df


class CleanVagas:
    """Classe para realizar a limpeza e conversão de tipos no DataFrame de vagas."""

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa a classe com um DataFrame.

        :param df: DataFrame contendo os dados das vagas.
        """
        self.df = df.copy()

        # Colunas que devem ser tratadas como tipo texto
        self.colunas_string = [
            'titulo_vaga', 'vaga_sap', 'cliente', 'solicitante_cliente',
            'empresa_divisao', 'requisitante', 'analista_responsavel',
            'tipo_contratacao', 'prazo_contratacao', 'objetivo_vaga',
            'prioridade_vaga', 'origem_vaga', 'superior_imediato',
            'nome', 'telefone', 'pais', 'estado', 'cidade', 'bairro',
            'regiao', 'local_trabalho', 'vaga_especifica_para_pcd',
            'faixa_etaria', 'horario_trabalho', 'nivel profissional', 'nivel_academico',
            'nivel_ingles', 'nivel_espanhol', 'outro_idioma', 'areas_atuacao',
            'principais_atividades', 'competencia_tecnicas_e_comportamentais',
            'demais_observacoes', 'viagens_requeridas', 'equipamentos_necessarios',
            'valor_compra_1', 'valor_compra_2', 'habilidades_comportamentais_necessarias',
            'nome_substituto'
        ]

        # Colunas que devem ser tratadas como tipo data
        self.colunas_data = [
            'data_requicisao', 'limite_esperado_para_contratacao',
            'data_inicial', 'data_final'
        ]

        # Colunas que devem ser tratadas como tipo data
        self.colunas_int = [
            'id_vaga'
        ]

    @staticmethod
    def limpar_valor(valor: str) -> float:
        """Limpa e converte valores monetários para float."""
        valor = str(valor).strip()
        if valor == '-' or 'p/ mês' in valor or '(' in valor or valor.count('.') > 1:
            return 0.0

        # Remove caracteres indesejados e converte para formato numérico válido
        valor = (
            valor.replace("R$", "")
            .replace(".", "")  # Remove pontos de milhar
            .replace(",", ".")  # Substitui vírgula decimal por ponto
        )
        valor = "".join(c for c in valor if c.isdigit() or c == ".")

        try:
            return float(valor)
        except:
            return 0.0

    def clean_valor_venda(self) -> None:
        """Aplica a limpeza à coluna 'valor_venda'."""
        self.df["valor_venda"] = self.df["valor_venda"].apply(self.limpar_valor)

    def convert_to_datetime(self) -> None:
        """Converte colunas especificadas para formato datetime."""
        for col in self.colunas_data:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], format="%d-%m-%Y", errors="coerce")

    def convert_to_string(self) -> None:
        """Converte colunas especificadas para string."""
        for col in self.colunas_string:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str)

    def convert_to_int(self) -> None:
        """Converte a coluna especificada para inteiro."""
        for col in self.colunas_int:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").astype("Int64")

    @staticmethod
    def categorizar_contratacao(tipo: str) -> str:
        """Cria categorias agrupadas para tipos de contratação."""
        categorias = set()
        if not tipo or tipo.strip() == "":
            return "Vazio/Indefinido"

        if "CLT Full" in tipo or "CLT Cotas" in tipo:
            categorias.add("CLT")
        if "PJ/Autônomo" in tipo:
            categorias.add("PJ/Autônomo")
        if "Cooperado" in tipo:
            categorias.add("Cooperado")
        if "Estagiário" in tipo:
            categorias.add("Estágio")
        if "Hunting" in tipo:
            categorias.add("Hunting")
        if "Candidato poderá escolher" in tipo:
            categorias.add("Escolha do Candidato")

        return ", ".join(sorted(categorias))

    def clean_tipo_contratacao(self) -> None:
        """Aplica a categorização de tipos de contratação."""
        self.df["categoria_contratacao"] = self.df["tipo_contratacao"].apply(self.categorizar_contratacao)

    def clean_all(self) -> pd.DataFrame:
        """Executa todas as funções de limpeza."""
        self.clean_valor_venda()
        self.clean_tipo_contratacao()
        self.convert_to_datetime()
        self.convert_to_string()
        self.convert_to_int()

        return self.df


class CleanProspects:
    """Classe para realizar a limpeza e conversão de tipos no DataFrame de prospects."""

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa a classe com um DataFrame.

        :param df: DataFrame contendo os dados das prospecções.
        """
        self.df = df.copy()

        # Colunas que devem ser tratadas como tipo texto
        self.colunas_string = [
            "titulo", "modalidade", "nome", "situacao_candidado", "comentario", "recrutador"
        ]

        # Colunas que devem ser tratadas como tipo data
        self.colunas_data = [
            'data_candidatura', 'ultima_atualizacao'
        ]

        # Colunas que devem ser tratadas como tipo data
        self.colunas_int = [
            'vaga_id', 'quantidade_prospects', 'codigo'
        ]

    def convert_to_datetime(self) -> None:
        """Converte colunas especificadas para formato datetime."""
        for col in self.colunas_data:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], format="%d-%m-%Y", errors="coerce")

    def convert_to_string(self) -> None:
        """Converte colunas especificadas para string."""
        for col in self.colunas_string:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str)

    def convert_to_int(self) -> None:
        """Converte a coluna especificada para inteiro."""
        for col in self.colunas_int:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").astype("Int64")

    def clean_all(self) -> pd.DataFrame:
        """Executa todas as funções de limpeza."""
        self.convert_to_datetime()
        self.convert_to_string()
        self.convert_to_int()

        return self.df