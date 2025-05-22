from http import HTTPStatus
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import get_session
from .exceptions import UserNotFound, PermissionDenied
from .models import User, Prospect, Job
from .schemas import (
    Message, 
    ProspectCreate, 
    ProspectUpdate, 
    ProspectPublic
)
from .security import get_current_user

router = APIRouter(prefix='/prospects', tags=['prospects'])

# Dependências
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/create', status_code=HTTPStatus.CREATED, response_model=ProspectPublic)
def create_prospect(
    prospect_data: ProspectCreate, 
    session: Session, 
    current_user: CurrentUser
):
    """
    Cria um novo prospect (candidatura) no banco de dados.
    
    Argumentos:
        prospect_data: Dados do prospect a ser criado
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    try:
        # Verifica se a vaga existe (se job_id foi fornecido)
        if prospect_data.job_id:
            job = session.scalar(
                select(Job).where(Job.id == prospect_data.job_id)
            )
            if not job:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail="Vaga não encontrada."
                )
        
        # Cria o prospect
        db_prospect = Prospect(**prospect_data.model_dump())
        session.add(db_prospect)
        session.commit()
        session.refresh(db_prospect)
        
        return db_prospect
        
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Erro de integridade dos dados. Verifique se todos os campos estão corretos."
        )


@router.get('/list', response_model=List[ProspectPublic])
def list_prospects(
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Busca por nome, título da vaga ou recrutador"),
    vaga_id: Optional[str] = Query(None, description="Filtrar por ID da vaga"),
    situacao: Optional[str] = Query(None, description="Filtrar por situação do candidato")
):
    """
    Lista prospects com paginação e filtros opcionais.
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular (paginação)
        limit: Limite de registros por página
        search: Termo de busca (opcional)
        vaga_id: ID da vaga para filtrar
        situacao: Situação do candidato para filtrar
    """
    query = select(Prospect)
    
    # Filtro por vaga específica
    if vaga_id:
        query = query.where(Prospect.vaga_id == vaga_id)
    
    # Filtro por situação
    if situacao:
        query = query.where(Prospect.situacao_candidado.ilike(f"%{situacao}%"))
    
    # Aplica filtro de busca se fornecido
    if search:
        search_filter = or_(
            Prospect.nome.ilike(f"%{search}%"),
            Prospect.titulo.ilike(f"%{search}%"),
            Prospect.recrutador.ilike(f"%{search}%"),
            Prospect.comentario.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    # Aplica paginação e ordenação
    query = query.offset(skip).limit(limit).order_by(Prospect.created_at.desc())
    
    prospects = session.scalars(query).all()
    return prospects


@router.get('/{prospect_id}', response_model=ProspectPublic)
def get_prospect(
    prospect_id: int,
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém um prospect específico por ID.
    
    Argumentos:
        prospect_id: ID do prospect
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    prospect = session.scalar(
        select(Prospect).where(Prospect.id == prospect_id)
    )
    
    if not prospect:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Prospect não encontrado."
        )
    
    return prospect


@router.put('/{prospect_id}', response_model=ProspectPublic)
def update_prospect(
    prospect_id: int,
    prospect_update: ProspectUpdate,
    session: Session,
    current_user: CurrentUser
):
    """
    Atualiza um prospect existente.
    
    Argumentos:
        prospect_id: ID do prospect
        prospect_update: Dados para atualização
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    prospect = session.scalar(
        select(Prospect).where(Prospect.id == prospect_id)
    )
    
    if not prospect:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Prospect não encontrado."
        )
    
    try:
        # Atualiza apenas os campos fornecidos
        update_data = prospect_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(prospect, field, value)
        
        session.commit()
        session.refresh(prospect)
        
        return prospect
        
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Erro de integridade dos dados. Verifique se todos os campos estão corretos."
        )


@router.delete('/{prospect_id}', response_model=Message)
def delete_prospect(
    prospect_id: int,
    session: Session,
    current_user: CurrentUser
):
    """
    Remove um prospect do banco de dados.
    
    Argumentos:
        prospect_id: ID do prospect
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    prospect = session.scalar(
        select(Prospect).where(Prospect.id == prospect_id)
    )
    
    if not prospect:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Prospect não encontrado."
        )
    
    session.delete(prospect)
    session.commit()
    
    return {"message": f"Prospect de {prospect.nome} removido com sucesso."}


@router.get('/by-vaga/{vaga_id}', response_model=List[ProspectPublic])
def get_prospects_by_vaga(
    vaga_id: str,
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Obtém todos os prospects de uma vaga específica.
    
    Argumentos:
        vaga_id: ID da vaga
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular
        limit: Limite de registros por página
    """
    query = (
        select(Prospect)
        .where(Prospect.vaga_id == vaga_id)
        .offset(skip)
        .limit(limit)
        .order_by(Prospect.data_candidatura.desc())
    )
    
    prospects = session.scalars(query).all()
    return prospects


@router.get('/by-candidato/{nome_candidato}', response_model=List[ProspectPublic])
def get_prospects_by_candidato(
    nome_candidato: str,
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Obtém todas as candidaturas de um candidato específico.
    
    Argumentos:
        nome_candidato: Nome do candidato
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular
        limit: Limite de registros por página
    """
    query = (
        select(Prospect)
        .where(Prospect.nome.ilike(f"%{nome_candidato}%"))
        .offset(skip)
        .limit(limit)
        .order_by(Prospect.data_candidatura.desc())
    )
    
    prospects = session.scalars(query).all()
    return prospects


@router.get('/by-recrutador/{recrutador}', response_model=List[ProspectPublic])
def get_prospects_by_recrutador(
    recrutador: str,
    session: Session,
    current_user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Obtém todos os prospects de um recrutador específico.
    
    Argumentos:
        recrutador: Nome do recrutador
        session: Sessão do banco de dados
        current_user: Usuário autenticado
        skip: Número de registros para pular
        limit: Limite de registros por página
    """
    query = (
        select(Prospect)
        .where(Prospect.recrutador.ilike(f"%{recrutador}%"))
        .offset(skip)
        .limit(limit)
        .order_by(Prospect.data_candidatura.desc())
    )
    
    prospects = session.scalars(query).all()
    return prospects


@router.get('/stats/summary')
def get_prospects_summary(
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém estatísticas resumidas dos prospects.
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    # Total de prospects
    total_prospects = session.scalar(
        select(func.count(Prospect.id))
    )
    
    # Prospects por situação
    situacao_stats = session.execute(
        select(
            Prospect.situacao_candidado,
            func.count(Prospect.id).label('count')
        )
        .where(Prospect.situacao_candidado != '')
        .group_by(Prospect.situacao_candidado)
        .order_by(func.count(Prospect.id).desc())
    ).all()
    
    # Prospects por recrutador (top 10)
    recrutador_stats = session.execute(
        select(
            Prospect.recrutador,
            func.count(Prospect.id).label('count')
        )
        .where(Prospect.recrutador != '')
        .group_by(Prospect.recrutador)
        .order_by(func.count(Prospect.id).desc())
        .limit(10)
    ).all()
    
    # Prospects por modalidade
    modalidade_stats = session.execute(
        select(
            Prospect.modalidade,
            func.count(Prospect.id).label('count')
        )
        .where(Prospect.modalidade != '')
        .group_by(Prospect.modalidade)
        .order_by(func.count(Prospect.id).desc())
    ).all()
    
    # Vagas com mais prospects (top 10)
    vagas_populares = session.execute(
        select(
            Prospect.vaga_id,
            Prospect.titulo,
            func.count(Prospect.id).label('count')
        )
        .group_by(Prospect.vaga_id, Prospect.titulo)
        .order_by(func.count(Prospect.id).desc())
        .limit(10)
    ).all()
    
    # Prospects recentes (últimos 30 dias)
    prospects_recentes = session.scalar(
        select(func.count(Prospect.id))
        .where(Prospect.created_at >= func.current_date() - func.interval('30 days'))
    )
    
    return {
        "total_prospects": total_prospects,
        "prospects_recentes_30_dias": prospects_recentes,
        "situacoes": [
            {"situacao": row.situacao_candidado, "count": row.count} 
            for row in situacao_stats
        ],
        "top_recrutadores": [
            {"recrutador": row.recrutador, "count": row.count} 
            for row in recrutador_stats
        ],
        "modalidades": [
            {"modalidade": row.modalidade, "count": row.count} 
            for row in modalidade_stats
        ],
        "vagas_mais_populares": [
            {
                "vaga_id": row.vaga_id, 
                "titulo": row.titulo, 
                "count": row.count
            } 
            for row in vagas_populares
        ]
    }


@router.get('/stats/situacoes')
def get_situacoes_stats(
    session: Session,
    current_user: CurrentUser
):
    """
    Obtém estatísticas detalhadas por situação do candidato.
    
    Argumentos:
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    # Estatísticas detalhadas por situação
    situacao_detalhada = session.execute(
        select(
            Prospect.situacao_candidado,
            func.count(Prospect.id).label('total'),
            func.count(
                func.case((Prospect.created_at >= func.current_date() - func.interval('7 days'), 1))
            ).label('ultimos_7_dias'),
            func.count(
                func.case((Prospect.created_at >= func.current_date() - func.interval('30 days'), 1))
            ).label('ultimos_30_dias')
        )
        .where(Prospect.situacao_candidado != '')
        .group_by(Prospect.situacao_candidado)
        .order_by(func.count(Prospect.id).desc())
    ).all()
    
    return {
        "situacoes_detalhadas": [
            {
                "situacao": row.situacao_candidado,
                "total": row.total,
                "ultimos_7_dias": row.ultimos_7_dias,
                "ultimos_30_dias": row.ultimos_30_dias
            }
            for row in situacao_detalhada
        ]
    }


@router.post('/bulk-create', response_model=dict)
def bulk_create_prospects(
    prospects_data: List[ProspectCreate],
    session: Session,
    current_user: CurrentUser
):
    """
    Cria múltiplos prospects em lote.
    
    Argumentos:
        prospects_data: Lista de prospects para criar
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    created_count = 0
    errors = []
    
    for idx, prospect_data in enumerate(prospects_data):
        try:
            # Verifica se a vaga existe (se job_id foi fornecido)
            if prospect_data.job_id:
                job = session.scalar(
                    select(Job).where(Job.id == prospect_data.job_id)
                )
                if not job:
                    errors.append({
                        "index": idx,
                        "vaga_id": prospect_data.vaga_id,
                        "error": "Vaga não encontrada"
                    })
                    continue
            
            # Cria o prospect
            db_prospect = Prospect(**prospect_data.model_dump())
            session.add(db_prospect)
            created_count += 1
            
        except Exception as e:
            errors.append({
                "index": idx,
                "vaga_id": prospect_data.vaga_id,
                "nome": prospect_data.nome,
                "error": str(e)
            })
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar prospects: {str(e)}"
        )
    
    return {
        "message": f"Processamento concluído",
        "created": created_count,
        "total": len(prospects_data),
        "errors": errors
    }


@router.put('/bulk-update-situacao', response_model=dict)
def bulk_update_situacao(
    prospect_ids: List[int],
    nova_situacao: str,
    comentario: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Atualiza a situação de múltiplos prospects em lote.
    
    Argumentos:
        prospect_ids: Lista de IDs dos prospects
        nova_situacao: Nova situação para os prospects
        comentario: Comentário opcional
        session: Sessão do banco de dados
        current_user: Usuário autenticado
    """
    updated_count = 0
    errors = []
    
    for prospect_id in prospect_ids:
        try:
            prospect = session.scalar(
                select(Prospect).where(Prospect.id == prospect_id)
            )
            
            if not prospect:
                errors.append({
                    "prospect_id": prospect_id,
                    "error": "Prospect não encontrado"
                })
                continue
            
            prospect.situacao_candidado = nova_situacao
            if comentario:
                prospect.comentario = comentario
            
            updated_count += 1
            
        except Exception as e:
            errors.append({
                "prospect_id": prospect_id,
                "error": str(e)
            })
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar prospects: {str(e)}"
        )
    
    return {
        "message": f"Atualização concluída",
        "updated": updated_count,
        "total": len(prospect_ids),
        "errors": errors
    }