"""
Social Media Tool
Post to Twitter, LinkedIn, Instagram with scheduling.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SocialTool:
    """Social media posting."""
    
    async def post_twitter(
        self,
        text: str,
        media_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Post to Twitter.
        
        Args:
            text: Tweet text
            media_url: Optional media URL
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from config import config
            import tweepy
            
            auth = tweepy.OAuthHandler(
                config.social.twitter_api_key,
                config.social.twitter_api_secret,
            )
            auth.set_access_token(
                config.social.twitter_access_token,
                config.social.twitter_access_secret,
            )
            
            api = tweepy.API(auth)
            
            if media_url:
                # Download and upload media
                import requests
                response = requests.get(media_url)
                with open("/tmp/tweet_media.jpg", "wb") as f:
                    f.write(response.content)
                media = api.media_upload("/tmp/tweet_media.jpg")
                tweet = api.update_status(text, media_ids=[media.media_id])
            else:
                tweet = api.update_status(text)
            
            logger.info(f"Tweet posted: {tweet.id}")
            return {
                "success": True,
                "result": {"tweet_id": tweet.id},
                "error": None,
            }
        except Exception as e:
            logger.error(f"Twitter post failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def post_linkedin(
        self,
        text: str,
        image_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Post to LinkedIn.
        
        Args:
            text: Post text
            image_url: Optional image URL
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from config import config
            import httpx
            
            headers = {
                "Authorization": f"Bearer {config.social.linkedin_access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "commentary": text,
                "visibility": "PUBLIC",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.linkedin.com/v2/ugcPosts",
                    headers=headers,
                    json=payload,
                    timeout=15,
                )
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            logger.info("LinkedIn post created")
            return {
                "success": True,
                "result": response.json(),
                "error": None,
            }
        except Exception as e:
            logger.error(f"LinkedIn post failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def post_instagram(
        self,
        image_url: str,
        caption: str,
    ) -> Dict[str, Any]:
        """
        Post to Instagram.
        
        Args:
            image_url: Image URL
            caption: Post caption
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from config import config
            import httpx
            
            headers = {
                "Authorization": f"Bearer {config.social.instagram_access_token}",
            }
            
            data = {
                "image_url": image_url,
                "caption": caption,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://graph.instagram.com/me/media",
                    headers=headers,
                    data=data,
                    timeout=15,
                )
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            logger.info("Instagram post created")
            return {
                "success": True,
                "result": response.json(),
                "error": None,
            }
        except Exception as e:
            logger.error(f"Instagram post failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def schedule_post(
        self,
        platform: str,
        content: str,
        scheduled_time: datetime,
    ) -> Dict[str, Any]:
        """
        Schedule post for later.
        
        Args:
            platform: Social platform (twitter, linkedin, instagram)
            content: Post content
            scheduled_time: When to post
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from memory.short_term import add_scheduled_post
            
            result = await add_scheduled_post(
                platform=platform,
                content=content,
                scheduled_time=scheduled_time,
            )
            
            return {
                "success": True,
                "result": {"scheduled": scheduled_time},
                "error": None,
            }
        except Exception as e:
            logger.error(f"Schedule post failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
social_tool = SocialTool()
