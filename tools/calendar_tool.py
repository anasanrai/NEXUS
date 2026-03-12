"""
Calendar Tool
Create and manage calendar events.
"""

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class CalendarTool:
    """Calendar operations."""
    
    async def create_event(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        description: str = "",
        attendees: list = None,
    ) -> Dict[str, Any]:
        """
        Create calendar event.
        
        Args:
            title: Event title
            start_time: Start datetime
            end_time: End datetime
            description: Event description
            attendees: List of attendee emails
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from memory.entities import save_event
            
            event = {
                "title": title,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "description": description,
                "attendees": attendees or [],
            }
            
            result = await save_event(event)
            logger.info(f"Event created: {title}")
            
            return {
                "success": True,
                "result": result,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Create event failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def get_events(self, days: int = 7) -> Dict[str, Any]:
        """
        Get upcoming events.
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from memory.entities import get_upcoming_events
            
            result = await get_upcoming_events(days)
            
            return {
                "success": True,
                "result": result,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Get events failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def cancel_event(self, event_id: str) -> Dict[str, Any]:
        """
        Cancel event.
        
        Args:
            event_id: Event ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from memory.entities import delete_event
            
            await delete_event(event_id)
            logger.info(f"Event cancelled: {event_id}")
            
            return {
                "success": True,
                "result": f"Cancelled {event_id}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Cancel event failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
calendar_tool = CalendarTool()
