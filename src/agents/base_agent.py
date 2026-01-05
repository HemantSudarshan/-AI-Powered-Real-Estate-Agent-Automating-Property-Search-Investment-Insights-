"""Abstract base class for AI agents."""
from abc import ABC, abstractmethod
from typing import Dict, Any
from src.utils.logger import setup_logger


class BaseAgent(ABC):
    """Abstract base class for all AI agents."""
    
    def __init__(self, name: str):
        """
        Initialize agent.
        
        Args:
            name: Agent name for logging
        """
        self.name = name
        self.logger = setup_logger(f"agents.{name}")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic.
        
        Args:
            input_data: Input data dictionary
        
        Returns:
            Output data dictionary
        """
        pass
    
    def log_execution(self, input_data: Dict, output_data: Dict):
        """
        Log agent execution.
        
        Args:
            input_data: Input data
            output_data: Output data
        """
        self.logger.info(
            f"Agent {self.name} executed",
            extra={
                'input': str(input_data)[:200],
                'output': str(output_data)[:200]
            }
        )
