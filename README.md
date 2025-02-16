# **AI Movie Character Chatbot 🎭**  

This is a simple AI chatbot that lets users chat with movie characters. It retrieves real dialogues from a database and generates AI responses when necessary.  

---

## **📌 Features**
✅ Chat with movie characters like **Iron Man, Harry Potter, Yoda, Babu Rao, etc.**  
✅ Uses a **Vector Embeddings** to store real movie dialogues.  
✅ **AI-powered responses** if no matching dialogue is found.  
✅ Built with **FastAPI** (Backend) and **React.js + Tailwind CSS + Radix UI** (Frontend).  

---

## **🛠️ Tech Stack**
- **Backend:** FastAPI, FAISS, LangChain (OpenAI API), Python  
- **Frontend:** React.js, Tailwind CSS, Radix UI  
- **Database:** SQLite (for storing movie dialogues)  

---

## **🚀 Getting Started**
### **1️⃣ Clone the Repository**
```sh
git https://github.com/lunatic-7/dharmal_q.git
cd dharmal_q
```

### **2️⃣ Backend Setup**
#### **Install Dependencies**
```sh
cd dharmal_q_backend
pip install -r requirements.txt
```
#### **Set Up Environment Variables**
Create a `.env` file in the `dharmal_q_backend` directory:
```sh
OPENAI_API_KEY=your_openai_api_key
```

#### **Load Harry Potter Dialogues into Vector embeddings**
```sh
python rag_indexer.py  # Only Harry Potter Script is used for now, rest of the charater responses are generated from propmt only
```

#### **Run the Backend**
```sh
uvicorn main:app --reload
```
The API will be available at: **`http://127.0.0.1:8000`**

---

### **3️⃣ Frontend Setup**
#### **Install Dependencies**
```sh
cd dharmal_q_frontend
npm install
```

#### **Start the Frontend**
```sh
npm run dev
```
The UI will be available at: **`http://localhost:5173`**

---

## **🛠 API Endpoint**
| Method | Endpoint  | Description |
|---------|----------|-------------|
| `POST` | `/chat` | Accepts `{ character, user_message }` and returns a response. |

---

## **📌 Future Enhancements**
- ✅ Add **more characters and dialogues**  
- ✅ Implement **fuzzy matching** for better dialogue retrieval  
- ✅ Improve **UI design** for a more engaging experience  

---

## **📜 License**
This project is open-source. Feel free to use, modify, and contribute! 🚀  

---
🔗 **Created by [Your Name]**  
💻 **Repo:** [GitHub Link]  
