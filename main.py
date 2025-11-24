from core.logger import get_logger
from cli.apex_cli import ApexCLI

logger = get_logger()
apex = ApexCLI()
apex.run()
