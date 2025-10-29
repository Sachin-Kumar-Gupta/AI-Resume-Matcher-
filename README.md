# 🤖 AI Resume Matcher

An intelligent Streamlit app that compares your **resume** with multiple **job descriptions** using **Natural Language Processing (NLP)** and **semantic similarity** to find the best job match.

---

## 🚀 Features

- 📄 Upload your **resume** in `.pdf` or `.docx` format  
- 🧠 Paste multiple **job descriptions**  
- 📊 Get an **AI-based Match Score** for each job  
- 💬 Personalized feedback on **missing skills**  
- 📈 Interactive **bar chart visualization**  
- 🌐 Simple **Streamlit web interface**

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend UI | Streamlit |
| NLP Model | `sentence-transformers` (MiniLM) |
| Data Handling | Pandas, NumPy |
| Resume Parsing | PyPDF2, python-docx |
| Visualization | Matplotlib |

---
🧠 How It Works

The app converts resume & job descriptions into sentence embeddings using the all-MiniLM-L6-v2 model from Hugging Face.

It then calculates cosine similarity between vectors to determine match percentage.

Finally, it highlights missing keywords and skills from each job description.

💡 Future Enhancements

🌍 Auto-fetch job descriptions from LinkedIn/Indeed

🗂️ Multi-resume comparison

🧑‍🏫 AI-generated resume improvement tips using GPT

📬 Email-based report export

🧑‍💻 Author

Sachin Kumar Gupta
📍 Data Analyst | Aspiring NLP Engineer
🔗 [LinkedIn](https://www.linkedin.com/in/sachingupta-ds/)
 | [GitHub](https://github.com/Sachin-Kumar-Gupta)

 ⭐ If you like this project, consider giving it a star — it helps others discover it!
