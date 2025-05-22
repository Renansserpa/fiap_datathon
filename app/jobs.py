from http import HTTPStatus
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import get_session
from .exceptions import UserNotFound, PermissionDenied
from .models import User, Job
from .schemas import (
    Message, 
    JobCreate, 
    JobUpdate, 
    JobPublic, 
    JobDetailed,
    JobFilter
)
from .security import get_current_user

router = APIRouter(prefix='/jobs', tags=['jobs'])

# Dependências
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/create', status_code=HTTPStatus.CREATED, response_model=JobPublic)
def create_job(
    job_data: JobCreate, 
    session: Session, 
    current_user: CurrentUser
):
    """
    Cria uma nova vaga no banco de dados.
    
    Argumentos:
        job_data: Dados da vaga a ser criada
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    # Verifica se já existe vaga com esse id_vaga
    existing_job = session.scalar(
        select(Job).where(Job.id_vaga == job_data.id_vaga)
    )
    
    if existing_job:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Vaga com este ID já existe na base de dados."
        )
    
    try:
        # Cria a vaga
        db_job = Job(**job_data.model_dump())
        session.add(db_job)
        session.commit()
        session.refresh(db_job)
        
        return db_job
        
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Erro de integridade dos dados. Verifique se todos os campos estão corretos."
        )


@router.get('/list', response_model=List[JobPublic])
def list_jobs(
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Busca por título, cliente ou área de atuação"),
    active_only: bool = Query(False, description="Apenas vagas ativas (não expiradas)")
):
    """
    Lista vagas com paginação e busca opcional.
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular (paginação)
        limit: Limite de registros por página
        search: Termo de busca (opcional)
        active_only: Filtrar apenas vagas ativas
    """
    query = select(Job)
    
    # Filtro de vagas ativas (não expiradas)
    if active_only:
        query = query.where(
            or_(
                Job.limite_esperado_para_contratacao.is_(None),
                Job.limite_esperado_para_contratacao >= func.current_date()
            )
        )
    
    # Aplica filtro de busca se fornecido
    if search:
        search_filter = or_(
            Job.titulo_vaga.ilike(f"%{search}%"),
            Job.cliente.ilike(f"%{search}%"),
            Job.areas_atuacao.ilike(f"%{search}%"),
            Job.principais_atividades.ilike(f"%{search}%"),
            Job.competencia_tecnicas_e_comportamentais.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    # Aplica paginação e ordenação
    query = query.offset(skip).limit(limit).order_by(Job.created_at.desc())
    
    jobs = session.scalars(query).all()
    return jobs


@router.post('/search', response_model=List[JobPublic])
def search_jobs(
    filters: JobFilter,
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Busca avançada de vagas com filtros específicos.
    
    Argumentos:
        filters: Filtros para busca
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular
        limit: Limite de registros por página
    """
    query = select(Job)
    conditions = []
    
    # Aplica filtros condicionalmente
    if filters.titulo_vaga:
        conditions.append(Job.titulo_vaga.ilike(f"%{filters.titulo_vaga}%"))
    
    if filters.cliente:
        conditions.append(Job.cliente.ilike(f"%{filters.cliente}%"))
    
    if filters.tipo_contratacao:
        conditions.append(Job.tipo_contratacao.ilike(f"%{filters.tipo_contratacao}%"))
    
    if filters.nivel_profissional:
        conditions.append(Job.nivel_profissional.ilike(f"%{filters.nivel_profissional}%"))
    
    if filters.nivel_academico:
        conditions.append(Job.nivel_academico.ilike(f"%{filters.nivel_academico}%"))
    
    if filters.cidade:
        conditions.append(Job.cidade.ilike(f"%{filters.cidade}%"))
    
    if filters.estado:
        conditions.append(Job.estado.ilike(f"%{filters.estado}%"))
    
    if filters.areas_atuacao:
        conditions.append(Job.areas_atuacao.ilike(f"%{filters.areas_atuacao}%"))
    
    if filters.valor_min is not None:
        conditions.append(Job.valor_venda >= filters.valor_min)
    
    if filters.valor_max is not None:
        conditions.append(Job.valor_venda <= filters.valor_max)
    
    # Aplica todos os filtros
    if conditions:
        query = query.where(and_(*conditions))
    
    # Aplica paginação
    query = query.offset(skip).limit(limit).order_by(Job.created_at.desc())
    
    jobs = session.scalars(query).all()
    return jobs


@router.get('/{job_id}', response_model=JobDetailed)
def get_job(
    job_id: int,
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém uma vaga específica por ID.
    
    Argumentos:
        job_id: ID da vaga
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    job = session.scalar(
        select(Job).where(Job.id == job_id)
    )
    
    if not job:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Vaga não encontrada."
        )
    
    return job


@router.get('/by-external-id/{external_id}', response_model=JobDetailed)
def get_job_by_external_id(
    external_id: str,
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém uma vaga pelo ID externo (id_vaga).
    
    Argumentos:
        external_id: ID externo da vaga
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    job = session.scalar(
        select(Job).where(Job.id_vaga == external_id)
    )
    
    if not job:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Vaga não encontrada."
        )
    
    return job


@router.put('/{job_id}', response_model=JobDetailed)
def update_job(
    job_id: int,
    job_update: JobUpdate,
    session: Session,
    current_user: CurrentUser
):
    """
    Atualiza uma vaga existente.
    
    Argumentos:
        job_id: ID da vaga
        job_update: Dados para atualização
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    job = session.scalar(
        select(Job).where(Job.id == job_id)
    )
    
    if not job:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Vaga não encontrada."
        )
    
    try:
        # Atualiza apenas os campos fornecidos
        update_data = job_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(job, field, value)
        
        session.commit()
        session.refresh(job)
        
        return job
        
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Erro de integridade dos dados. Verifique se todos os campos estão corretos."
        )


@router.delete('/{job_id}', response_model=Message)
def delete_job(
    job_id: int,
    session: Session,
    current_user: CurrentUser
):
    """
    Remove uma vaga do banco de dados.
    
    Argumentos:
        job_id: ID da vaga
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    job = session.scalar(
        select(Job).where(Job.id == job_id)
    )
    
    if not job:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Vaga não encontrada."
        )
    
    session.delete(job)
    session.commit()
    
    return {"message": f"Vaga '{job.titulo_vaga}' removida com sucesso."}


@router.get('/stats/summary')
def get_jobs_summary(
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém estatísticas resumidas das vagas.
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    # Total de vagas
    total_jobs = session.scalar(
        select(func.count(Job.id))
    )
    
    # Vagas ativas (não expiradas)
    active_jobs = session.scalar(
        select(func.count(Job.id))
        .where(
            or_(
                Job.limite_esperado_para_contratacao.is_(None),
                Job.limite_esperado_para_contratacao >= func.current_date()
            )
        )
    )
    
    # Vagas por cliente (top 10)
    client_stats = session.execute(
        select(
            Job.cliente,
            func.count(Job.id).label('count')
        )
        .where(Job.cliente != '')
        .group_by(Job.cliente)
        .order_by(func.count(Job.id).desc())
        .limit(10)
    ).all()
    
    # Vagas por tipo de contratação
    contract_stats = session.execute(
        select(
            Job.categoria_contratacao,
            func.count(Job.id).label('count')
        )
        .where(Job.categoria_contratacao != '')
        .group_by(Job.categoria_contratacao)
        .order_by(func.count(Job.id).desc())
    ).all()
    
    # Vagas por nível profissional
    level_stats = session.execute(
        select(
            Job.nivel_profissional,
            func.count(Job.id).label('count')
        )
        .where(Job.nivel_profissional != '')
        .group_by(Job.nivel_profissional)
        .order_by(func.count(Job.id).desc())
    ).all()
    
    # Estatísticas de valores
    value_stats = session.execute(
        select(
            func.avg(Job.valor_venda).label('avg_value'),
            func.min(Job.valor_venda).label('min_value'),
            func.max(Job.valor_venda).label('max_value')
        )
        .where(Job.valor_venda > 0)
    ).first()
    
    # Vagas por região (top 10)
    region_stats = session.execute(
        select(
            func.concat(Job.cidade, ' - ', Job.estado).label('location'),
            func.count(Job.id).label('count')
        )
        .where(and_(Job.cidade != '', Job.estado != ''))
        .group_by(Job.cidade, Job.estado)
        .order_by(func.count(Job.id).desc())
        .limit(10)
    ).all()
    
    return {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "expired_jobs": total_jobs - active_jobs,
        "top_clients": [
            {"cliente": row.cliente, "count": row.count} 
            for row in client_stats
        ],
        "contract_types": [
            {"tipo": row.categoria_contratacao, "count": row.count} 
            for row in contract_stats
        ],
        "professional_levels": [
            {"nivel": row.nivel_profissional, "count": row.count} 
            for row in level_stats
        ],
        "value_stats": {
            "average": float(value_stats.avg_value) if value_stats.avg_value else 0,
            "minimum": float(value_stats.min_value) if value_stats.min_value else 0,
            "maximum": float(value_stats.max_value) if value_stats.max_value else 0
        } if value_stats else {"average": 0, "minimum": 0, "maximum": 0},
        "top_regions": [
            {"location": row.location, "count": row.count} 
            for row in region_stats
        ]
    }


@router.get('/active/list', response_model=List[JobPublic])
def list_active_jobs(
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Lista apenas vagas ativas (não expiradas).
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular
        limit: Limite de registros por página
    """
    query = (
        select(Job)
        .where(
            or_(
                Job.limite_esperado_para_contratacao.is_(None),
                Job.limite_esperado_para_contratacao >= func.current_date()
            )
        )
        .offset(skip)
        .limit(limit)
        .order_by(Job.created_at.desc())
    )
    
    jobs = session.scalars(query).all()
    return jobs


@router.get('/expired/list', response_model=List[JobPublic])
def list_expired_jobs(
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Lista vagas expiradas.
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular
        limit: Limite de registros por página
    """
    query = (
        select(Job)
        .where(
            and_(
                Job.limite_esperado_para_contratacao.is_not(None),
                Job.limite_esperado_para_contratacao < func.current_date()
            )
        )
        .offset(skip)
        .limit(limit)
        .order_by(Job.limite_esperado_para_contratacao.desc())
    )
    
    jobs = session.scalars(query).all()
    return jobs


@router.post('/bulk-create', response_model=dict)
def bulk_create_jobs(
    jobs_data: List[JobCreate],
    session: Session,
    current_user: CurrentUser
):
    """
    Cria múltiplas vagas em lote.
    
    Argumentos:
        jobs_data: Lista de vagas para criar
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    created_count = 0
    errors = []
    
    for idx, job_data in enumerate(jobs_data):
        try:
            # Verifica se já existe
            existing = session.scalar(
                select(Job).where(Job.id_vaga == job_data.id_vaga)
            )
            
            if existing:
                errors.append({
                    "index": idx,
                    "id_vaga": job_data.id_vaga,
                    "error": "Vaga já existe"
                })
                continue
            
            # Cria a vaga
            db_job = Job(**job_data.model_dump())
            session.add(db_job)
            created_count += 1
            
        except Exception as e:
            errors.append({
                "index": idx,
                "id_vaga": job_data.id_vaga,
                "error": str(e)
            })
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar vagas: {str(e)}"
        )
    
    return {
        "message": f"Processamento concluído",
        "created": created_count,
        "total": len(jobs_data),
        "errors": errors
    }