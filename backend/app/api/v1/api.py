from fastapi import APIRouter
from app.api.v1 import profiles
from app.api.v1 import sessions
from app.api.v1 import stats
from app.api.v1 import friends
from app.api.v1 import users
from app.api.v1 import feed
from app.api.v1 import auth
from app.api.v1 import challenges
from app.api.v1 import notifications
from app.api.v1 import presence

api_router = APIRouter()

@api_router.get("/health")
def health_check():
    return {"status": "ok", "message": "Hello Runity"}

api_router.include_router(profiles.router, prefix="/profile", tags=["Profile"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(stats.router, prefix="/stats", tags=["Stats"])
api_router.include_router(friends.router, prefix="/friends", tags=["Friends"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(feed.router, prefix="/feed", tags=["Feed"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(presence.router, prefix="/presence", tags=["Presence"])
