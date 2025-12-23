import os
import toml

def load_config():
    config = toml.load('config.toml')
    
    # Override with environment variables
    if os.getenv('PEXELS_API_KEY'):
        config['app']['pexels_api_keys'] = [os.getenv('PEXELS_API_KEY')]
    
    if os.getenv('GEMINI_API_KEY'):
        config['llm']['gemini']['api_key'] = os.getenv('GEMINI_API_KEY')
    
    if os.getenv('LLM_PROVIDER'):
        config['app']['llm_provider'] = os.getenv('LLM_PROVIDER')
    
    return config