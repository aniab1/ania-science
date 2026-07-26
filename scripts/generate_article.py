import os
import google.generativeai as genai
from datetime import datetime

# استدعاء مفتاح الـ API من إعدادات الأمان في GitHub
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("مفتاح الـ API غير موجود!")

genai.configure(api_key=api_key)
# استخدام نموذج جيميناي السريع لتوليد المقالات
# اختيار النموذج المتاح تلقائياً لتجنب أخطاء 404
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        model_name = m.name
        break

model = genai.GenerativeModel(model_name)

# موضوع علمي جديد يتم توليده
prompt = "اكتب مقالة علمية عميقة ومتقدمة باللغة العربية حول موضوع في الفيزياء النظرية أو الرياضيات المتقدمة (مثل ميكانيكا الكم، النسبية العامة، أو المعادلات التفاضلية). اجعل المقالة منسقة بحيث تتضمن عنواناً رئيسياً، مقدمة تحليلية، وجسماً للموضوع مع معادلات رياضية واضحة."

response = model.generate_content(prompt)
article_content = response.text

# قراءة ملف index.html الحالي
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# تصميم المقالة الجديدة لإضافتها للصفحة
today = datetime.now().strftime("%Y-%m-%d")
new_article_html = f"""
    <div class="article">
        <h2>مقال جديد ({today})</h2>
        <div>{article_content.replace(chr(10), '<br>')}</div>
    </div>
"""

# دمج المقال الجديد في مكان الحاوية الرئيسية
updated_html = html_content.replace('<div class="container">', f'<div class="container">\n{new_article_html}')

# حفظ التعديل في ملف index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("تم توليد ونشر المقال بنجاح!")
