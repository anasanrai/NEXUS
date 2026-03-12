"""
Short-Term Memory using Redis
Stores session context and recent messages for fast access.
"""

import logging
import json
from typing import Dict, Any, List, Optional
import redis
from datetime import datetime, timedelta

from config import config

logger = logging.getLogger(__name__)


class ShortTermMemory:
    """Redis-based short-term memory for session context."""
    
    def __init__(self):
        """Initialize Redis connection."""
        try:
            self.redis = redis.from_url(config.database.redis_url)
            self.redis.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Redis connection failed: {str(e)}")
            self.redis = None
    
    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None,
    ) -> bool:
        """
        Add message to session history.
        
        Args:
            session_id: Session ID
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata
            
        Returns:
            bool: Success
        """
        if not self.redis:
            return False
        
        try:
            key = f"session:{session_id}:messages"
            message = {
                "timestamp": datetime.now().isoformat(),
                "role": role,
                "content": content,
                "metadata": metadata or {},
            }
            
            self.redis.lpush(key, json.dumps(message))
            # Keep only last 100 messages and expire after 24 hours
            self.redis.ltrim(key, 0, 99)
            self.redis.expire(key, 86400)
            
            return True
        except Exception as e:
            logger.error(f"Add message failed: {str(e)}")
            return False
    
    async def get_history(
        self,
        session_id: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history.
        
        Args:
            session_id: Session ID
            limit: Max messages to retrieve
            
        Returns:
            List[Dict]: Messages in chronological order
        """
        if not self.redis:
            return []
        
        try:
            key = f"session:{session_id}:messages"
            messages = self.redis.lrange(key, 0, limit - 1)
            
            # Reverse to get chronological order
            result = []
            for msg in reversed(messages):
                result.append(json.loads(msg))
            return result
            
        except Exception as e:
            logger.error(f"Get history failed: {str(e)}")
            return []
    
    async def clear(self, session_id: str) -> bool:
        """
        Clear session history.
        
        Args:
            session_id: Session ID
            
        Returns:
            bool: Success
        """
        if not self.redis:
            return False
        
        try:
            key = f"session:{session_id}:messages"
            self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Clear history failed: {str(e)}")
            return False
    
    async def set_context(
        self,
        session_id: str,
        key: str,
        value: Any,
        ttl: int = 3600,
    ) -> bool:
        """
        Set context value for session.
        
        Args:
            session_id: Session ID
            key: Context key
            value: Context value
            ttl: Time to live in seconds
            
        Returns:
            bool: Success
        """
        if not self.redis:
            return False
        
        try:
            redis_key = f"session:{session_id}:context:{key}"
            self.redis.setex(
                redis_key,
                ttl,
                json.dumps(value) if not isinstance(value, str) else value,
            )
            return True
        except Exception as e:
            logger.error(f"Set context failed: {str(e)}")
            return False
    
    async def get_context(self, session_id: str, key: str) -> Optional[Any]:
        """
        Get context value.
        
        Args:
            session_id: Session ID
            key: Context key
            
        Returns:
            Any: Context value or None
        """
        if not self.redis:
            return None
        
        try:
            redis_key = f"session:{session_id}:context:{key}"
            value = self.redis.get(redis_key)
            if value:
                try:
                    return json.loads(value)
                except:
                    return value.decode()
            return None
        except Exception as e:
            logger.error(f"Get context failed: {str(e)}")
            return None
    
    async def add_scheduled_post(
        self,
        platform: str,
        content: str,
        scheduled_time: datetime,
    ) -> bool:
        """
        Add scheduled post.
        
        Args:
            platform: Social platform
            content: Post content
            scheduled_time: When to post
            
        Returns:
            bool: Success
        """
        if not self.redis:
            return False
        
        try:
            key = f"scheduled_posts:{scheduled_time.date()}"
            post = {
                "platform": platform,
                "content": content,
                "time": scheduled_time.isoformat(),
                "created": datetime.now().isoformat(),
            }
            
            self.redis.lpush(key, json.dumps(post))
            return True
        except Exception as e:
            logger.error(f"Add scheduled post failed: {str(e)}")
            return False
    
    async def get_scheduled_posts(self, date: datetime = None) -> List[Dict]:
        """Get scheduled posts for date."""
        if not self.redis:
            return []
        
        date = date or datetime.now()
        key = f"scheduled_posts:{date.date()}"
        
        try:
            posts = self.redis.lrange(key, 0, -1)
            return [json.loads(p) for p in posts]
        except Exception as e:
            logger.error(f"Get scheduled posts failed: {str(e)}")
            return []


# Global instance
short_term_memory = ShortTermMemory()
