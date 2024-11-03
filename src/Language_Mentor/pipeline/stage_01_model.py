from Language_Mentor import logger
from Language_Mentor.config.configuration import ConfigurationManager
from Language_Mentor.components.Model import ModelSetup




STAGE_NAME = "Model setup stage"


class ModelPipeline:
    def __init__(self):
        pass 
    def main(self):
        try:
            manager             = ConfigurationManager()
            model_config        = manager.get_model_config()
            model_setup         = ModelSetup(config=model_config)
            llm                 = model_setup.model_setup()
            return llm
        except Exception as e:
            raise e
        

if __name__ == "__main__":
    try:
        logger.info(f"<<<    stage   {STAGE_NAME}    started >>>")
        obj     = ModelPipeline()
        llm     = obj.main()
        #print(llm.invoke("hey"))
        logger.info(f"<<<    stage   {STAGE_NAME}    completed \n\n===========================================>>>")

    except Exception as e:
        raise e