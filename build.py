import os
import re
import markdown
from datetime import datetime

# 配置路径
MD_DIR = "markdowns"
HTML_DIR = "posts"
TEMPLATE_FILE = "Zhilin Zhang.html"
INDEX_FILE = "index.html"

def init_dirs():
    if not os.path.exists(MD_DIR):
        os.makedirs(MD_DIR)
        # 生成一个示例文件
        with open(os.path.join(MD_DIR, "2026-04-24-hello-world.md"), "w", encoding="utf-8") as f:
            f.write("# Hello World\n\n欢迎来到我的博客！这是第一篇测试文章。\n\n只需在 `markdowns/` 目录下添加 `.md` 文件，然后运行 `python build.py`，即可自动生成静态网页。")
    if not os.path.exists(HTML_DIR):
        os.makedirs(HTML_DIR)

def load_template():
    # 内置极简模板，摆脱对 Zhilin Zhang.html 的依赖
    header_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>我的个人博客</title>
  <style>
    body {
        background-color: #181818;
        color: #BBBBBB;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        margin: 0;
        padding: 0;
    }
    .wrapper {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    a {
        color: #BBBBBB;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    .site-header {
        padding: 20px 0;
        margin-bottom: 40px;
    }
    .site-title {
        font-size: 24px;
        font-weight: bold;
    }
    .page-heading {
        font-size: 32px;
        margin-bottom: 15px;
    }
    .page-intro {
        margin-bottom: 30px;
        font-size: 16px;
    }
    .home-hr {
        border: 0;
        border-top: 1px solid #333;
        margin: 30px 0;
    }
    .post-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .post-list li {
        margin-bottom: 15px;
    }
    .post-list h3 {
        margin: 0;
        font-size: 18px;
        font-weight: normal;
    }
    .site-footer {
        padding: 40px 0;
        margin-top: 40px;
        border-top: 1px solid #333;
        text-align: center;
        font-size: 14px;
    }
    /* Markdown 元素样式 */
    pre, code {
        background-color: #222;
        border-radius: 4px;
        padding: 2px 6px;
    }
    pre {
        padding: 15px;
        overflow-x: auto;
    }
    pre code {
        padding: 0;
        background-color: transparent;
    }
    blockquote {
        border-left: 4px solid #444;
        margin: 0;
        padding-left: 15px;
        color: #999;
    }
  </style>
</head>
<body>
<header class="site-header">
  <div class="wrapper">
    <a class="site-title" rel="author" href="/">My Blog</a>
  </div>
</header>
<main class="page-content" aria-label="Content">
"""

    home_intro = """<div class="wrapper">
  <div class="home">
    <h1 class="page-heading">Unit6,勿忘心安Live,风中追风Fzz1,Yu Chang.没错这些都是我</h1>
    <div class="page-intro">
      <p>歌手,硕士研究生,开发者,调参侠,游泳爱好者,摄影师,骑行者(曾一天骑行120km)</p>
      <p>这个博客囊括了我写过的大部分文章，而这里面的大部分其实都没有什么营养。所以，慎重点击。</p>
    </div>
    <hr class="home-hr">
"""

    footer_html = """
<footer class="site-footer">
  <div class="wrapper">
    <p>© 2026 My Blog. Powered by Markdown.</p>
  </div>
</footer>
</body>
</html>
"""
    return header_html, home_intro, footer_html

def parse_markdowns():
    posts = []
    for filename in os.listdir(MD_DIR):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(MD_DIR, filename)

        # 解析日期 (要求格式: YYYY-MM-DD-名称.md)
        date_str = ""
        title = filename.replace(".md", "")
        date_obj = datetime.now()
        match = re.match(r'^(\d{4}-\d{2}-\d{2})-(.*)$', title)
        if match:
            date_str = match.group(1)
            title = match.group(2).replace("-", " ")
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            date_str = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d")

        with open(filepath, "r", encoding="utf-8") as f:
            md_content = f.read()

        # 尝试从第一行H1提取真正的标题
        first_line = md_content.split('\n')[0]
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            md_content = "\n".join(md_content.split('\n')[1:])

        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])

        post_url = f"{HTML_DIR}/{filename.replace('.md', '.html')}"
        posts.append({
            "title": title,
            "date_str": date_str,
            "date_obj": date_obj,
            "html_content": html_content,
            "url": post_url,
            "filename": filename.replace('.md', '.html')
        })

    # 按日期倒序排列
    posts.sort(key=lambda x: x["date_obj"], reverse=True)
    return posts

def generate_site():
    init_dirs()
    header, home_intro, footer = load_template()
    if not header:
        print("模板解析失败！请确保目录下有 Zhilin Zhang.html 文件。")
        return

    posts = parse_markdowns()

    # 1. 生成文章详情页
    for post in posts:
        post_html = f"""
{header}
      <div class="wrapper">
        <article class="post h-entry" itemscope itemtype="http://schema.org/BlogPosting">
          <header class="post-header">
            <h1 class="post-title p-name" itemprop="name headline" style="margin-bottom: 5px;">{post['title']}</h1>
            <p class="post-meta" style="color: #828282; margin-bottom: 20px;">
              <time class="dt-published" datetime="{post['date_str']}" itemprop="datePublished">
                {post['date_str']}
              </time>
            </p>
          </header>
          <div class="post-content e-content" itemprop="articleBody" style="line-height: 1.8; font-size: 16px;">
            {post['html_content']}
          </div>
        </article>
      </div>
    </main>
{footer}"""

        with open(os.path.join(HTML_DIR, post['filename']), "w", encoding="utf-8") as f:
            f.write(post_html)

    # 2. 生成首页 index.html
    list_html = '<div class="wrapper">\n<ul class="post-list">\n'
    for post in posts:
        short_date = post['date_obj'].strftime("%y-%m-%d")
        list_html += f'''<li>
        <h3 style="display: flex; align-items: center;">
          <span style="color: #626262; margin-right: 8px;">{short_date} &middot;</span>
          <a class="post-link" href="{post['url']}">
            {post['title']}
          </a>
        </h3></li>\n'''
    list_html += '</ul>\n</div>\n</div>\n</main>'

    index_content = f"{header}\n{home_intro}\n{list_html}\n{footer}"
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"成功生成了主页 ({INDEX_FILE}) 和 {len(posts)} 篇文章在 {HTML_DIR}/ 目录下！")

if __name__ == "__main__":
    generate_site()
