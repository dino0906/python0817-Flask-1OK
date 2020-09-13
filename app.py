#https://www.youtube.com/watch?v=3mwFC4SHY-Y
#template夾內 base:html基底;index:首頁顯示框架和{extencs} {blockhead}[endblock];posts:同index頁面
#static/css靜態資料夾 main:設定字形等等
#base內 url_for方法 ('static',filename='css/main.css')
#基本DATA flask串sqlite 結尾def __repl__(self):
#sqlite 欄位設定,主key,屬性,預設值default
#datetime方法 預設值
#設定flask_sqlalchemy,進python環境開啟db; >>from app import db; >>db.create_all()
#>>from app import BlogPost;查詢內容>>BlogPost.query.all();新增會話>>db.session.add(BlogPost(title='Blog Post 1', content='Content of blog in post 01', author='Aaron'))
#指令查詢ex>>BlogPost.query.all()[0].content
#posts.html設定輸入框架
#設定request post;request.form.get(')
#db.session的用途;add()增加;delete()刪除;commit()遞交內容
#BlogPost.query.get(3).author = 'Fake Eric' 直接更改作者

from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(40), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Blog post" + str(self.id)
all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is content of page 1.',
        'author': 'Aaron'
    },
    {
        'title': 'Post 2',
        'content': 'This is content of page 2.'
    }
]
#可以在html直接引用{{ 內容 }}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['POST','GET'])
def posts():
    #1:15:40
    if request.method == 'POST':
        post_title = request.form.get('title')
        post_content = request.form.get('content')
        post_author = request.form.get('author')
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
        
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)
    # return render_template('posts.html' , posts=all_posts) #1次設定

@app.route('/posts/delete/<int:id>', methods=['POST','GET'])
def detele(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['POST','GET'])
def edit(id):

    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.author = request.form.get('author')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['POST','GET'])
def new_post():
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.author = request.form.get('author')
        post.content = request.form.get('content')
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')
    
#         return render_template('new_post.html')



#初創測試
# @app.route('/home/users/<string:name>/posts/<int:id>')   #name,id也要寫入def()內
# def hello(name,id):
#     return 'Hello, ' + name + ', your id is : ' + str(id)

# @app.route('/onlyget', methods=['GET','POST'])  #web使用方式兩個都寫
# def get_req():
#     return 'You can only get this webpage.'

if __name__ == '__main__':
    app.run(debug=True)