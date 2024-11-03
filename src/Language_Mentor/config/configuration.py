import os
from dotenv import load_dotenv
from Language_Mentor import logger
from Language_Mentor.constants import *
from Language_Mentor.utils.common import *
from Language_Mentor.entity.config_entity import (ModelConfig,)
                                                      #UploadFileConfig)



class ConfigurationManager:
    def __init__(self,
                 config_filepath    = CONFIG_FILE_PATH,
                 params_filepath    = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)


    def get_model_config(self) -> ModelConfig:
        params  = self.params
        logger.info("Model config initialized")
        load_dotenv()
        model_config = ModelConfig(Model_name   = params.MODEL_NAME,
                                   temperature  = params.TEMPERATURE,
                                   api_key      = os.getenv("OPENAI_API_KEY"))

        return model_config
    