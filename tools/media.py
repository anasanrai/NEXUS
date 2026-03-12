"""
Media Generation Tool
Generate images, videos, and add captions.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MediaTool:
    """Media generation and processing."""
    
    async def generate_image(self, prompt: str) -> Dict[str, Any]:
        """
        Generate image from text prompt via Replicate.
        
        Args:
            prompt: Image description
            
        Returns:
            dict: {success, result (image_url), error}
        """
        try:
            import replicate
            from config import config
            
            replicate.api.token = config.media.replicate_api_token
            
            output = replicate.run(
                "stability-ai/stable-diffusion-3",
                input={
                    "prompt": prompt,
                    "num_outputs": 1,
                },
            )
            
            logger.info(f"Image generated: {prompt[:50]}")
            return {
                "success": True,
                "result": {"image_url": output[0]},
                "error": None,
            }
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def generate_video(self, prompt: str) -> Dict[str, Any]:
        """
        Generate video using Kling API.
        
        Args:
            prompt: Video description
            
        Returns:
            dict: {success, result (video_url), error}
        """
        try:
            import httpx
            
            headers = {
                "Authorization": "Bearer YOUR_KLING_API_KEY",
                "Content-Type": "application/json",
            }
            
            payload = {
                "prompt": prompt,
                "duration": 6,
                "fps": 24,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.klingai.com/v1/videos/text2video",
                    headers=headers,
                    json=payload,
                    timeout=30,
                )
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            logger.info(f"Video generation started: {prompt[:50]}")
            return {
                "success": True,
                "result": response.json(),
                "error": None,
            }
        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def text_to_speech(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Convert text to speech using Fish Audio.
        
        Args:
            text: Text to convert
            language: Language code
            
        Returns:
            dict: {success, result (audio_url), error}
        """
        try:
            import httpx
            from config import config
            
            headers = {
                "Authorization": f"Bearer {config.media.fish_audio_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "text": text,
                "language": language,
                "voice_id": "default",
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.fish.audio/v1/tts",
                    headers=headers,
                    json=payload,
                    timeout=30,
                )
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "result": None,
                    "error": f"API error: {response.status_code}",
                }
            
            logger.info(f"Audio generated: {text[:50]}")
            return {
                "success": True,
                "result": response.json(),
                "error": None,
            }
        except Exception as e:
            logger.error(f"Text to speech failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def add_captions(self, video_path: str) -> Dict[str, Any]:
        """
        Add captions to video using Whisper.
        
        Args:
            video_path: Path to video file
            
        Returns:
            dict: {success, result (captions), error}
        """
        try:
            import whisper
            
            model = whisper.load_model("base")
            result = model.transcribe(video_path)
            
            logger.info(f"Captions generated for {video_path}")
            return {
                "success": True,
                "result": {
                    "text": result["text"],
                    "segments": result["segments"],
                },
                "error": None,
            }
        except Exception as e:
            logger.error(f"Add captions failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
media_tool = MediaTool()
