import os
import logging
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)


class EnvHelper:
    def __init__(self, **kwargs) -> None:
        load_dotenv()

        # Azure Search
        self.AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE", "")
        self.AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX", "")
        self.AZURE_SEARCH_USE_SEMANTIC_SEARCH = (
            os.getenv("AZURE_SEARCH_USE_SEMANTIC_SEARCH", "False").lower() == "true"
        )
        self.AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.getenv(
            "AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default"
        )
        self.AZURE_SEARCH_INDEX_IS_PRECHUNKED = os.getenv(
            "AZURE_SEARCH_INDEX_IS_PRECHUNKED", ""
        )
        self.AZURE_SEARCH_TOP_K = os.getenv("AZURE_SEARCH_TOP_K", 5)
        self.AZURE_SEARCH_ENABLE_IN_DOMAIN = (
            os.getenv("AZURE_SEARCH_ENABLE_IN_DOMAIN", "true").lower() == "true"
        )
        self.AZURE_SEARCH_FIELDS_ID = os.getenv("AZURE_SEARCH_FIELDS_ID", "id")
        self.AZURE_SEARCH_CONTENT_COLUMNS = os.getenv(
            "AZURE_SEARCH_CONTENT_COLUMNS", "content"
        )
        self.AZURE_SEARCH_CONTENT_VECTOR_COLUMNS = os.getenv(
            "AZURE_SEARCH_CONTENT_VECTOR_COLUMNS", "content_vector"
        )
        self.AZURE_SEARCH_DIMENSIONS = os.getenv("AZURE_SEARCH_DIMENSIONS", "1536")
        self.AZURE_SEARCH_FILENAME_COLUMN = os.getenv(
            "AZURE_SEARCH_FILENAME_COLUMN", "filepath"
        )
        self.AZURE_SEARCH_TITLE_COLUMN = os.getenv("AZURE_SEARCH_TITLE_COLUMN", "title")
        self.AZURE_SEARCH_URL_COLUMN = os.getenv("AZURE_SEARCH_URL_COLUMN", "url")
        self.AZURE_SEARCH_FIELDS_TAG = os.getenv("AZURE_SEARCH_FIELDS_TAG", "tag")
        self.AZURE_SEARCH_FIELDS_METADATA = os.getenv(
            "AZURE_SEARCH_FIELDS_METADATA", "metadata"
        )
        self.AZURE_SEARCH_CONVERSATIONS_LOG_INDEX = os.getenv(
            "AZURE_SEARCH_CONVERSATIONS_LOG_INDEX", "conversations"
        )
        self.AZURE_AUTH_TYPE = os.getenv("AZURE_AUTH_TYPE", "keys")
        # Azure OpenAI
        self.AZURE_OPENAI_RESOURCE = os.getenv("AZURE_OPENAI_RESOURCE", "")
        self.AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL", "")
        self.AZURE_OPENAI_MODEL_NAME = os.getenv(
            "AZURE_OPENAI_MODEL_NAME", "gpt-35-turbo"
        )
        self.AZURE_OPENAI_TEMPERATURE = os.getenv("AZURE_OPENAI_TEMPERATURE", 0)
        self.AZURE_OPENAI_TOP_P = os.getenv("AZURE_OPENAI_TOP_P", 1.0)
        self.AZURE_OPENAI_MAX_TOKENS = os.getenv("AZURE_OPENAI_MAX_TOKENS", 1000)
        self.AZURE_OPENAI_STOP_SEQUENCE = os.getenv("AZURE_OPENAI_STOP_SEQUENCE", "")
        self.AZURE_OPENAI_SYSTEM_MESSAGE = os.getenv(
            "AZURE_OPENAI_SYSTEM_MESSAGE",
            "You are an AI assistant that helps people find information.",
        )
        self.AZURE_OPENAI_API_VERSION = os.getenv(
            "AZURE_OPENAI_API_VERSION", "2023-12-01-preview"
        )
        self.AZURE_OPENAI_STREAM = os.getenv("AZURE_OPENAI_STREAM", "true")
        self.AZURE_OPENAI_EMBEDDING_MODEL = os.getenv(
            "AZURE_OPENAI_EMBEDDING_MODEL", ""
        )
        self.SHOULD_STREAM = (
            True if self.AZURE_OPENAI_STREAM.lower() == "true" else False
        )

        self.AZURE_TOKEN_PROVIDER = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
        self.USE_KEY_VAULT = os.getenv("USE_KEY_VAULT", "").lower() == "true"
        # Initialize Azure keys based on authentication type and environment settings.
        # When AZURE_AUTH_TYPE is "rbac", azure keys are None or an empty string.
        # When USE_KEY_VAULT environment variable is set, keys are securely fetched from Azure Key Vault using DefaultAzureCredential.
        # Otherwise, keys are obtained from environment variables.
        if self.AZURE_AUTH_TYPE == "rbac":
            self.AZURE_SEARCH_KEY = None
            self.AZURE_OPENAI_KEY = ""
            self.AZURE_SPEECH_KEY = None
        elif self.USE_KEY_VAULT:
            credential = DefaultAzureCredential()
            self.secret_client = SecretClient(
                os.environ.get("AZURE_KEY_VAULT_ENDPOINT"), credential
            )
            self.AZURE_SEARCH_KEY = self.secret_client.get_secret(
                os.environ.get("AZURE_SEARCH_KEY")
            ).value
            self.AZURE_OPENAI_KEY = self.secret_client.get_secret(
                os.environ.get("AZURE_OPENAI_KEY", "")
            ).value
            self.AZURE_SPEECH_KEY = self.secret_client.get_secret(
                os.environ.get("AZURE_SPEECH_SERVICE_KEY")
            ).value
        else:
            self.AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
            self.AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY", "")
            self.AZURE_SPEECH_KEY = os.environ.get("AZURE_SPEECH_SERVICE_KEY")
        # Set env for OpenAI SDK
        self.OPENAI_API_BASE = (
            f"https://{os.getenv('AZURE_OPENAI_RESOURCE')}.openai.azure.com/"
        )
        self.OPENAI_API_TYPE = "azure" if self.AZURE_AUTH_TYPE == "keys" else "azure_ad"
        self.OPENAI_API_KEY = self.AZURE_OPENAI_KEY
        self.OPENAI_API_VERSION = self.AZURE_OPENAI_API_VERSION
        os.environ["OPENAI_API_TYPE"] = self.OPENAI_API_TYPE
        os.environ["OPENAI_API_BASE"] = (
            f"https://{os.getenv('AZURE_OPENAI_RESOURCE')}.openai.azure.com/"
        )
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY
        os.environ["OPENAI_API_VERSION"] = self.OPENAI_API_VERSION
        # Azure Functions - Batch processing
        self.BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:7071")
        self.FUNCTION_KEY = os.getenv("FUNCTION_KEY")
        self.AzureWebJobsStorage = os.getenv("AzureWebJobsStorage", "")
        self.DOCUMENT_PROCESSING_QUEUE_NAME = os.getenv(
            "DOCUMENT_PROCESSING_QUEUE_NAME", "doc-processing"
        )
        # Azure Blob Storage
        self.AZURE_BLOB_ACCOUNT_NAME = os.getenv("AZURE_BLOB_ACCOUNT_NAME", "")
        self.AZURE_BLOB_ACCOUNT_KEY = (
            self.secret_client.get_secret(os.getenv("AZURE_BLOB_ACCOUNT_KEY", "")).value
            if self.USE_KEY_VAULT
            else os.getenv("AZURE_BLOB_ACCOUNT_KEY", "")
        )
        self.AZURE_BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME", "")
        # Azure Form Recognizer
        self.AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv(
            "AZURE_FORM_RECOGNIZER_ENDPOINT", ""
        )
        self.AZURE_FORM_RECOGNIZER_KEY = (
            self.secret_client.get_secret(
                os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")
            ).value
            if self.USE_KEY_VAULT
            else os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")
        )
        # Azure App Insights
        self.APPINSIGHTS_CONNECTION_STRING = os.getenv(
            "APPINSIGHTS_CONNECTION_STRING", ""
        )
        # Azure AI Content Safety
        self.AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv(
            "AZURE_CONTENT_SAFETY_ENDPOINT", ""
        )
        if (
            "https" not in self.AZURE_CONTENT_SAFETY_ENDPOINT
            and "api.cognitive.microsoft.com" not in self.AZURE_CONTENT_SAFETY_ENDPOINT
        ):
            self.AZURE_CONTENT_SAFETY_ENDPOINT = self.AZURE_FORM_RECOGNIZER_ENDPOINT
        self.AZURE_CONTENT_SAFETY_KEY = (
            self.secret_client.get_secret(
                os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
            ).value
            if self.USE_KEY_VAULT
            else os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
        )
        # Orchestration Settings
        self.ORCHESTRATION_STRATEGY = os.getenv(
            "ORCHESTRATION_STRATEGY", "openai_function"
        )
        # Speech Service
        self.AZURE_SPEECH_SERVICE_REGION = os.getenv("AZURE_SPEECH_SERVICE_REGION")

    def should_use_data(self) -> bool:
        if (
            self.AZURE_SEARCH_SERVICE
            and self.AZURE_SEARCH_INDEX
            and self.AZURE_SEARCH_KEY
        ):
            return True
        return False

    def is_chat_model(self):
        if "gpt-4" in self.AZURE_OPENAI_MODEL_NAME.lower():
            return True
        return False

    @staticmethod
    def check_env():
        for attr, value in EnvHelper().__dict__.items():
            if value == "":
                logging.warning(f"{attr} is not set in the environment variables.")
