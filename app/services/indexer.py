from llama_index.core.schema import TextNode
from llama_index.core.node_parser import SentenceSplitter
from app.utils.storage import fetch_parquet_texts
from app.core.engine import engine

def process_and_index_document(
        doc_id: str, 
        provider: str, 
        filename: str, 
        raw_path: str, 
        parquet_path: str
):
    try:
        print(f"[Indexer] 1. เริ่มดึงข้อมูลจาก Storage: {doc_id}")
        pages_data = fetch_parquet_texts(parquet_path)
        if not pages_data:
            print(f"[Indexer] Failed. ไม่พบข้อมูลใน Parquet สำหรับ {doc_id}")
            return
        print(f"[Indexer] 2. กำลังหั่นข้อความ (Chunking)...")
        text_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        nodes = []
        for row in pages_data:
            page_text = row["text"]
            if not page_text: continue
            chunks = text_parser.split_text(page_text)
            for chunk in chunks:
                node = TextNode(
                    text=chunk,
                    metadata={
                        "doc_id": doc_id,
                        "provider": provider,
                        "filename": filename,
                        "page_number": row["page"],
                        "raw_storage_path": raw_path
                    },
                    excluded_embed_metadata_keys=["doc_id", "raw_storage_path"],
                    excluded_llm_metadata_keys=["doc_id", "raw_storage_path"]
                )
                nodes.append(node)
        if engine.index:
            print(f"[Indexer] 3. กำลังเริ่ม Embedding ด้วย BGE-M3 (จำนวน {len(nodes)} chunks)...")
            engine.index.insert_nodes(nodes)
            print(f"[Indexer] 4. Indexing สำเร็จ! ข้อมูลลง Qdrant เรียบร้อยสำหรับ {doc_id}")
        else:
            print("[Indexer] Engine Index is not initialized!")

    except Exception as e:
        print(f"[Indexer] Error เกิดข้อผิดพลาด: {str(e)}")