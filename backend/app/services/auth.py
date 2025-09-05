from typing import Optional
from datetime import datetime, timedelta, timezone
import os

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
import bcrypt

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user"""
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID format")
    
    # Improved database query with error handling
    try:
        user = db.query(User).filter(User.id == user_id_int).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log only critical errors, not connection issues, and only in development
        error_msg = str(e).lower()
        is_connection_error = any(conn_error in error_msg for conn_error in 
                                ['connection failed', 'network is unreachable', 'timeout', 
                                 'connection refused', 'connection reset', 'pool timeout'])
        
        if not is_connection_error and not (os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID")):
            import logging
            logging.error(f"Database error in get_current_user: {str(e)}")
        
        # For connection errors, return 503; for other DB errors, return 401
        if is_connection_error:
            raise HTTPException(status_code=503, detail="Service temporarily unavailable")
        else:
            raise HTTPException(status_code=401, detail="Authentication failed")


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password"""
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    except Exception as e:
        # Log only critical errors, not connection issues, and only in development
        error_msg = str(e).lower()
        is_connection_error = any(conn_error in error_msg for conn_error in 
                                ['connection failed', 'network is unreachable', 'timeout', 
                                 'connection refused', 'connection reset', 'pool timeout'])
        
        if not is_connection_error and not (os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID")):
            import logging
            logging.error(f"Database error in authenticate_user: {str(e)}")
        
        return None
