from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ============== SCHEMAS EXISTENTES ==============
class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UpdateUserSchema(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: str | None = None


# ============== SCHEMAS PARA CANDIDATOS ==============
class ApplicantBase(BaseModel):
    """Schema base para candidatos"""
    # Campos principais que sempre aparecem
    nome: str = ""
    email: str = ""
    telefone_celular: str = ""
    titulo_profissional: str = ""
    area_atuacao: str = ""
    nivel_profissional: str = ""
    nivel_academico: str = ""
    remuneracao: float = 0.0


class ApplicantCreate(ApplicantBase):
    """Schema para criar candidato"""
    id_applicants: str
    # Informações básicas
    telefone_recado: str = ""
    telefone: str = ""
    infos_basicas_objetivo_profissional: str = ""
    infos_basicas_inserido_por: str = ""
    infos_basicas_email: str = ""
    infos_basicas_local: str = ""
    infos_basicas_sabendo_de_nos_por: str = ""
    infos_basicas_codigo_profissional: int = 0
    infos_basicas_nome: str = ""
    
    # Informações pessoais
    data_aceite: str = ""
    cpf: str = ""
    fonte_indicacao: str = ""
    email_secundario: str = ""
    data_nascimento: Optional[datetime] = None
    sexo: str = ""
    estado_civil: str = ""
    pcd: str = ""
    endereco: str = ""
    skype: str = ""
    url_linkedin: str = ""
    facebook: str = ""
    
    # Informações profissionais
    conhecimentos_tecnicos: str = ""
    certificacoes: str = ""
    outras_certificacoes: str = ""
    
    # Formação e idiomas
    nivel_ingles: str = ""
    nivel_espanhol: str = ""
    outro_idioma: str = ""
    instituicao_ensino_superior: str = ""
    cursos: str = ""
    ano_conclusao: str = ""
    download_cv: str = ""
    qualificacoes: str = ""
    experiencias: str = ""
    outro_curso: str = ""
    
    # Cargo atual
    id_ibrati: int = 0
    email_corporativo: str = ""
    cargo_atual: str = ""
    projeto_atual: str = ""
    cliente: str = ""
    unidade: str = ""
    data_admissao: Optional[datetime] = None
    data_ultima_promocao: Optional[datetime] = None
    nome_superior_imediato: str = ""
    email_superior_imediato: str = ""
    
    # CVs
    cv_pt: str = ""
    cv_en: str = ""


class ApplicantUpdate(BaseModel):
    """Schema para atualizar candidato - campos opcionais"""
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone_celular: Optional[str] = None
    titulo_profissional: Optional[str] = None
    area_atuacao: Optional[str] = None
    nivel_profissional: Optional[str] = None
    nivel_academico: Optional[str] = None
    remuneracao: Optional[float] = None
    conhecimentos_tecnicos: Optional[str] = None
    certificacoes: Optional[str] = None
    nivel_ingles: Optional[str] = None
    nivel_espanhol: Optional[str] = None
    qualificacoes: Optional[str] = None
    experiencias: Optional[str] = None


class ApplicantPublic(BaseModel):
    """Schema público do candidato - sem dados sensíveis"""
    id: int
    id_applicants: str
    nome: str
    email: str
    titulo_profissional: str
    area_atuacao: str
    nivel_profissional: str
    nivel_academico: str
    nivel_ingles: str
    nivel_espanhol: str
    conhecimentos_tecnicos: str
    certificacoes: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ApplicantDetailed(ApplicantPublic):
    """Schema detalhado do candidato - para usuários autenticados"""
    telefone_celular: str
    remuneracao: float
    data_nascimento: Optional[datetime]
    endereco: str
    url_linkedin: str
    qualificacoes: str
    experiencias: str
    cargo_atual: str
    cliente: str
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============== SCHEMAS PARA VAGAS ==============
class JobBase(BaseModel):
    """Schema base para vagas"""
    titulo_vaga: str = ""
    cliente: str = ""
    tipo_contratacao: str = ""
    nivel_profissional: str = ""
    nivel_academico: str = ""
    areas_atuacao: str = ""
    cidade: str = ""
    estado: str = ""


class JobCreate(JobBase):
    """Schema para criar vaga"""
    id_vaga: str
    # Informações básicas
    data_requicisao: Optional[datetime] = None
    limite_esperado_para_contratacao: Optional[datetime] = None
    vaga_sap: str = ""
    solicitante_cliente: str = ""
    empresa_divisao: str = ""
    requisitante: str = ""
    analista_responsavel: str = ""
    categoria_contratacao: str = ""
    prazo_contratacao: str = ""
    objetivo_vaga: str = ""
    prioridade_vaga: str = ""
    origem_vaga: str = ""
    superior_imediato: str = ""
    
    # Perfil da vaga
    nome: str = ""
    telefone: str = ""
    pais: str = ""
    bairro: str = ""
    regiao: str = ""
    local_trabalho: str = ""
    vaga_especifica_para_pcd: str = ""
    faixa_etaria: str = ""
    horario_trabalho: str = ""
    nivel_ingles: str = ""
    nivel_espanhol: str = ""
    outro_idioma: str = ""
    principais_atividades: str = ""
    competencia_tecnicas_e_comportamentais: str = ""
    demais_observacoes: str = ""
    viagens_requeridas: str = ""
    equipamentos_necessarios: str = ""
    
    # Benefícios
    valor_venda: float = 0.0
    valor_compra_1: str = ""
    valor_compra_2: str = ""
    data_inicial: Optional[datetime] = None
    data_final: Optional[datetime] = None
    habilidades_comportamentais_necessarias: str = ""
    nome_substituto: str = ""


class JobUpdate(BaseModel):
    """Schema para atualizar vaga"""
    titulo_vaga: Optional[str] = None
    cliente: Optional[str] = None
    tipo_contratacao: Optional[str] = None
    nivel_profissional: Optional[str] = None
    nivel_academico: Optional[str] = None
    areas_atuacao: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    principais_atividades: Optional[str] = None
    competencia_tecnicas_e_comportamentais: Optional[str] = None
    valor_venda: Optional[float] = None
    limite_esperado_para_contratacao: Optional[datetime] = None


class JobPublic(BaseModel):
    """Schema público da vaga"""
    id: int
    id_vaga: str
    titulo_vaga: str
    cliente: str
    tipo_contratacao: str
    categoria_contratacao: str
    nivel_profissional: str
    nivel_academico: str
    areas_atuacao: str
    cidade: str
    estado: str
    principais_atividades: str
    competencia_tecnicas_e_comportamentais: str
    valor_venda: float
    limite_esperado_para_contratacao: Optional[datetime]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class JobDetailed(JobPublic):
    """Schema detalhado da vaga"""
    vaga_sap: str
    solicitante_cliente: str
    requisitante: str
    analista_responsavel: str
    objetivo_vaga: str
    prioridade_vaga: str
    demais_observacoes: str
    habilidades_comportamentais_necessarias: str
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============== SCHEMAS PARA PROSPECTS ==============
class ProspectBase(BaseModel):
    """Schema base para prospects"""
    vaga_id: str
    titulo: str = ""
    modalidade: str = ""
    nome: str = ""
    situacao_candidado: str = ""


class ProspectCreate(ProspectBase):
    """Schema para criar prospect"""
    quantidade_prospects: int = 0
    codigo: int = 0
    data_candidatura: Optional[datetime] = None
    ultima_atualizacao: Optional[datetime] = None
    comentario: str = ""
    recrutador: str = ""
    job_id: Optional[int] = None


class ProspectUpdate(BaseModel):
    """Schema para atualizar prospect"""
    situacao_candidado: Optional[str] = None
    comentario: Optional[str] = None
    recrutador: Optional[str] = None


class ProspectPublic(BaseModel):
    """Schema público do prospect"""
    id: int
    vaga_id: str
    titulo: str
    modalidade: str
    nome: str
    situacao_candidado: str
    data_candidatura: Optional[datetime]
    ultima_atualizacao: Optional[datetime]
    recrutador: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============== SCHEMAS PARA ANÁLISE IA ==============
class JobMatchCreate(BaseModel):
    """Schema para criar match candidato-vaga"""
    applicant_id: int
    job_id: int
    compatibility_score: float = 0.0
    technical_score: float = 0.0
    experience_score: float = 0.0
    location_score: float = 0.0
    salary_score: float = 0.0
    analysis_details: str = ""
    recommendations: str = ""
    is_recommended: bool = False


class JobMatchPublic(BaseModel):
    """Schema público do match"""
    id: int
    applicant_id: int
    job_id: int
    compatibility_score: float
    technical_score: float
    experience_score: float
    location_score: float
    salary_score: float
    is_recommended: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class JobMatchDetailed(JobMatchPublic):
    """Schema detalhado do match com dados do candidato e vaga"""
    analysis_details: str
    recommendations: str
    applicant: ApplicantPublic
    job: JobPublic
    
    model_config = ConfigDict(from_attributes=True)


# ============== SCHEMAS PARA BUSCA E FILTROS ==============
class ApplicantFilter(BaseModel):
    """Filtros para busca de candidatos"""
    nome: Optional[str] = None
    area_atuacao: Optional[str] = None
    nivel_profissional: Optional[str] = None
    nivel_academico: Optional[str] = None
    nivel_ingles: Optional[str] = None
    cidade: Optional[str] = None
    remuneracao_min: Optional[float] = None
    remuneracao_max: Optional[float] = None
    conhecimentos_tecnicos: Optional[str] = None


class JobFilter(BaseModel):
    """Filtros para busca de vagas"""
    titulo_vaga: Optional[str] = None
    cliente: Optional[str] = None
    tipo_contratacao: Optional[str] = None
    nivel_profissional: Optional[str] = None
    nivel_academico: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    valor_min: Optional[float] = None
    valor_max: Optional[float] = None
    areas_atuacao: Optional[str] = None


class MatchRequest(BaseModel):
    """Request para análise de compatibilidade"""
    applicant_id: Optional[int] = None
    job_id: Optional[int] = None
    limit: int = Field(default=10, ge=1, le=100)
    min_score: float = Field(default=0.0, ge=0.0, le=1.0)


class MatchResponse(BaseModel):
    """Response com matches encontrados"""
    matches: List[JobMatchDetailed]
    total: int
    message: str


# ============== SCHEMAS PARA ANÁLISE BULK ==============
class BulkAnalysisRequest(BaseModel):
    """Request para análise em lote"""
    job_ids: Optional[List[int]] = None
    applicant_ids: Optional[List[int]] = None
    recalculate: bool = False
    min_score: float = Field(default=0.5, ge=0.0, le=1.0)


class BulkAnalysisResponse(BaseModel):
    """Response da análise em lote"""
    processed: int
    matches_created: int
    matches_updated: int
    message: str


# ============== SCHEMAS PARA DASHBOARD ==============
class DashboardStats(BaseModel):
    """Estatísticas do dashboard"""
    total_applicants: int
    total_jobs: int
    total_prospects: int
    total_matches: int
    matches_this_month: int
    top_areas: List[dict]
    recent_matches: List[JobMatchPublic]