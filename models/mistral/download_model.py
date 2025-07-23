#!/usr/bin/env python3
"""
Script to download and setup Mistral model locally
"""
import os
import sys
import json
import subprocess
import requests
from pathlib import Path
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model configurations
MISTRAL_MODELS = {
    "mistral-7b-instruct": {
        "name": "mistral:7b-instruct",
        "size": "4.1GB",
        "description": "Mistral 7B Instruct model optimized for instruction following",
        "recommended": True
    },
    "mistral-7b": {
        "name": "mistral:7b",
        "size": "4.1GB", 
        "description": "Base Mistral 7B model",
        "recommended": False
    },
    "mistral-small": {
        "name": "mistral-small",
        "size": "12GB",
        "description": "Mistral Small model for better performance",
        "recommended": False
    }
}

class MistralDownloader:
    def __init__(self, model_dir: Optional[str] = None):
        self.model_dir = Path(model_dir) if model_dir else Path(__file__).parent
        self.config_path = self.model_dir / "model_config.json"
        
    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(
                ['ollama', '--version'], 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode == 0:
                logger.info(f"Ollama found: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            pass
        
        logger.error("Ollama not found. Please install Ollama first.")
        return False
    
    def install_ollama(self) -> bool:
        """Install Ollama automatically"""
        logger.info("Installing Ollama...")
        
        try:
            # For Linux/Mac
            if sys.platform in ['linux', 'darwin']:
                install_cmd = 'curl -fsSL https://ollama.ai/install.sh | sh'
                result = subprocess.run(
                    install_cmd, 
                    shell=True, 
                    capture_output=True, 
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if result.returncode == 0:
                    logger.info("Ollama installed successfully!")
                    return True
                else:
                    logger.error(f"Failed to install Ollama: {result.stderr}")
                    return False
            
            # For Windows
            elif sys.platform == 'win32':
                logger.info("Please install Ollama manually from: https://ollama.ai/download/windows")
                return False
                
        except Exception as e:
            logger.error(f"Error installing Ollama: {e}")
            return False
    
    def download_model(self, model_key: str = "mistral-7b-instruct") -> bool:
        """Download specified Mistral model via Ollama"""
        
        if model_key not in MISTRAL_MODELS:
            logger.error(f"Unknown model: {model_key}")
            logger.info(f"Available models: {list(MISTRAL_MODELS.keys())}")
            return False
        
        model_info = MISTRAL_MODELS[model_key]
        model_name = model_info["name"]
        
        logger.info(f"Downloading {model_name} ({model_info['size']})...")
        logger.info(f"Description: {model_info['description']}")
        
        try:
            # Pull the model using Ollama
            cmd = ['ollama', 'pull', model_name]
            
            # Run with real-time output - FIXED VERSION
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',        # Fixed: Added explicit UTF-8 encoding
                errors='replace',        # Fixed: Handle any decode errors gracefully
                bufsize=1
            )
            
            # Stream output in real-time
            for line in process.stdout:
                print(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                logger.info(f"Successfully downloaded {model_name}")
                self._save_model_config(model_key, model_info)
                return True
            else:
                logger.error(f"Failed to download {model_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading model: {e}")
            return False
    
    def list_available_models(self) -> Dict[str, Any]:
        """List available models"""
        try:
            result = subprocess.run(
                ['ollama', 'list'], 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                logger.info("Installed models:")
                print(result.stdout)
                return {"installed": result.stdout.strip()}
            else:
                logger.error("Failed to list models")
                return {}
                
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return {}
    
    def verify_model(self, model_name: str = "mistral:7b-instruct") -> bool:
        """Verify that the model is working"""
        try:
            logger.info(f"Testing {model_name}...")
            
            cmd = ['ollama', 'run', model_name, 'Hello, can you help me?']
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0 and result.stdout.strip():
                logger.info(f"Model {model_name} is working correctly!")
                logger.info(f"Test response: {result.stdout.strip()[:100]}...")
                return True
            else:
                logger.error(f"Model {model_name} test failed")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Model test timed out")
            return False
        except Exception as e:
            logger.error(f"Error testing model: {e}")
            return False
    
    def _save_model_config(self, model_key: str, model_info: Dict[str, Any]):
        """Save model configuration"""
        config = {
            "model_key": model_key,
            "model_name": model_info["name"],
            "downloaded_at": __import__('datetime').datetime.now().isoformat(),
            "size": model_info["size"],
            "description": model_info["description"]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:  # Fixed: Added UTF-8 encoding
            json.dump(config, f, indent=2)
        
        logger.info(f"Model configuration saved to {self.config_path}")
    
    def setup_complete_environment(self) -> bool:
        """Complete setup of Mistral environment"""
        logger.info("Setting up complete Mistral environment...")
        
        # Check if Ollama is installed
        if not self.check_ollama_installed():
            if not self.install_ollama():
                return False
        
        # Download recommended model
        if not self.download_model("mistral-7b-instruct"):
            return False
        
        # Verify model works
        if not self.verify_model("mistral:7b-instruct"):
            return False
        
        logger.info("✅ Mistral environment setup complete!")
        return True

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Download and setup Mistral model")
    parser.add_argument("--model", default="mistral-7b-instruct", 
                       choices=list(MISTRAL_MODELS.keys()),
                       help="Model to download")
    parser.add_argument("--list", action="store_true", 
                       help="List available models")
    parser.add_argument("--verify", action="store_true",
                       help="Verify model is working")
    parser.add_argument("--setup-all", action="store_true",
                       help="Complete environment setup")
    
    args = parser.parse_args()
    
    downloader = MistralDownloader()
    
    if args.list:
        print("Available models:")
        for key, info in MISTRAL_MODELS.items():
            status = "⭐ Recommended" if info["recommended"] else ""
            print(f"  {key}: {info['description']} ({info['size']}) {status}")
        downloader.list_available_models()
        return
    
    if args.setup_all:
        success = downloader.setup_complete_environment()
        sys.exit(0 if success else 1)
    
    if args.verify:
        success = downloader.verify_model()
        sys.exit(0 if success else 1)
    
    # Download specified model
    success = downloader.download_model(args.model)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
