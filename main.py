from Language_Mentor.config.configuration import ConfigurationManager
from Language_Mentor.components.Model import ModelSetup


manager = ConfigurationManager()
model_config = manager.get_model_config()
llm = ModelSetup(config=model_config).model_setup()



if __name__ == "__main__":
    print(llm.invoke("hey"))






