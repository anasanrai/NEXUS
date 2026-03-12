"""
Long-Term Memory using Supabase + pgvector
Semantic search and persistent storage of important information.
"""

import logging
from typing import Dict, Any, List, Optional
import json

from config import config

logger = logging.getLogger(__name__)


class LongTermMemory:
    """Supabase-based long-term semantic memory."""
    
    def __init__(self):
        """Initialize Supabase client."""
        try:
            from supabase import create_client
            self.supabase = create_client(
                config.database.supabase_url,
                config.database.supabase_key,
            )
            logger.info("Connected to Supabase")
        except Exception as e:
            logger.error(f"Supabase connection failed: {str(e)}")
            self.supabase = None
    
    async def store(
        self,
        content: str,
        metadata: Optional[Dict] = None,
        embedding: Optional[List[float]] = None,
    ) -> bool:
        """
        Store content with optional embedding.
        
        Args:
            content: Text content to store
            metadata: Optional metadata
            embedding: Optional vector embedding
            
        Returns:
            bool: Success
        """
        if not self.supabase:
            return False
        
        try:
            # Generate embedding if not provided
            if not embedding:
                embedding = await self._generate_embedding(content)
            
            record = {
                "content": content,
                "metadata": metadata or {},
                "embedding": embedding,
            }
            
            result = self.supabase.table("memories").insert(record).execute()
            logger.info(f"Stored to long-term memory: {content[:50]}")
            return True
            
        except Exception as e:
            logger.error(f"Store memory failed: {str(e)}")
            return False
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """
        Semantic search in memory.
        
        Args:
            query: Search query
            limit: Max results
            threshold: Similarity threshold
            
        Returns:
            List[Dict]: Search results
        """
        if not self.supabase:
            return []
        
        try:
            # Generate query embedding
            query_embedding = await self._generate_embedding(query)
            
            # Search with pgvector
            result = self.supabase.rpc(
                "search_memories",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": threshold,
                    "match_count": limit,
                },
            ).execute()
            
            return result.data if hasattr(result, "data") else []
            
        except Exception as e:
            logger.error(f"Memory search failed: {str(e)}")
            return []
    
    async def forget(self, memory_id: str) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: Memory ID
            
        Returns:
            bool: Success
        """
        if not self.supabase:
            return False
        
        try:
            self.supabase.table("memories").delete().eq("id", memory_id).execute()
            logger.info(f"Deleted memory: {memory_id}")
            return True
        except Exception as e:
            logger.error(f"Forget memory failed: {str(e)}")
            return False
    
    async def get_all(self, limit: int = 100) -> List[Dict]:
        """Get all memories."""
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table("memories").select("*").limit(limit).execute()
            return result.data if hasattr(result, "data") else []
        except Exception as e:
            logger.error(f"Get memories failed: {str(e)}")
            return []
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            List[float]: Vector embedding
        """
        try:
            # Use Anthropic Claude to generate embeddings
            # For now, return placeholder
            import hashlib
            # Simple hash-based embedding (replace with real embedding model)
            hash_bytes = hashlib.sha256(text.encode()).digest()
            embedding = [float(b) / 255.0 for b in hash_bytes[:32]]
            return embedding
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            return [0.0] * 32


# Global instance
long_term_memory = LongTermMemory()
