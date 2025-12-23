import os
import shutil
import socket

import toml
from loguru import logger

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
config_file = f"{root_dir}/config.toml"


def load_config():
    # fix: IsADirectoryError: [Errno 21] Is a directory: '/MoneyPrinterTurbo/config.toml'
    if os.path.isdir(config_file):
        shutil.rmtree(config_file)

    if not os.path.isfile(config_file):
        example_file = f"{root_dir}/config.example.toml"
        if os.path.isfile(example_file):
            shutil.copyfile(example_file, config_file)
            logger.info("copy config.example.toml to config.toml")

    logger.info(f"load config from file: {config_file}")

    try:
        _config_ = toml.load(config_file)
    except Exception as e:
        logger.warning(f"load config failed: {str(e)}, try to load as utf-8-sig")
        with open(config_file, mode="r", encoding="utf-8-sig") as fp:
            _cfg_content = fp.read()
            _config_ = toml.loads(_cfg_content)
    
    # ===== OVERRIDE WITH ENVIRONMENT VARIABLES (for production) =====
    _config_ = override_with_env_vars(_config_)
    
    return _config_


def override_with_env_vars(config):
    """Override config values with environment variables if they exist"""
    
    # Ensure 'app' section exists
    if 'app' not in config:
        config['app'] = {}
    
    # Pixabay API Keys
    if os.getenv('PIXABAY_API_KEY'):
        keys = os.getenv('PIXABAY_API_KEY').split(',')
        config['app']['pixabay_api_keys'] = [k.strip() for k in keys]
        logger.info(f"Loaded {len(config['app']['pixabay_api_keys'])} Pixabay API key(s) from environment")
    
    # Pexels API Keys
    if os.getenv('PEXELS_API_KEY'):
        keys = os.getenv('PEXELS_API_KEY').split(',')
        config['app']['pexels_api_keys'] = [k.strip() for k in keys]
        logger.info(f"Loaded {len(config['app']['pexels_api_keys'])} Pexels API key(s) from environment")
    
    # LLM Provider
    if os.getenv('LLM_PROVIDER'):
        config['app']['llm_provider'] = os.getenv('LLM_PROVIDER')
        logger.info(f"LLM Provider set to: {config['app']['llm_provider']}")
    
    # Video Source
    if os.getenv('VIDEO_SOURCE'):
        config['app']['video_source'] = os.getenv('VIDEO_SOURCE')
        logger.info(f"Video Source set to: {config['app']['video_source']}")
    
    # Gemini API Key
    if os.getenv('GEMINI_API_KEY'):
        config['app']['gemini_api_key'] = os.getenv('GEMINI_API_KEY')
        logger.info("Gemini API key loaded from environment")
    
    # OpenAI API Key
    if os.getenv('OPENAI_API_KEY'):
        config['app']['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        logger.info("OpenAI API key loaded from environment")
    
    # Moonshot API Key
    if os.getenv('MOONSHOT_API_KEY'):
        config['app']['moonshot_api_key'] = os.getenv('MOONSHOT_API_KEY')
        logger.info("Moonshot API key loaded from environment")
    
    # DeepSeek API Key
    if os.getenv('DEEPSEEK_API_KEY'):
        config['app']['deepseek_api_key'] = os.getenv('DEEPSEEK_API_KEY')
        logger.info("DeepSeek API key loaded from environment")
    
    # Qwen API Key
    if os.getenv('QWEN_API_KEY'):
        config['app']['qwen_api_key'] = os.getenv('QWEN_API_KEY')
        logger.info("Qwen API key loaded from environment")
    
    # Subtitle Provider
    if os.getenv('SUBTITLE_PROVIDER'):
        config['app']['subtitle_provider'] = os.getenv('SUBTITLE_PROVIDER')
        logger.info(f"Subtitle Provider set to: {config['app']['subtitle_provider']}")
    
    # Endpoint URL
    if os.getenv('ENDPOINT'):
        config['app']['endpoint'] = os.getenv('ENDPOINT')
        logger.info(f"Endpoint URL set to: {config['app']['endpoint']}")
    
    # Material Directory
    if os.getenv('MATERIAL_DIRECTORY'):
        config['app']['material_directory'] = os.getenv('MATERIAL_DIRECTORY')
        logger.info(f"Material Directory set to: {config['app']['material_directory']}")
    
    # Max Concurrent Tasks
    if os.getenv('MAX_CONCURRENT_TASKS'):
        try:
            config['app']['max_concurrent_tasks'] = int(os.getenv('MAX_CONCURRENT_TASKS'))
            logger.info(f"Max Concurrent Tasks set to: {config['app']['max_concurrent_tasks']}")
        except ValueError:
            logger.warning("Invalid MAX_CONCURRENT_TASKS value, using default")
    
    return config


def save_config():
    with open(config_file, "w", encoding="utf-8") as f:
        _cfg["app"] = app
        _cfg["azure"] = azure
        _cfg["siliconflow"] = siliconflow
        _cfg["ui"] = ui
        f.write(toml.dumps(_cfg))


_cfg = load_config()
app = _cfg.get("app", {})
whisper = _cfg.get("whisper", {})
proxy = _cfg.get("proxy", {})
azure = _cfg.get("azure", {})
siliconflow = _cfg.get("siliconflow", {})
ui = _cfg.get(
    "ui",
    {
        "hide_log": False,
    },
)

hostname = socket.gethostname()

log_level = _cfg.get("log_level", "DEBUG")
listen_host = _cfg.get("listen_host", "0.0.0.0")
listen_port = _cfg.get("listen_port", 8080)
project_name = _cfg.get("project_name", "MoneyPrinterTurbo")
project_description = _cfg.get(
    "project_description",
    "<a href='https://github.com/harry0703/MoneyPrinterTurbo'>https://github.com/harry0703/MoneyPrinterTurbo</a>",
)
project_version = _cfg.get("project_version", "1.2.6")
reload_debug = False

imagemagick_path = app.get("imagemagick_path", "")
if imagemagick_path and os.path.isfile(imagemagick_path):
    os.environ["IMAGEMAGICK_BINARY"] = imagemagick_path

ffmpeg_path = app.get("ffmpeg_path", "")
if ffmpeg_path and os.path.isfile(ffmpeg_path):
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

logger.info(f"{project_name} v{project_version}")