import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# توليد مقال علمي جديد
prompt = """
اكتب مقالاً علمياً تحليلياً قصيراً وعميقاً باللغة العربية حول موضوع متقدم في الفيزياء النظرية أو الرياضيات.
شروط هامة:
1. لا تستخدم رموزاً عشوائية أو غريبة.
2. اكتب المعادلات الرياضية بصيغة LaTeX محاطة بعلامات دولار مثل $$E=mc^2$$ لكي تظهر بشكل صحيح.
"""

response = model.generate_content(prompt)
article_text = response.text

# قالب الموقع الاحترافي المتكامل (الداكن، مع المعادلات، ونافذة الدردشة، ومكان المقالات المتجدد)
html_template = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدونة العلوم والفيزياء النظرية</title>
    <!-- مكتبة MathJax لعرض المعادلات الرياضية بوضوح -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .container {{
            max-width: 800px;
            width: 100%;
            background: #161b22;
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            margin-top: 20px;
        }}
        h1 {{
            color: #58a6ff;
            text-align: center;
            border-bottom: 2px solid #30363d;
            padding-bottom: 15px;
        }}
        .article {{
            line-height: 1.9;
            font-size: 1.15em;
            margin-top: 20px;
        }}
        /* تصميم نافذة الدردشة العائمة */
        #chat-widget {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            z-index: 1000;
        }}
        #chat-btn {{
            background-color: #238636;
            color: white;
            border: none;
            padding: 12px 22px;
            border-radius: 30px;
            cursor: pointer;
            font-size: 1.05em;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }}
        #chat-box {{
            display: none;
            width: 350px;
            height: 450px;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.6);
            flex-direction: column;
            overflow: hidden;
            margin-bottom: 10px;
        }}
        #chat-header {{
            background: #21262d;
            padding: 12px 15px;
            font-weight: bold;
            color: #58a6ff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #30363d;
        }}
        #close-chat {{
            background: none;
            border: none;
            color: #8b949e;
            cursor: pointer;
            font-size: 1.3em;
        }}
        #chat-messages {{
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            font-size: 0.95em;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .msg {{
            padding: 10px 14px;
            border-radius: 10px;
            max-width: 85%;
        }}
        .user-msg {{
            background: #1f6feb;
            color: white;
            align-self: flex-start;
        }}
        .ai-msg {{
            background: #21262d;
            color: #c9d1d9;
            align-self: flex-end;
            border: 1px solid #30363d;
        }}
        #chat-input-area {{
            display: flex;
            padding: 10px;
            background: #21262d;
            border-top: 1px solid #30363d;
        }}
        #user-input {{
            flex: 1;
            background: #0d1117;
            border: 1px solid #30363d;
            color: white;
            padding: 10px;
            border-radius: 6px;
            outline: none;
        }}
        #send-btn {{
            background: #238636;
            color: white;
            border: none;
            padding: 10px 15px;
            margin-right: 8px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }}
    </style>
</head>
<body>

    <div class="container">
        <h1>مدونة العلوم والرياضيات</h1>
        <div class="article">
            <p>{article_text.replace(chr(10), "</p><p>")}</p>
        </div>
    </div>

    <!-- نافذة المحادثة العائمة -->
    <div id="chat-widget">
        <div id="chat-box">
            <div id="chat-header">
                <span>مساعد الذكاء الاصطناعي العلمي</span>
                <button id="close-chat" onclick="toggleChat()">×</button>
            </div>
            <div id="chat-messages">
                <div class="msg ai-msg">أهلاً بك! أنا مساعدك العلمي للفيزياء والرياضيات. اطرح أي سؤال وسأرد عليك فوراً.</div>
            </div>
            <div id="chat-input-area">
                <input type="text" id="user-input" placeholder="اكتب سؤالك العلمي هنا..." onkeypress="handleKeyPress(event)">
                <button id="send-btn" onclick="sendMessage()">إرسال</button>
            </div>
        </div>
        <button id="chat-btn" onclick="toggleChat()">💬 اسأل الذكاء الاصطناعي</button>
    </div>

    <script>
        function toggleChat() {{
            const box = document.getElementById('chat-box');
            const btn = document.getElementById('chat-btn');
            if (box.style.display === 'flex') {{
                box.style.display = 'none';
                btn.style.display = 'block';
            }} else {{
                box.style.display = 'flex';
                btn.style.display = 'none';
            }}
        }}

        function sendMessage() {{
            const input = document.getElementById('user-input');
            const text = input.value.trim();
            if (!text) return;

            const messages = document.getElementById('chat-messages');
            const userMsg = document.createElement('div');
            userMsg.className = 'msg user-msg';
            userMsg.textContent = text;
            messages.appendChild(userMsg);

            input.value = '';
            messages.scrollTop = messages.scrollHeight;

            setTimeout(() => {{
                const aiMsg = document.createElement('div');
                aiMsg.className = 'msg ai-msg';
                aiMsg.textContent = "لقد استقبلت سؤالك حول (" + text + "). جاري تحليل المفهوم العلمي وإعداد الإجابة لك!";
                messages.appendChild(aiMsg);
                messages.scrollTop = messages.scrollHeight;
            }}, 800);
        }}

        function handleKeyPress(e) {{
            if (e.key === 'Enter') {{
                sendMessage();
            }}
        }}
    </script>

</body>
</html>
"""

# حفظ الملف بالشكل الصحيح
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("تم تحديث الموقع بنجاح مع القالب الداكن والمعادلات والدردشة!")
