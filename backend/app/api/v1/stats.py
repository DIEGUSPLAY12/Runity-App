from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session as DbSession
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.domain import Session, Profile
from app.schemas.stats import StatsSummary, WeeklyStatsResponse, DailyStatsResponse, StreakStatsResponse

router = APIRouter()

@router.get("/summary", response_model=StatsSummary)
def get_stats_summary(
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Devuelve un resumen acumulado de toda la actividad del usuario.
    """
    stats = db.query(
        func.count(Session.id).label("total_sessions"),
        func.sum(Session.distance_meters).label("total_distance_m"),
        func.sum(Session.duration_seconds).label("total_duration_sec")
    ).filter(
        Session.profile_id == current_user_id
    ).first()

    total_sessions = stats.total_sessions or 0

    if total_sessions == 0:
        return StatsSummary(
            total_distance_km=0.0,
            total_duration_sec=0,
            total_sessions=0,
            avg_pace=0.0
        )

    total_distance_m = stats.total_distance_m or 0
    total_duration_sec = stats.total_duration_sec or 0
    total_distance_km = total_distance_m / 1000.0

    avg_pace = 0.0
    if total_distance_km > 0:
        avg_pace = total_duration_sec / total_distance_km

    return StatsSummary(
        total_distance_km=round(total_distance_km, 2),
        total_duration_sec=total_duration_sec,
        total_sessions=total_sessions,
        avg_pace=round(avg_pace, 2)
    )


@router.get("/weekly", response_model=WeeklyStatsResponse)
def get_stats_weekly(
    week: str = Query(..., description="Semana en formato YYYY-WW, ej: 2026-11"),
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Exponer métricas agregadas de progreso semanal.
    """
    try:
        start_of_week = datetime.strptime(f"{week}-1", "%Y-%W-%w")
        end_of_week = start_of_week + timedelta(days=7)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato de semana inválido. Usa YYYY-WW (ej: 2026-11)"
        )

    stats = db.query(
        func.count(Session.id).label("total_sessions"),
        func.sum(Session.distance_meters).label("total_distance_m"),
        func.sum(Session.duration_seconds).label("total_duration_sec")
    ).filter(
        Session.profile_id == current_user_id,
        Session.start_time >= start_of_week,
        Session.start_time < end_of_week
    ).first()

    total_sessions = stats.total_sessions or 0

    if total_sessions == 0:
        return WeeklyStatsResponse(
            week=week,
            total_distance_km=0.0,
            total_duration_sec=0,
            total_sessions=0,
            avg_pace=0.0
        )

    total_distance_m = stats.total_distance_m or 0
    total_duration_sec = stats.total_duration_sec or 0
    total_distance_km = total_distance_m / 1000.0

    avg_pace = 0.0
    if total_distance_km > 0:
        avg_pace = total_duration_sec / total_distance_km

    return WeeklyStatsResponse(
        week=week,
        total_distance_km=round(total_distance_km, 2),
        total_duration_sec=total_duration_sec,
        total_sessions=total_sessions,
        avg_pace=round(avg_pace, 2)
    )


@router.get("/daily", response_model=DailyStatsResponse)
def get_stats_daily(
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Devuelve el resumen del día actual para la pantalla Home.
    Calcula calorías estimadas usando la fórmula MET.
    """
    profile = db.query(Profile).filter(Profile.id == current_user_id).first()
    weight = 70.0
    if profile and profile.weight_kg:
        weight = profile.weight_kg

    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    sessions = db.query(Session).filter(
        Session.profile_id == current_user_id,
        Session.start_time >= start_of_day,
        Session.start_time <= end_of_day
    ).all()

    if not sessions:
        return DailyStatsResponse(
            active_time_sec=0,
            estimated_calories=0.0,
            sessions_count=0
        )

    met_values = {
        "running": 9.8,
        "cycling": 7.5,
        "walking": 3.5
    }
    
    active_time_sec = 0
    estimated_calories = 0.0

    for s in sessions:
        active_time_sec += s.duration_seconds
        met = met_values.get(s.sport.lower(), 5.0)
        hours = s.duration_seconds / 3600.0
        estimated_calories += met * weight * hours

    return DailyStatsResponse(
        active_time_sec=active_time_sec,
        estimated_calories=round(estimated_calories, 2),
        sessions_count=len(sessions)
    )

@router.get("/streak", response_model=StreakStatsResponse)
def get_stats_streak(
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Devuelve la racha actual de días consecutivos entrenando y la mejor racha histórica.
    """
    sessions = db.query(Session.start_time).filter(
        Session.profile_id == current_user_id
    ).order_by(Session.start_time.desc()).all()

    if not sessions:
        return StreakStatsResponse(current_streak=0, longest_streak=0)

    unique_dates = sorted(list({s.start_time.date() for s in sessions}), reverse=True)

    if not unique_dates:
        return StreakStatsResponse(current_streak=0, longest_streak=0)

    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    current_streak = 0
    
    if today in unique_dates:
        current_date = today
        current_streak = 1
    elif yesterday in unique_dates:
        current_date = yesterday
        current_streak = 1
    else:
        current_date = None

    if current_streak > 0:
        check_date = current_date - timedelta(days=1)
        for d in unique_dates:
            if d >= current_date:
                continue
            if d == check_date:
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break

    longest_streak = 0
    temp_streak = 1
    
    for i in range(len(unique_dates) - 1):
        if unique_dates[i] - timedelta(days=1) == unique_dates[i+1]:
            temp_streak += 1
        else:
            if temp_streak > longest_streak:
                longest_streak = temp_streak
            temp_streak = 1
            
    if temp_streak > longest_streak:
        longest_streak = temp_streak

    if len(unique_dates) == 1:
        longest_streak = 1

    return StreakStatsResponse(
        current_streak=current_streak,
        longest_streak=longest_streak
    )