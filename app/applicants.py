from http import HTTPStatus
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import get_session
from .exceptions import UserNotFound, PermissionDenied
from .models import User, Applicant
from .schemas import (
    Message, 
    ApplicantCreate, 
    ApplicantUpdate, 
    ApplicantPublic, 
    ApplicantDetailed,
    ApplicantFilter
)
from .security import get_current_user

router = APIRouter(prefix='/applicants', tags=['applicants'])

# Dependências
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/create', status_code=HTTPStatus.CREATED, response_model=ApplicantPublic)
def create_applicant(
    applicant_data: ApplicantCreate, 
    session: Session, 
    current_user: CurrentUser
):
    """
    Cria um novo candidato no banco de dados.
    
    Argumentos:
        applicant_data: Dados do candidato a ser criado
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    # Verifica se já existe candidato com esse id_applicants
    existing_applicant = session.scalar(
        select(Applicant).where(Applicant.id_applicants == applicant_data.id_applicants)
    )
    
    if existing_applicant:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Candidato com este ID já existe na base de dados."
        )
    
    try:
        # Cria o candidato
        db_applicant = Applicant(**applicant_data.model_dump())
        session.add(db_applicant)
        session.commit()
        session.refresh(db_applicant)
        
        return db_applicant
        
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Erro de integridade dos dados. Verifique se todos os campos estão corretos."
        )


@router.get('/list', response_model=List[ApplicantPublic])
def list_applicants(
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Busca por nome, email ou área de atuação")
):
    """
    Lista candidatos com paginação e busca opcional.
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular (paginação)
        limit: Limite de registros por página
        search: Termo de busca (opcional)
    """
    query = select(Applicant)
    
    # Aplica filtro de busca se fornecido
    if search:
        search_filter = or_(
            Applicant.nome.ilike(f"%{search}%"),
            Applicant.email.ilike(f"%{search}%"),
            Applicant.titulo_profissional.ilike(f"%{search}%"),
            Applicant.area_atuacao.ilike(f"%{search}%"),
            Applicant.conhecimentos_tecnicos.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    # Aplica paginação e ordenação
    query = query.offset(skip).limit(limit).order_by(Applicant.created_at.desc())
    
    applicants = session.scalars(query).all()
    return applicants


@router.post('/search', response_model=List[ApplicantPublic])
def search_applicants(
    filters: ApplicantFilter,
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Busca avançada de candidatos com filtros específicos.
    
    Argumentos:
        filters: Filtros para busca
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular
        limit: Limite de registros por página
    """
    query = select(Applicant)
    conditions = []
    
    # Aplica filtros condicionalmente
    if filters.nome:
        conditions.append(Applicant.nome.ilike(f"%{filters.nome}%"))
    
    if filters.area_atuacao:
        conditions.append(Applicant.area_atuacao.ilike(f"%{filters.area_atuacao}%"))
    
    if filters.nivel_profissional:
        conditions.append(Applicant.nivel_profissional.ilike(f"%{filters.nivel_profissional}%"))
    
    if filters.nivel_academico:
        conditions.append(Applicant.nivel_academico.ilike(f"%{filters.nivel_academico}%"))
    
    if filters.nivel_ingles:
        conditions.append(Applicant.nivel_ingles.ilike(f"%{filters.nivel_ingles}%"))
    
    if filters.conhecimentos_tecnicos:
        conditions.append(Applicant.conhecimentos_tecnicos.ilike(f"%{filters.conhecimentos_tecnicos}%"))
    
    if filters.remuneracao_min is not None:
        conditions.append(Applicant.remuneracao >= filters.remuneracao_min)
    
    if filters.remuneracao_max is not None:
        conditions.append(Applicant.remuneracao <= filters.remuneracao_max)
    
    # Aplica todos os filtros
    if conditions:
        query = query.where(and_(*conditions))
    
    # Aplica paginação
    query = query.offset(skip).limit(limit).order_by(Applicant.created_at.desc())
    
    applicants = session.scalars(query).all()
    return applicants


@router.get('/{applicant_id}', response_model=ApplicantDetailed)
def get_applicant(
    applicant_id: int,
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém um candidato específico por ID.
    
    Argumentos:
        applicant_id: ID do candidato
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    applicant = session.scalar(
        select(Applicant).where(Applicant.id == applicant_id)
    )
    
    if not applicant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Candidato não encontrado."
        )
    
    return applicant


@router.get('/by-external-id/{external_id}', response_model=ApplicantDetailed)
def get_applicant_by_external_id(
    external_id: str,
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém um candidato pelo ID externo (id_applicants).
    
    Argumentos:
        external_id: ID externo do candidato
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    applicant = session.scalar(
        select(Applicant).where(Applicant.id_applicants == external_id)
    )
    
    if not applicant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Candidato não encontrado."
        )
    
    return applicant


@router.put('/{applicant_id}', response_model=ApplicantDetailed)
def update_applicant(
    applicant_id: int,
    applicant_update: ApplicantUpdate,
    session: Session,
    current_user: CurrentUser
):
    """
    Atualiza um candidato existente.
    
    Argumentos:
        applicant_id: ID do candidato
        applicant_update: Dados para atualização
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    applicant = session.scalar(
        select(Applicant).where(Applicant.id == applicant_id)
    )
    
    if not applicant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Candidato não encontrado."
        )
    
    try:
        # Atualiza apenas os campos fornecidos
        update_data = applicant_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(applicant, field, value)
        
        session.commit()
        session.refresh(applicant)
        
        return applicant
        
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Erro de integridade dos dados. Verifique se todos os campos estão corretos."
        )


@router.delete('/{applicant_id}', response_model=Message)
def delete_applicant(
    applicant_id: int,
    session: Session,
    current_user: CurrentUser
):
    """
    Remove um candidato do banco de dados.
    
    Argumentos:
        applicant_id: ID do candidato
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    applicant = session.scalar(
        select(Applicant).where(Applicant.id == applicant_id)
    )
    
    if not applicant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Candidato não encontrado."
        )
    
    session.delete(applicant)
    session.commit()
    
    return {"message": f"Candidato {applicant.nome} removido com sucesso."}


@router.get('/stats/summary')
def get_applicants_summary(
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém estatísticas resumidas dos candidatos.
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    # Total de candidatos
    total_applicants = session.scalar(
        select(func.count(Applicant.id))
    )
    
    # Candidatos por nível profissional
    nivel_profissional_stats = session.execute(
        select(
            Applicant.nivel_profissional,
            func.count(Applicant.id).label('count')
        )
        .where(Applicant.nivel_profissional != '')
        .group_by(Applicant.nivel_profissional)
        .order_by(func.count(Applicant.id).desc())
    ).all()
    
    # Candidatos por área de atuação (top 10)
    areas_stats = session.execute(
        select(
            Applicant.area_atuacao,
            func.count(Applicant.id).label('count')
        )
        .where(Applicant.area_atuacao != '')
        .group_by(Applicant.area_atuacao)
        .order_by(func.count(Applicant.id).desc())
        .limit(10)
    ).all()
    
    # Estatísticas de remuneração
    salary_stats = session.execute(
        select(
            func.avg(Applicant.remuneracao).label('avg_salary'),
            func.min(Applicant.remuneracao).label('min_salary'),
            func.max(Applicant.remuneracao).label('max_salary')
        )
        .where(Applicant.remuneracao > 0)
    ).first()
    
    return {
        "total_applicants": total_applicants,
        "nivel_profissional": [
            {"nivel": row.nivel_profissional, "count": row.count} 
            for row in nivel_profissional_stats
        ],
        "top_areas": [
            {"area": row.area_atuacao, "count": row.count} 
            for row in areas_stats
        ],
        "salary_stats": {
            "average": float(salary_stats.avg_salary) if salary_stats.avg_salary else 0,
            "minimum": float(salary_stats.min_salary) if salary_stats.min_salary else 0,
            "maximum": float(salary_stats.max_salary) if salary_stats.max_salary else 0
        } if salary_stats else {"average": 0, "minimum": 0, "maximum": 0}
    }


@router.post('/bulk-create', response_model=dict)
def bulk_create_applicants(
    applicants_data: List[ApplicantCreate],
    session: Session,
    current_user: CurrentUser
):
    """
    Cria múltiplos candidatos em lote.
    
    Argumentos:
        applicants_data: Lista de candidatos para criar
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    created_count = 0
    errors = []
    
    for idx, applicant_data in enumerate(applicants_data):
        try:
            # Verifica se já existe
            existing = session.scalar(
                select(Applicant).where(Applicant.id_applicants == applicant_data.id_applicants)
            )
            
            if existing:
                errors.append({
                    "index": idx,
                    "id_applicants": applicant_data.id_applicants,
                    "error": "Candidato já existe"
                })
                continue
            
            # Cria o candidato
            db_applicant = Applicant(**applicant_data.model_dump())
            session.add(db_applicant)
            created_count += 1
            
        except Exception as e:
            errors.append({
                "index": idx,
                "id_applicants": applicant_data.id_applicants,
                "error": str(e)
            })
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar candidatos: {str(e)}"
        )
    
    return {
        "message": f"Processamento concluído",
        "created": created_count,
        "total": len(applicants_data),
        "errors": errors
    }