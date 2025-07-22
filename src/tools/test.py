import asyncio
import os
import sys
# プロジェクトのルートディレクトリをパスに追加
# test.pyから見て適切なパスに調整してください
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_root)

# 絶対インポートに変更
from src.tools.mcp_search_manual import notion_mcp_search

async def main():
    """Notion MCP検索を実行するメイン関数"""
    
    # 検索クエリを指定（複数のクエリでテスト可能）
    test_queries = [
        "React",
    ]
    
    # 複数クエリをテスト
    for search_query in test_queries:
    
        try:
            # Notion MCP検索を実行（.ainvoke() を使用）
            print(f"検索開始: '{search_query}'")
            results = await notion_mcp_search.ainvoke({"query": search_query})
            
            # 結果を表示
            print(f"\n検索結果: {len(results)}件")
            print("=" * 50)
            
            for i, result in enumerate(results, 1):
                print(f"\n【結果 {i}】")
                print(f"ファイル名: {result.file_name}")
                print(f"内容:")
                print(result.content)
                print("-" * 30)
                
        except Exception as e:
            print(f"クエリ '{search_query}' でエラー: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 80 + "\n")  # 次のクエリとの区切り

# 非同期関数を実行
if __name__ == "__main__":
    asyncio.run(main())