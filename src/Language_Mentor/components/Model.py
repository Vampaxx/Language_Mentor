from Language_Mentor import logger
from langchain_openai import ChatOpenAI
from Language_Mentor.entity.config_entity import ModelConfig


class ModelSetup:

    def __init__(self,config = ModelConfig):
        self.config = config

    def model_setup(self):
        logger.info("Model setup initialized")
        llm     = ChatOpenAI(model        = self.config.Model_name,
                             temperature  = self.config.temperature,
                             api_key      = self.config.api_key,)
        
        logger.info(f"model----{(self.config.Model_name).split('/')[-1]}----created")
        return llm 
    



if __name__ == "__main__":
    pass 