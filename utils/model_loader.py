import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_mistralai import ChatMistralAI   # ✅ CHANGE 1: import MistralAI instead of Groq/OpenAI

load_dotenv()

class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    # ✅ CHANGE 2: model_provider now only accepts "mistral"
    # BEFORE: Literal["groq", "openai"] = "groq"
    # AFTER:  Literal["mistral"] = "mistral"
    # WHY: We removed Groq and OpenAI — Mistral is the only provider now.
    model_provider: Literal["mistral"] = "mistral"

    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")

        # ✅ CHANGE 3: Replaced groq/openai blocks with a single mistral block
        # BEFORE:
        #   if self.model_provider == "groq":
        #       groq_api_key = os.getenv("GROQ_API_KEY")
        #       model_name = self.config["llm"]["groq"]["model_name"]
        #       llm = ChatGroq(model=model_name, api_key=groq_api_key)
        #   elif self.model_provider == "openai":
        #       openai_api_key = os.getenv("OPENAI_API_KEY")
        #       model_name = self.config["llm"]["openai"]["model_name"]
        #       llm = ChatOpenAI(model_name="o4-mini", api_key=openai_api_key)
        #
        # AFTER:
        #   if self.model_provider == "mistral":
        #       mistral_api_key = os.getenv("MISTRAL_API_KEY")   ← reads from .env
        #       model_name = self.config["llm"]["mistral"]["model_name"]  ← reads from config
        #       llm = ChatMistralAI(model=model_name, api_key=mistral_api_key)
        #
        # WHY: Same pattern as before, just swapped provider name, env key, and class.

        if self.model_provider == "mistral":
            print("Loading LLM from Mistral..............")
            mistral_api_key = os.getenv("MISTRAL_API_KEY")      # ← from .env
            model_name = self.config["llm"]["mistral"]["model_name"]  # ← from config.yaml
            llm = ChatMistralAI(model=model_name, api_key=mistral_api_key)

        return llm