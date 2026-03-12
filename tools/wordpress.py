"""
WordPress Blog Management Tool
Create, edit, and publish blog posts.
"""

import logging
from typing import Dict, Any, Optional

from config import config

logger = logging.getLogger(__name__)


class WordPressTool:
    """WordPress content management."""
    
    def __init__(self):
        """Initialize WordPress tool."""
        self.url = config.wordpress.wordpress_url
        self.user = config.wordpress.wordpress_user
        self.password = config.wordpress.wordpress_password
    
    async def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        tags: Optional[list] = None,
        categories: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Create blog post.
        
        Args:
            title: Post title
            content: Post content (HTML)
            status: Post status (draft, publish)
            tags: Post tags
            categories: Post categories
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from wordpress_xmlrpc import Client, WordPressPost
            from wordpress_xmlrpc.methods import posts
            
            client = Client(self.url, self.user, self.password)
            
            post = WordPressPost()
            post.title = title
            post.content = content
            post.post_status = status
            
            if tags:
                post.terms_names = {"post_tag": tags}
            if categories:
                post.terms_names = {"category": categories}
            
            post_id = client.call(posts.NewPost(post))
            
            logger.info(f"Post created: {post_id}")
            return {
                "success": True,
                "result": {"post_id": post_id},
                "error": None,
            }
        except Exception as e:
            logger.error(f"Create post failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def get_posts(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get blog posts.
        
        Args:
            limit: Max posts to retrieve
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from wordpress_xmlrpc import Client
            from wordpress_xmlrpc.methods import posts
            
            client = Client(self.url, self.user, self.password)
            
            wp_posts = client.call(posts.GetPosts({"limit": limit}))
            
            results = []
            for post in wp_posts:
                results.append({
                    "id": post.id,
                    "title": post.title,
                    "status": post.post_status,
                    "date": str(post.date),
                })
            
            return {
                "success": True,
                "result": results,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Get posts failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def publish_post(self, post_id: int) -> Dict[str, Any]:
        """
        Publish post.
        
        Args:
            post_id: Post ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from wordpress_xmlrpc import Client, WordPressPost
            from wordpress_xmlrpc.methods import posts
            
            client = Client(self.url, self.user, self.password)
            
            post = client.call(posts.GetPost(post_id))
            post.post_status = "publish"
            client.call(posts.EditPost(post_id, post))
            
            logger.info(f"Post published: {post_id}")
            return {
                "success": True,
                "result": f"Published post {post_id}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Publish post failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def delete_post(self, post_id: int) -> Dict[str, Any]:
        """
        Delete post.
        
        Args:
            post_id: Post ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            from wordpress_xmlrpc import Client
            from wordpress_xmlrpc.methods import posts
            
            client = Client(self.url, self.user, self.password)
            client.call(posts.DeletePost(post_id))
            
            logger.info(f"Post deleted: {post_id}")
            return {
                "success": True,
                "result": f"Deleted post {post_id}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Delete post failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
wordpress_tool = WordPressTool()
