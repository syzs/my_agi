import numpy as np
from numpy import dot
from numpy.linalg import norm
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

amap_key = "6d672e6194caa3b639fccf2caf06c342"

_ = load_dotenv(find_dotenv())

client = OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
    '''封装 openai 接口'''
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content

def extract_text_from_pdf(filename, page_numbers=None, min_line_length=1):
    '''从 PDF 文件中（按指定页码）提取文字'''
    paragraphs = []
    buffer = ''
    full_text = ''
    # 提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳过范围外的页
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + '\n'
    # 按空行分隔，将文本重新组织成段落
    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' '+text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    return paragraphs

def cos_sim(a, b):
    '''余弦距离 -- 越大越相似'''
    return dot(a, b)/(norm(a)*norm(b))


def l2(a, b):
    '''欧式距离 -- 越小越相似'''
    x = np.asarray(a)-np.asarray(b)
    return norm(x)

def get_embeddings(texts, model='text-embedding-ada-002'):
    data = client.embeddings.create(input=texts, model=model).data
    return [x.embedding for x in data]

def test_query():
    test_query = ["测试文本", "ceshiwenben"]
    vec_list = get_embeddings(test_query)
    print(len(vec_list)) # @
    print(vec_list[0][:10]) # [-0.0072620222344994545, -0.006227712146937847, -0.0...]
    print(vec_list[1][:10])
    print(len(vec_list[0], len(vec_list[1]))) # 1536


def test_cos_sim():
    # query = "国际争端"
    # 且能支持跨语言
    query = "global conflicts"

    documents = [
        "联合国就苏丹达尔富尔地区大规模暴力事件发出警告",
        "土耳其、芬兰、瑞典与北约代表将继续就瑞典“入约”问题进行谈判",
        "日本岐阜市陆上自卫队射击场内发生枪击事件 3人受伤",
        "国家游泳中心（水立方）：恢复游泳、嬉水乐园等水上项目运营",
        "我国首次在空间站开展舱外辐射生物学暴露实验",
    ]

    query_vec = get_embeddings([query])[0]
    doc_vecs = get_embeddings(documents)

    print("Cosine distance:")
    print(cos_sim(query_vec, query_vec))

    for doc_vec in doc_vecs:
        print(cos_sim(query_vec, doc_vec))

    print("\nEuclidean distance:")
    print(l2(query_vec, query_vec))
    for vec in doc_vecs:
        print(l2(query_vec, vec))




class MyVectorDBConnector:
    def __init__(self, collection_name, embedding_fn):
        chroma_client =   chromadb.Client(Settings(allow_reset=True))

        # 为了演示，实际不需要每次 reset()
        chroma_client.reset()

        # 创建一个 collection
        self.collection = chroma_client.get_or_create_collection(name=collection_name)
        self.embedding_fn = embedding_fn

    def add_documents(self, documents):
        '''向 collection 中添加文档与向量'''
        self.collection.add(
            embeddings=self.embedding_fn(documents),  # 每个文档的向量
            documents=documents,  # 文档的原文
            ids=[f"id{i}" for i in range(len(documents))]  # 每个文档的 id
        )

    def search(self, query, top_n):
        '''检索向量数据库'''
        results = self.collection.query(
            query_embeddings=self.embedding_fn([query]),
            n_results=top_n
        )
        return results

class RAG_Bot:
    def __init__(self, vector_db, llm_api, n_results=2):
        self.vector_db = vector_db
        self.llm_api = llm_api
        self.n_results = n_results

    def chat(self, user_query):
        # 1. 检索
        search_results = self.vector_db.search(user_query, self.n_results)

        # 2. 构建 Prompt
        prompt = build_prompt(
            prompt_template, info=search_results['documents'][0], query=user_query)

        # 3. 调用 LLM
        response = self.llm_api(pro mpt)
        return response

def search_from_embedding_db():
    # 为了演示方便，我们只取两页（第一章）
    paragraphs = extract_text_from_pdf("llama2.pdf", page_numbers=[2, 3], min_line_length=10)

    # 创建一个向量数据库对象
    vector_db = MyVectorDBConnector("demo", get_embeddings)
    # 向向量数据库中添加文档
    vector_db.add_documents(paragraphs)

    user_query = "Llama 2有多少参数"
    results = vector_db.search(user_query, 2)

    for para in results['documents'][0]:
        print(para + "\n")

    # 创建一个RAG机器人
    bot = RAG_Bot(
        vector_db,
        llm_api=get_completion
    )

    user_query = "llama 2有对话版吗？"
    response = bot.chat(user_query)
    print(response) # 是的，Llama 2有对话版，它被称为Llama 2-Chat，是经过优化用于对话场景的版本。


if __name__ == '__main__':
    test_cos_sim()