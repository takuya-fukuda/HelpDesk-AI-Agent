from langchain.tools import tool
from openai import OpenAI
from pydantic import BaseModel, Field
import json

from src.configs import Settings
from src.custom_logger import setup_logger
#from src.models import SearchOutput

#DB接続用のライブラリ
import psycopg2

# 検索結果の最大取得数
MAX_SEARCH_RESULTS = 3

logger = setup_logger(__name__)


class SearchQueryInput(BaseModel):
    query: str = Field(description="検索クエリ")

class SearchOutput(BaseModel):
    file_name: str = Field(description="The file name")
    content: str = Field(description="The content of the file")

@tool(args_schema=SearchQueryInput)
def search_db_qa(query: str) -> list[SearchOutput]:
    """
    DBからナレッジを検索する関数。
    """

    logger.info(f"Searching by query: {query}")

    settings = Settings()

    #DB接続
    connection = psycopg2.connect(f"host={settings.db_host} dbname={settings.db_name} user={settings.db_user} password={settings.db_password}")

    # カーソルをオープンします
    cursor = connection.cursor()

    openai_client = OpenAI(api_key=settings.openai_api_key)

    logger.info("Generating embedding vector from input query")
    query_vector = (
        openai_client.embeddings.create(input=query, model="text-embedding-3-small")
        .data[0]
        .embedding
    )

    #ベクトル検索クエリの実行
    cursor.execute("SELECT id, chunks, metadata FROM data_table ORDER BY embeddings <#> %s::vector LIMIT %s",[query_vector, MAX_SEARCH_RESULTS])
    search_results = cursor.fetchall()
    print(search_results)

    outputs = []
    for row in search_results:
        _, chunk, metadata = row
        try:
            # metadataがJSON文字列ならパースする
            metadata_dict = json.loads(metadata) if isinstance(metadata, str) else metadata
            file_name = metadata_dict.get("file_name", "unknown")
        except Exception as e:
            logger.warning(f"Failed to parse metadata: {e}")
            file_name = "unknown"

        outputs.append(SearchOutput(file_name=file_name, content=chunk))


    logger.info("Finished searching QA by query")

    return outputs
