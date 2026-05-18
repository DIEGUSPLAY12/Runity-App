from pydantic import BaseModel, Field

class StatsSummary(BaseModel):
    total_distance_km: float
    total_duration_sec: int
    total_sessions: int
    avg_pace: float

class WeeklyStatsResponse(BaseModel):
    week: str = Field(..., description="Semana en formato YYYY-WW")
    total_distance_km: float
    total_duration_sec: int
    total_sessions: int
    avg_pace: float
    
class DailyStatsResponse(BaseModel):
    active_time_sec: int
    estimated_calories: float
    sessions_count: int

class StreakStatsResponse(BaseModel):
    current_streak: int
    longest_streak: int
