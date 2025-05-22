from datetime import datetime
from sqlalchemy import func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, registry
from .database import engine

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    """Modelo User"""
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Applicant:
    """Modelo para candidatos/aplicantes"""
    __tablename__ = 'applicants'
    
    # Chave primária
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_applicants: Mapped[str] = mapped_column(unique=True)
    
    # Informações Básicas
    telefone_recado: Mapped[str] = mapped_column(default="")
    telefone: Mapped[str] = mapped_column(default="")
    infos_basicas_objetivo_profissional: Mapped[str] = mapped_column(Text, default="")
    infos_basicas_data_criacao: Mapped[datetime | None] = mapped_column(default=None)
    infos_basicas_inserido_por: Mapped[str] = mapped_column(default="")
    infos_basicas_email: Mapped[str] = mapped_column(default="")
    infos_basicas_local: Mapped[str] = mapped_column(default="")
    infos_basicas_sabendo_de_nos_por: Mapped[str] = mapped_column(default="")
    infos_basicas_data_atualizacao: Mapped[datetime | None] = mapped_column(default=None)
    infos_basicas_codigo_profissional: Mapped[int] = mapped_column(default=0)
    infos_basicas_nome: Mapped[str] = mapped_column(default="")
    
    # Informações Pessoais
    data_aceite: Mapped[str] = mapped_column(default="")
    nome: Mapped[str] = mapped_column(default="")
    cpf: Mapped[str] = mapped_column(default="")
    fonte_indicacao: Mapped[str] = mapped_column(default="")
    email: Mapped[str] = mapped_column(default="")
    email_secundario: Mapped[str] = mapped_column(default="")
    data_nascimento: Mapped[datetime | None] = mapped_column(default=None)
    telefone_celular: Mapped[str] = mapped_column(default="")
    sexo: Mapped[str] = mapped_column(default="")
    estado_civil: Mapped[str] = mapped_column(default="")
    pcd: Mapped[str] = mapped_column(default="")
    endereco: Mapped[str] = mapped_column(Text, default="")
    skype: Mapped[str] = mapped_column(default="")
    url_linkedin: Mapped[str] = mapped_column(default="")
    facebook: Mapped[str] = mapped_column(default="")
    
    # Informações Profissionais
    titulo_profissional: Mapped[str] = mapped_column(default="")
    area_atuacao: Mapped[str] = mapped_column(Text, default="")
    conhecimentos_tecnicos: Mapped[str] = mapped_column(Text, default="")
    certificacoes: Mapped[str] = mapped_column(Text, default="")
    outras_certificacoes: Mapped[str] = mapped_column(Text, default="")
    remuneracao: Mapped[float] = mapped_column(default=0.0)
    nivel_profissional: Mapped[str] = mapped_column(default="")
    
    # Formação e Idiomas
    nivel_academico: Mapped[str] = mapped_column(default="")
    nivel_ingles: Mapped[str] = mapped_column(default="")
    nivel_espanhol: Mapped[str] = mapped_column(default="")
    outro_idioma: Mapped[str] = mapped_column(default="")
    instituicao_ensino_superior: Mapped[str] = mapped_column(default="")
    cursos: Mapped[str] = mapped_column(Text, default="")
    ano_conclusao: Mapped[str] = mapped_column(default="")
    download_cv: Mapped[str] = mapped_column(default="")
    qualificacoes: Mapped[str] = mapped_column(Text, default="")
    experiencias: Mapped[str] = mapped_column(Text, default="")
    outro_curso: Mapped[str] = mapped_column(default="")
    
    # Cargo Atual
    id_ibrati: Mapped[int] = mapped_column(default=0)
    email_corporativo: Mapped[str] = mapped_column(default="")
    cargo_atual: Mapped[str] = mapped_column(default="")
    projeto_atual: Mapped[str] = mapped_column(default="")
    cliente: Mapped[str] = mapped_column(default="")
    unidade: Mapped[str] = mapped_column(default="")
    data_admissao: Mapped[datetime | None] = mapped_column(default=None)
    data_ultima_promocao: Mapped[datetime | None] = mapped_column(default=None)
    nome_superior_imediato: Mapped[str] = mapped_column(default="")
    email_superior_imediato: Mapped[str] = mapped_column(default="")
    
    # CVs
    cv_pt: Mapped[str] = mapped_column(Text, default="")
    cv_en: Mapped[str] = mapped_column(Text, default="")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Job:
    """Modelo para vagas"""
    __tablename__ = 'jobs'
    
    # Chave primária
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_vaga: Mapped[str] = mapped_column(unique=True)
    
    # Informações Básicas
    data_requicisao: Mapped[datetime | None] = mapped_column(default=None)
    limite_esperado_para_contratacao: Mapped[datetime | None] = mapped_column(default=None)
    titulo_vaga: Mapped[str] = mapped_column(default="")
    vaga_sap: Mapped[str] = mapped_column(default="")
    cliente: Mapped[str] = mapped_column(default="")
    solicitante_cliente: Mapped[str] = mapped_column(default="")
    empresa_divisao: Mapped[str] = mapped_column(default="")
    requisitante: Mapped[str] = mapped_column(default="")
    analista_responsavel: Mapped[str] = mapped_column(default="")
    tipo_contratacao: Mapped[str] = mapped_column(default="")
    categoria_contratacao: Mapped[str] = mapped_column(default="")
    prazo_contratacao: Mapped[str] = mapped_column(default="")
    objetivo_vaga: Mapped[str] = mapped_column(Text, default="")
    prioridade_vaga: Mapped[str] = mapped_column(default="")
    origem_vaga: Mapped[str] = mapped_column(default="")
    superior_imediato: Mapped[str] = mapped_column(default="")
    
    # Perfil da Vaga
    nome: Mapped[str] = mapped_column(default="")
    telefone: Mapped[str] = mapped_column(default="")
    pais: Mapped[str] = mapped_column(default="")
    estado: Mapped[str] = mapped_column(default="")
    cidade: Mapped[str] = mapped_column(default="")
    bairro: Mapped[str] = mapped_column(default="")
    regiao: Mapped[str] = mapped_column(default="")
    local_trabalho: Mapped[str] = mapped_column(default="")
    vaga_especifica_para_pcd: Mapped[str] = mapped_column(default="")
    faixa_etaria: Mapped[str] = mapped_column(default="")
    horario_trabalho: Mapped[str] = mapped_column(default="")
    nivel_profissional: Mapped[str] = mapped_column(default="")
    nivel_academico: Mapped[str] = mapped_column(default="")
    nivel_ingles: Mapped[str] = mapped_column(default="")
    nivel_espanhol: Mapped[str] = mapped_column(default="")
    outro_idioma: Mapped[str] = mapped_column(default="")
    areas_atuacao: Mapped[str] = mapped_column(Text, default="")
    principais_atividades: Mapped[str] = mapped_column(Text, default="")
    competencia_tecnicas_e_comportamentais: Mapped[str] = mapped_column(Text, default="")
    demais_observacoes: Mapped[str] = mapped_column(Text, default="")
    viagens_requeridas: Mapped[str] = mapped_column(default="")
    equipamentos_necessarios: Mapped[str] = mapped_column(Text, default="")
    
    # Benefícios e Valores
    valor_venda: Mapped[float] = mapped_column(default=0.0)
    valor_compra_1: Mapped[str] = mapped_column(default="")
    valor_compra_2: Mapped[str] = mapped_column(default="")
    data_inicial: Mapped[datetime | None] = mapped_column(default=None)
    data_final: Mapped[datetime | None] = mapped_column(default=None)
    habilidades_comportamentais_necessarias: Mapped[str] = mapped_column(Text, default="")
    nome_substituto: Mapped[str] = mapped_column(default="")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Prospect:
    """Modelo para prospecções (candidaturas)"""
    __tablename__ = 'prospects'
    
    # Chave primária
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    
    # Relacionamento com vaga
    vaga_id: Mapped[str] = mapped_column()
    job_id: Mapped[int | None] = mapped_column(ForeignKey('jobs.id'), default=None)
    job: Mapped[Job | None] = relationship(init=False, default=None)
    
    # Informações da Vaga
    titulo: Mapped[str] = mapped_column(default="")
    modalidade: Mapped[str] = mapped_column(default="")
    quantidade_prospects: Mapped[int] = mapped_column(default=0)
    
    # Informações do Candidato
    nome: Mapped[str] = mapped_column(default="")
    codigo: Mapped[int] = mapped_column(default=0)
    situacao_candidado: Mapped[str] = mapped_column(default="")
    data_candidatura: Mapped[datetime | None] = mapped_column(default=None)
    ultima_atualizacao: Mapped[datetime | None] = mapped_column(default=None)
    comentario: Mapped[str] = mapped_column(Text, default="")
    recrutador: Mapped[str] = mapped_column(default="")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class JobMatch:
    """Modelo para armazenar matches entre candidatos e vagas (para IA)"""
    __tablename__ = 'job_matches'
    
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    
    # Relacionamentos
    applicant_id: Mapped[int] = mapped_column(ForeignKey('applicants.id'))
    job_id: Mapped[int] = mapped_column(ForeignKey('jobs.id'))
    
    applicant: Mapped[Applicant] = relationship(init=False)
    job: Mapped[Job] = relationship(init=False)
    
    # Scores da análise IA
    compatibility_score: Mapped[float] = mapped_column(default=0.0)
    technical_score: Mapped[float] = mapped_column(default=0.0)
    experience_score: Mapped[float] = mapped_column(default=0.0)
    location_score: Mapped[float] = mapped_column(default=0.0)
    salary_score: Mapped[float] = mapped_column(default=0.0)
    
    # Análise detalhada
    analysis_details: Mapped[str] = mapped_column(Text, default="")
    recommendations: Mapped[str] = mapped_column(Text, default="")
    
    # Status
    is_recommended: Mapped[bool] = mapped_column(default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


# Criar todas as tabelas
table_registry.metadata.create_all(bind=engine)