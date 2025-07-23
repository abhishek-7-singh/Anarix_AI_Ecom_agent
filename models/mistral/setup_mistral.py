"""
Mistral setup utilities and configuration management
"""
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MistralSetup:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else Path(__file__).parent / "model_config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "model_name": "mistral:7b-instruct",
            "api_settings": {
                "temperature": 0.7,
                "max_tokens": 2048,
                "top_p": 0.9
            }
        }
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values"""
        try:
            self._deep_update(self.config, updates)
            return self.save_config()
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            return False
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict):
        """Deep update dictionary"""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def get_model_settings(self) -> Dict[str, Any]:
        """Get model-specific settings"""
        return {
            "model_name": self.config.get("model_name", "mistral:7b-instruct"),
            "temperature": self.config.get("api_settings", {}).get("temperature", 0.7),
            "max_tokens": self.config.get("api_settings", {}).get("max_tokens", 2048),
            "top_p": self.config.get("api_settings", {}).get("top_p", 0.9),
        }
    
    def get_prompts(self) -> Dict[str, str]:
        """Get configured prompts"""
        return self.config.get("prompts", {})
    
    def get_database_schema(self) -> Dict[str, Any]:
        """Get database schema information"""
        return self.config.get("database_schema", {})
    
    def validate_setup(self) -> bool:
        """Validate Mistral setup"""
        logger.info("Validating Mistral setup...")
        
        # Check if Ollama is available
        if not self._check_ollama():
            return False
        
        # Check if model is available
        model_name = self.config.get("model_name", "mistral:7b-instruct")
        if not self._check_model(model_name):
            return False
        
        # Test model response
        if not self._test_model_response(model_name):
            return False
        
        logger.info("✅ Mistral setup validation successful!")
        return True
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("✅ Ollama is available")
                return True
            else:
                logger.error("❌ Ollama not working properly")
                return False
        except FileNotFoundError:
            logger.error("❌ Ollama not installed")
            return False
    
    def _check_model(self, model_name: str) -> bool:
        """Check if specific model is available"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                if model_name in result.stdout:
                    logger.info(f"✅ Model {model_name} is available")
                    return True
                else:
                    logger.error(f"❌ Model {model_name} not found")
                    logger.info("Available models:")
                    logger.info(result.stdout)
                    return False
            else:
                logger.error("Failed to list Ollama models")
                return False
                
        except Exception as e:
            logger.error(f"Error checking model: {e}")
            return False
    
    def _test_model_response(self, model_name: str) -> bool:
        """Test model response"""
        try:
            test_prompt = "What is 2+2? Answer briefly."
            
            cmd = ['ollama', 'run', model_name, test_prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0 and result.stdout.strip():
                logger.info("✅ Model response test successful")
                return True
            else:
                logger.error("❌ Model response test failed")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Model response test timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Error testing model response: {e}")
            return False

def setup_mistral_environment():
    """Setup complete Mistral environment"""
    setup = MistralSetup()
    return setup.validate_setup()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = setup_mistral_environment()
    sys.exit(0 if success else 1)
