"""
Mistral model utility functions
"""
import asyncio
import json
import logging
import subprocess
import time
from typing import Dict, Any, List, Optional, AsyncGenerator
from pathlib import Path

logger = logging.getLogger(__name__)

class MistralModelUtils:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else Path(__file__).parent / "model_config.json"
        self.config = self._load_config()
        self.model_name = self.config.get("model_name", "mistral:7b-instruct")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load model configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {"model_name": "mistral:7b-instruct"}
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response from Mistral model"""
        try:
            # Prepare command
            cmd = ['ollama', 'run', self.model_name]
            
            # Create subprocess
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Send prompt and get response
            stdout, stderr = await process.communicate(prompt.encode())
            
            if process.returncode == 0:
                return stdout.decode().strip()
            else:
                error_msg = stderr.decode().strip()
                logger.error(f"Model error: {error_msg}")
                raise Exception(f"Model generation failed: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def generate_streaming_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """Generate streaming response from Mistral model"""
        try:
            cmd = ['ollama', 'run', self.model_name]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Send prompt
            process.stdin.write(prompt.encode())
            await process.stdin.drain()
            process.stdin.close()
            
            # Stream output
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                
                chunk = line.decode().strip()
                if chunk:
                    yield chunk
                    
                await asyncio.sleep(0.01)  # Small delay for streaming effect
            
            await process.wait()
            
        except Exception as e:
            logger.error(f"Error in streaming generation: {e}")
            yield f"Error: {str(e)}"
    
    def generate_sql_query(self, question: str, schema_info: str) -> str:
        """Generate SQL query from natural language question"""
        
        system_prompt = self.config.get("prompts", {}).get("system_prompt", "")
        sql_prompt = self.config.get("prompts", {}).get("sql_generation_prompt", "")
        
        full_prompt = f"""
{system_prompt}

Database Schema:
{schema_info}

{sql_prompt}

Question: {question}

SQL Query:
"""
        
        try:
            # Use synchronous call for SQL generation
            result = subprocess.run(
                ['ollama', 'run', self.model_name],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                response = result.stdout.strip()
                # Extract SQL from response
                sql_query = self._extract_sql_from_response(response)
                return sql_query
            else:
                logger.error(f"SQL generation failed: {result.stderr}")
                return "SELECT 1; -- Error generating query"
                
        except subprocess.TimeoutExpired:
            logger.error("SQL generation timed out")
            return "SELECT 1; -- Query timeout"
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            return "SELECT 1; -- Error"
    
    def generate_human_response(self, question: str, sql_query: str, results: List[Dict]) -> str:
        """Generate human-readable response from query results"""
        
        response_prompt = self.config.get("prompts", {}).get("response_generation_prompt", "")
        
        results_text = json.dumps(results[:10], indent=2) if results else "No results found"
        
        full_prompt = f"""
{response_prompt}

Original Question: {question}
SQL Query Used: {sql_query}
Query Results: {results_text}

Please provide a clear, conversational answer:
"""
        
        try:
            result = subprocess.run(
                ['ollama', 'run', self.model_name],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Response generation failed: {result.stderr}")
                return "I found some data but couldn't generate a proper response."
                
        except subprocess.TimeoutExpired:
            logger.error("Response generation timed out")
            return "The query completed but response generation took too long."
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "An error occurred while generating the response."
    
    def _extract_sql_from_response(self, response: str) -> str:
        """Extract SQL query from model response"""
        # Remove common prefixes/suffixes
        response = response.strip()
        
        # Look for SQL patterns
        sql_patterns = [
            r'``````',
            r'``````',
            r'SELECT.*?(?:;|$)',
            r'WITH.*?SELECT.*?(?:;|$)'
        ]
        
        import re
        for pattern in sql_patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                sql = match.group(1) if len(match.groups()) > 0 else match.group(0)
                sql = sql.strip()
                if sql.endswith(';'):
                    sql = sql[:-1]
                return sql
        
        # If no pattern matches, return cleaned response
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.upper().startswith(('SELECT', 'WITH')):
                if line.endswith(';'):
                    line = line[:-1]
                return line
        
        return response
    
    def benchmark_model(self) -> Dict[str, Any]:
        """Benchmark model performance"""
        logger.info("Benchmarking Mistral model...")
        
        test_queries = [
            "What is machine learning?",
            "Explain the concept of databases in simple terms.",
            "How do you calculate return on investment?",
            "What are the benefits of data visualization?"
        ]
        
        results = {
            "model_name": self.model_name,
            "test_results": [],
            "average_response_time": 0,
            "successful_responses": 0
        }
        
        total_time = 0
        successful = 0
        
        for i, query in enumerate(test_queries):
            logger.info(f"Test {i+1}/{len(test_queries)}: {query[:50]}...")
            
            start_time = time.time()
            try:
                result = subprocess.run(
                    ['ollama', 'run', self.model_name],
                    input=query,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                if result.returncode == 0:
                    successful += 1
                    total_time += response_time
                    
                    test_result = {
                        "query": query,
                        "response_time": response_time,
                        "success": True,
                        "response_length": len(result.stdout)
                    }
                else:
                    test_result = {
                        "query": query,
                        "response_time": response_time,
                        "success": False,
                        "error": result.stderr.strip()
                    }
                
                results["test_results"].append(test_result)
                
            except subprocess.TimeoutExpired:
                test_result = {
                    "query": query,
                    "response_time": 30,
                    "success": False,
                    "error": "Timeout"
                }
                results["test_results"].append(test_result)
            
            except Exception as e:
                test_result = {
                    "query": query,
                    "response_time": 0,
                    "success": False,
                    "error": str(e)
                }
                results["test_results"].append(test_result)
        
        results["successful_responses"] = successful
        results["average_response_time"] = total_time / successful if successful > 0 else 0
        
        logger.info(f"Benchmark complete: {successful}/{len(test_queries)} successful")
        logger.info(f"Average response time: {results['average_response_time']:.2f}s")
        
        return results

# Utility functions
def test_mistral_connection(model_name: str = "mistral:7b-instruct") -> bool:
    """Test connection to Mistral model"""
    try:
        result = subprocess.run(
            ['ollama', 'run', model_name, 'Hello'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False

def get_available_models() -> List[str]:
    """Get list of available Ollama models"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            return models
    except:
        pass
    return []
