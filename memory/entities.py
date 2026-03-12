"""
Entity Management
Store and retrieve business entities: clients, tasks, revenue, events.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from config import config

logger = logging.getLogger(__name__)


class EntityManager:
    """Manage business entities in Supabase."""
    
    def __init__(self):
        """Initialize entity manager."""
        try:
            from supabase import create_client
            self.supabase = create_client(
                config.database.supabase_url,
                config.database.supabase_key,
            )
            logger.info("Connected to Supabase for entities")
        except Exception as e:
            logger.error(f"Supabase connection failed: {str(e)}")
            self.supabase = None
    
    async def save_client(self, data: Dict[str, Any]) -> bool:
        """
        Save client information.
        
        Args:
            data: Client data
            
        Returns:
            bool: Success
        """
        if not self.supabase:
            return False
        
        try:
            self.supabase.table("clients").insert(data).execute()
            logger.info(f"Client saved: {data.get('name')}")
            return True
        except Exception as e:
            logger.error(f"Save client failed: {str(e)}")
            return False
    
    async def get_clients(self, limit: int = 50) -> List[Dict]:
        """
        Get all clients.
        
        Args:
            limit: Max results
            
        Returns:
            List[Dict]: Client records
        """
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table("clients").select("*").limit(limit).execute()
            return result.data if hasattr(result, "data") else []
        except Exception as e:
            logger.error(f"Get clients failed: {str(e)}")
            return []
    
    async def save_task(self, data: Dict[str, Any]) -> bool:
        """
        Save task.
        
        Args:
            data: Task data
            
        Returns:
            bool: Success
        """
        if not self.supabase:
            return False
        
        try:
            self.supabase.table("tasks").insert(data).execute()
            logger.info(f"Task saved: {data.get('title')}")
            return True
        except Exception as e:
            logger.error(f"Save task failed: {str(e)}")
            return False
    
    async def get_pending_tasks(self) -> List[Dict]:
        """Get pending tasks."""
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table("tasks").select("*").eq(
                "status", "pending"
            ).execute()
            return result.data if hasattr(result, "data") else []
        except Exception as e:
            logger.error(f"Get pending tasks failed: {str(e)}")
            return []
    
    async def update_task_status(self, task_id: str, status: str) -> bool:
        """Update task status."""
        if not self.supabase:
            return False
        
        try:
            self.supabase.table("tasks").update(
                {"status": status, "updated_at": datetime.now().isoformat()}
            ).eq("id", task_id).execute()
            return True
        except Exception as e:
            logger.error(f"Update task status failed: {str(e)}")
            return False
    
    async def log_revenue(
        self,
        amount: float,
        source: str,
        description: str = "",
    ) -> bool:
        """
        Log revenue transaction.
        
        Args:
            amount: Amount in USD
            source: Revenue source
            description: Transaction description
            
        Returns:
            bool: Success
        """
        if not self.supabase:
            return False
        
        try:
            record = {
                "amount": amount,
                "source": source,
                "description": description,
                "date": datetime.now().isoformat(),
            }
            self.supabase.table("revenue").insert(record).execute()
            logger.info(f"Revenue logged: ${amount} from {source}")
            return True
        except Exception as e:
            logger.error(f"Log revenue failed: {str(e)}")
            return False
    
    async def get_revenue_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        Get revenue summary for period.
        
        Args:
            days: Days to summarize
            
        Returns:
            dict: Revenue summary
        """
        if not self.supabase:
            return {"total": 0, "by_source": {}}
        
        try:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            result = self.supabase.table("revenue").select("*").gte(
                "date", start_date
            ).execute()
            
            records = result.data if hasattr(result, "data") else []
            
            total = sum(r.get("amount", 0) for r in records)
            by_source = {}
            for r in records:
                source = r.get("source", "unknown")
                by_source[source] = by_source.get(source, 0) + r.get("amount", 0)
            
            return {
                "total": total,
                "by_source": by_source,
                "count": len(records),
                "period_days": days,
            }
        except Exception as e:
            logger.error(f"Get revenue summary failed: {str(e)}")
            return {"total": 0, "by_source": {}}
    
    async def save_event(self, data: Dict[str, Any]) -> bool:
        """Save calendar event."""
        if not self.supabase:
            return False
        
        try:
            self.supabase.table("events").insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Save event failed: {str(e)}")
            return False
    
    async def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Get upcoming events."""
        if not self.supabase:
            return []
        
        try:
            start = datetime.now().isoformat()
            end = (datetime.now() + timedelta(days=days)).isoformat()
            
            result = self.supabase.table("events").select("*").gte(
                "start_time", start
            ).lte("start_time", end).execute()
            
            return result.data if hasattr(result, "data") else []
        except Exception as e:
            logger.error(f"Get upcoming events failed: {str(e)}")
            return []
    
    async def delete_event(self, event_id: str) -> bool:
        """Delete event."""
        if not self.supabase:
            return False
        
        try:
            self.supabase.table("events").delete().eq("id", event_id).execute()
            return True
        except Exception as e:
            logger.error(f"Delete event failed: {str(e)}")
            return False


# Global instance
entity_manager = EntityManager()


# Convenience functions
async def save_client(data: Dict) -> bool:
    """Save client wrapper."""
    return await entity_manager.save_client(data)


async def get_clients() -> List[Dict]:
    """Get clients wrapper."""
    return await entity_manager.get_clients()


async def save_task(data: Dict) -> bool:
    """Save task wrapper."""
    return await entity_manager.save_task(data)


async def get_pending_tasks() -> List[Dict]:
    """Get pending tasks wrapper."""
    return await entity_manager.get_pending_tasks()


async def log_revenue(amount: float, source: str) -> bool:
    """Log revenue wrapper."""
    return await entity_manager.log_revenue(amount, source)


async def get_revenue_summary(days: int = 30) -> Dict:
    """Get revenue summary wrapper."""
    return await entity_manager.get_revenue_summary(days)


async def save_event(data: Dict) -> bool:
    """Save event wrapper."""
    return await entity_manager.save_event(data)


async def get_upcoming_events(days: int = 7) -> List[Dict]:
    """Get upcoming events wrapper."""
    return await entity_manager.get_upcoming_events(days)


async def delete_event(event_id: str) -> bool:
    """Delete event wrapper."""
    return await entity_manager.delete_event(event_id)
