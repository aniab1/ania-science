
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
