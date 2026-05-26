"""
网文创作平台后端 - Flask版本（生产部署）
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__)

# 配置 - 优先读取环境变量，兼容本地开发
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'novel-platform-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres.fmzgfcfcdzyxssjgpvgh:Lzk9710181030@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_recycle': 300,
    'pool_pre_ping': True
}

# CORS - 同域部署不需要限制，兼容本地开发
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*')
CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

db = SQLAlchemy(app)

# ==================== 数据库模型 ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)  # nullable=True，email变为可选
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Novel(db.Model):
    __tablename__ = 'novels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # 用于统计最后更新时间
    today_words = db.Column(db.Integer, default=0)  # 今日字数
    today_date = db.Column(db.Date, nullable=True)  # 记录今日字数的日期

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    word_count = db.Column(db.Integer, default=0)  # 字数统计
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'order': self.order,
            'word_count': self.word_count,
            'novel_id': self.novel_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class World(db.Model):
    __tablename__ = 'worlds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='rules')  # rules/geography/history/culture
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'novel_id': self.novel_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    role = db.Column(db.String(50), default='supporting')  # protagonist/supporting/antagonist
    ability_values = db.Column(db.Text, default='{}')  # JSON格式存储角色能力值
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'role': self.role,
            'ability_values': self.ability_values,
            'novel_id': self.novel_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Timeline(db.Model):
    __tablename__ = 'timelines'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_time = db.Column(db.String(100), default='')  # 故事内时间点（如"第三纪元·仲夏"）
    order = db.Column(db.Integer, default=0)  # 排序
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=True)  # 关联章节
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_time': self.event_time,
            'order': self.order,
            'chapter_id': self.chapter_id,
            'novel_id': self.novel_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserSetting(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    theme = db.Column(db.String(20), default='light')  # light/dark
    auto_save_interval = db.Column(db.Integer, default=30)  # 秒
    ai_provider = db.Column(db.String(50), default='mock')  # mock/openai/claude
    custom_api_url = db.Column(db.String(500), nullable=True)
    custom_api_key = db.Column(db.String(500), nullable=True)
    default_ai_model = db.Column(db.String(100), default='gpt-3.5-turbo')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'theme': self.theme,
            'auto_save_interval': self.auto_save_interval,
            'ai_provider': self.ai_provider,
            'custom_api_url': self.custom_api_url,
            'custom_api_key': self.custom_api_key,
            'default_ai_model': self.default_ai_model,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Draft(db.Model):
    __tablename__ = 'drafts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, default='')
    tags = db.Column(db.String(500), default='')
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'novel_id': self.novel_id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags.split(',') if self.tags else [],
            'version': self.version,
            'word_count': count_words(self.content or ''),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, default='')
    category = db.Column(db.String(50), default='discussion')
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self, include_author=True):
        d = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'likes': self.likes,
            'views': self.views,
            'comment_count': self.comment_count,
            'is_pinned': self.is_pinned,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_author:
            author = User.query.get(self.user_id)
            d['author'] = author.username if author else '未知'
        return d


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        author = User.query.get(self.user_id)
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content,
            'author': author.username if author else '未知',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class LinkedAccount(db.Model):
    __tablename__ = 'linked_accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # bilibili, qidian, tomato, qwen, coze, custom_api 等
    account_name = db.Column(db.String(200), default='')  # 账号名/昵称
    account_id = db.Column(db.String(200), default='')    # 平台用户ID
    access_token = db.Column(db.Text, default='')         # 加密存储的token
    refresh_token = db.Column(db.Text, default='')
    auth_data = db.Column(db.Text, default='')             # 其他认证数据(JSON)
    is_valid = db.Column(db.Boolean, default=True)         # 账号是否有效
    last_verified = db.Column(db.DateTime)                 # 最后验证时间
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self, include_tokens=False):
        d = {
            'id': self.id,
            'user_id': self.user_id,
            'platform': self.platform,
            'account_name': self.account_name,
            'account_id': self.account_id,
            'is_valid': self.is_valid,
            'last_verified': self.last_verified.isoformat() if self.last_verified else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_tokens:
            d['access_token'] = self.access_token[:8] + '...' if self.access_token else ''
            d['auth_data'] = self.auth_data
        return d


class CozeProject(db.Model):
    __tablename__ = 'coze_projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coze_project_id = db.Column(db.String(200), nullable=False)   # 扣子项目ID
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    project_type = db.Column(db.String(50), default='novel')  # novel, worldbuilding, character
    sync_data = db.Column(db.Text, default='')                  # 同步的数据JSON
    local_novel_id = db.Column(db.Integer, nullable=True)       # 关联本地小说ID
    last_synced = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'coze_project_id': self.coze_project_id,
            'title': self.title,
            'description': self.description,
            'project_type': self.project_type,
            'local_novel_id': self.local_novel_id,
            'last_synced': self.last_synced.isoformat() if self.last_synced else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    url = db.Column(db.String(500), nullable=False)
    cover = db.Column(db.String(500), default='')
    source = db.Column(db.String(50), default='bilibili')  # bilibili, user_upload
    category = db.Column(db.String(50), default='writing')  # writing, craft, inspiration, publish
    rating_avg = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self, include_author=True):
        d = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'cover': self.cover,
            'source': self.source,
            'category': self.category,
            'rating_avg': round(self.rating_avg, 1) if self.rating_avg else 0,
            'rating_count': self.rating_count,
            'views': self.views,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_author:
            author = User.query.get(self.user_id)
            d['author'] = author.username if author else '未知'
        return d


class CourseRating(db.Model):
    __tablename__ = 'course_ratings'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 1-5
    review = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('course_id', 'user_id'),)


# ==================== 工具函数 ====================

def create_token(user_id):
    """创建JWT token，30天过期"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


def count_words(text):
    """统计字数（中文按字符，英文按单词）"""
    if not text:
        return 0
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_words = len([w for w in text.split() if any('\u0041' <= c <= '\u005a' or '\u0061' <= c <= '\u007a' for c in w)])
    return chinese_chars + english_words


def require_auth():
    """从请求头获取token并返回user_id，失败返回None"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(data['user_id'])
        if not user:
            return None
        return user.id
    except:
        return None


def update_novel_stats(novel_id):
    """更新小说统计信息"""
    novel = Novel.query.get(novel_id)
    if not novel:
        return
    
    chapters = Chapter.query.filter_by(novel_id=novel_id).all()
    
    # 统计总字数
    total_words = sum(c.word_count or 0 for c in chapters)
    
    # 统计章节数
    chapter_count = len(chapters)
    
    # 计算今日新增字数
    today = datetime.date.today()
    today_words = 0
    
    if novel.today_date == today:
        today_words = novel.today_words
    else:
        # 检查是否有章节今天更新
        for chapter in chapters:
            if chapter.updated_at and chapter.updated_at.date() == today:
                today_words += chapter.word_count or 0
        novel.today_date = today
        novel.today_words = today_words
    
    novel.last_update = datetime.datetime.utcnow()
    
    # 注意：这里不直接设置word_count和chapter_count字段，
    # 而是通过查询chapter来计算
    return {
        'word_count': total_words,
        'chapter_count': chapter_count,
        'today_words': today_words,
        'last_update': novel.last_update.isoformat() if novel.last_update else None
    }


# ==================== 认证接口 ====================

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing required fields: username, password'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # email变为可选，不传则自动生成
    email = data.get('email')
    if not email:
        email = f"{data['username']}@novel.local"
    else:
        # 检查email唯一性（如果提供了的话）
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
    
    user = User(username=data['username'], email=email)
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    # 创建默认用户设置
    setting = UserSetting(user_id=user.id)
    db.session.add(setting)
    db.session.commit()
    
    token = create_token(user.id)
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': user.to_dict()
    }), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    token = create_token(user.id)
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    })


# ==================== 小说接口 ====================

@app.route('/api/v1/novels', methods=['GET'])
@token_required
def get_novels(current_user):
    """获取小说列表，返回分页对象格式"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    page_size = min(page_size, 100)  # 限制最大100条
    
    # 构建基础查询
    query = Novel.query.filter_by(user_id=current_user.id)
    
    # 获取总数
    total = query.count()
    
    # 分页查询
    novels = query.order_by(Novel.updated_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return jsonify({
        'items': [n.to_dict() for n in novels],
        'total': total,
        'page': page,
        'page_size': page_size
    })


@app.route('/api/v1/novels', methods=['POST'])
@token_required
def create_novel(current_user):
    data = request.get_json()
    novel = Novel(
        title=data.get('title', '未命名小说'),
        description=data.get('description', ''),
        status=data.get('status', 'draft'),
        user_id=current_user.id
    )
    db.session.add(novel)
    db.session.commit()
    return jsonify(novel.to_dict()), 201


@app.route('/api/v1/novels/<int:id>', methods=['GET'])
@token_required
def get_novel(current_user, id):
    novel = Novel.query.filter_by(id=id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    return jsonify(novel.to_dict())


@app.route('/api/v1/novels/<int:id>', methods=['PUT'])
@token_required
def update_novel(current_user, id):
    novel = Novel.query.filter_by(id=id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    data = request.get_json()
    if 'title' in data:
        novel.title = data['title']
    if 'description' in data:
        novel.description = data['description']
    if 'status' in data:
        novel.status = data['status']
    
    db.session.commit()
    return jsonify(novel.to_dict())


@app.route('/api/v1/novels/<int:id>', methods=['DELETE'])
@token_required
def delete_novel(current_user, id):
    novel = Novel.query.filter_by(id=id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    # 同步删除关联的世界观、角色、章节
    World.query.filter_by(novel_id=id).delete()
    Character.query.filter_by(novel_id=id).delete()
    Chapter.query.filter_by(novel_id=id).delete()
    
    db.session.delete(novel)
    db.session.commit()
    return jsonify({'message': 'Novel deleted'})


@app.route('/api/v1/novels/<int:id>/stats', methods=['GET'])
@token_required
def get_novel_stats(current_user, id):
    """获取作品统计信息"""
    novel = Novel.query.filter_by(id=id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    stats = update_novel_stats(id)
    db.session.commit()
    
    return jsonify(stats)


# ==================== 章节接口 ====================

@app.route('/api/v1/novels/<int:novel_id>/chapters', methods=['GET'])
@token_required
def get_chapters(current_user, novel_id):
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    chapters = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.order).all()
    return jsonify([c.to_dict() for c in chapters])


@app.route('/api/v1/novels/<int:novel_id>/chapters', methods=['POST'])
@token_required
def create_chapter(current_user, novel_id):
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    data = request.get_json()
    last_chapter = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.order.desc()).first()
    order = (last_chapter.order + 1) if last_chapter else 1
    
    content = data.get('content', '')
    word_count = count_words(content)
    
    chapter = Chapter(
        title=data.get('title', '新章节'),
        content=content,
        order=order,
        word_count=word_count,
        novel_id=novel_id
    )
    db.session.add(chapter)
    db.session.commit()
    
    # 更新小说统计
    update_novel_stats(novel_id)
    db.session.commit()
    
    return jsonify(chapter.to_dict()), 201


@app.route('/api/v1/chapters/<int:id>', methods=['GET'])
@token_required
def get_chapter(current_user, id):
    """获取单个章节"""
    chapter = Chapter.query.get(id)
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    
    novel = Novel.query.filter_by(id=chapter.novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(chapter.to_dict())


@app.route('/api/v1/chapters/<int:id>', methods=['PUT'])
@token_required
def update_chapter(current_user, id):
    chapter = Chapter.query.get(id)
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    
    novel = Novel.query.filter_by(id=chapter.novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    if 'title' in data:
        chapter.title = data['title']
    if 'content' in data:
        old_word_count = chapter.word_count or 0
        chapter.content = data['content']
        chapter.word_count = count_words(data['content'])
        # 更新今日字数
        today = datetime.date.today()
        if novel.today_date == today:
            novel.today_words += (chapter.word_count - old_word_count)
        else:
            novel.today_date = today
            novel.today_words = chapter.word_count - old_word_count
    
    if 'order' in data:
        chapter.order = data['order']
    
    db.session.commit()
    return jsonify(chapter.to_dict())


@app.route('/api/v1/chapters/<int:id>', methods=['DELETE'])
@token_required
def delete_chapter(current_user, id):
    """删除章节"""
    chapter = Chapter.query.get(id)
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    
    novel = Novel.query.filter_by(id=chapter.novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(chapter)
    db.session.commit()
    
    # 更新小说统计
    update_novel_stats(novel.id)
    db.session.commit()
    
    return jsonify({'message': 'Chapter deleted'})


# ==================== 世界观接口（挂到小说下） ====================

@app.route('/api/v1/novels/<int:novel_id>/worlds', methods=['GET'])
@token_required
def get_worlds(current_user, novel_id):
    """获取小说下的世界观列表"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    category = request.args.get('category')
    query = World.query.filter_by(novel_id=novel_id, user_id=current_user.id)
    
    if category:
        query = query.filter_by(category=category)
    
    worlds = query.all()
    return jsonify([w.to_dict() for w in worlds])


@app.route('/api/v1/novels/<int:novel_id>/worlds', methods=['POST'])
@token_required
def create_world(current_user, novel_id):
    """创建世界观"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    data = request.get_json()
    world = World(
        name=data.get('name', '新世界观'),
        description=data.get('description', ''),
        category=data.get('category', 'rules'),
        novel_id=novel_id,
        user_id=current_user.id
    )
    db.session.add(world)
    db.session.commit()
    return jsonify(world.to_dict()), 201


@app.route('/api/v1/novels/<int:novel_id>/worlds/<int:world_id>', methods=['GET'])
@token_required
def get_world(current_user, novel_id, world_id):
    """获取单个世界观"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    world = World.query.filter_by(id=world_id, novel_id=novel_id, user_id=current_user.id).first()
    if not world:
        return jsonify({'error': 'World not found'}), 404
    
    return jsonify(world.to_dict())


@app.route('/api/v1/novels/<int:novel_id>/worlds/<int:world_id>', methods=['PUT'])
@token_required
def update_world(current_user, novel_id, world_id):
    """更新世界观"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    world = World.query.filter_by(id=world_id, novel_id=novel_id, user_id=current_user.id).first()
    if not world:
        return jsonify({'error': 'World not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        world.name = data['name']
    if 'description' in data:
        world.description = data['description']
    if 'category' in data:
        world.category = data['category']
    
    db.session.commit()
    return jsonify(world.to_dict())


@app.route('/api/v1/novels/<int:novel_id>/worlds/<int:world_id>', methods=['DELETE'])
@token_required
def delete_world(current_user, novel_id, world_id):
    """删除世界观"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    world = World.query.filter_by(id=world_id, novel_id=novel_id, user_id=current_user.id).first()
    if not world:
        return jsonify({'error': 'World not found'}), 404
    
    db.session.delete(world)
    db.session.commit()
    return jsonify({'message': 'World deleted'})


# ==================== 角色接口（挂到小说下） ====================

@app.route('/api/v1/novels/<int:novel_id>/characters', methods=['GET'])
@token_required
def get_characters(current_user, novel_id):
    """获取小说下的角色列表"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    role = request.args.get('role')
    query = Character.query.filter_by(novel_id=novel_id, user_id=current_user.id)
    
    if role:
        query = query.filter_by(role=role)
    
    characters = query.all()
    return jsonify([c.to_dict() for c in characters])


@app.route('/api/v1/novels/<int:novel_id>/characters', methods=['POST'])
@token_required
def create_character(current_user, novel_id):
    """创建角色"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    data = request.get_json()
    ability_values = data.get('ability_values', {})
    if isinstance(ability_values, dict):
        import json
        ability_values = json.dumps(ability_values)
    
    character = Character(
        name=data.get('name', '新角色'),
        description=data.get('description', ''),
        role=data.get('role', 'supporting'),
        ability_values=ability_values,
        novel_id=novel_id,
        user_id=current_user.id
    )
    db.session.add(character)
    db.session.commit()
    return jsonify(character.to_dict()), 201


@app.route('/api/v1/novels/<int:novel_id>/characters/<int:character_id>', methods=['GET'])
@token_required
def get_character(current_user, novel_id, character_id):
    """获取单个角色"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    character = Character.query.filter_by(id=character_id, novel_id=novel_id, user_id=current_user.id).first()
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    
    return jsonify(character.to_dict())


@app.route('/api/v1/novels/<int:novel_id>/characters/<int:character_id>', methods=['PUT'])
@token_required
def update_character(current_user, novel_id, character_id):
    """更新角色"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    character = Character.query.filter_by(id=character_id, novel_id=novel_id, user_id=current_user.id).first()
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        character.name = data['name']
    if 'description' in data:
        character.description = data['description']
    if 'role' in data:
        character.role = data['role']
    if 'ability_values' in data:
        ability_values = data['ability_values']
        if isinstance(ability_values, dict):
            import json
            ability_values = json.dumps(ability_values)
        character.ability_values = ability_values
    
    db.session.commit()
    return jsonify(character.to_dict())


@app.route('/api/v1/novels/<int:novel_id>/characters/<int:character_id>', methods=['DELETE'])
@token_required
def delete_character(current_user, novel_id, character_id):
    """删除角色"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    character = Character.query.filter_by(id=character_id, novel_id=novel_id, user_id=current_user.id).first()
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    
    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Character deleted'})


# ==================== 时间线接口（挂到小说下） ====================

@app.route('/api/v1/novels/<int:novel_id>/timelines', methods=['GET'])
@token_required
def get_timelines(current_user, novel_id):
    """获取小说下的时间线事件列表"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    timelines = Timeline.query.filter_by(novel_id=novel_id, user_id=current_user.id).order_by(Timeline.order, Timeline.id).all()
    return jsonify([t.to_dict() for t in timelines])


@app.route('/api/v1/novels/<int:novel_id>/timelines', methods=['POST'])
@token_required
def create_timeline(current_user, novel_id):
    """创建时间线事件"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    data = request.get_json()
    # 自动计算order
    max_order = db.session.query(db.func.max(Timeline.order)).filter_by(novel_id=novel_id).scalar() or 0
    timeline = Timeline(
        title=data.get('title', '新事件'),
        description=data.get('description', ''),
        event_time=data.get('event_time', ''),
        order=data.get('order', max_order + 1),
        chapter_id=data.get('chapter_id'),
        novel_id=novel_id,
        user_id=current_user.id
    )
    db.session.add(timeline)
    db.session.commit()
    return jsonify(timeline.to_dict()), 201


@app.route('/api/v1/novels/<int:novel_id>/timelines/<int:timeline_id>', methods=['PUT'])
@token_required
def update_timeline(current_user, novel_id, timeline_id):
    """更新时间线事件"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    timeline = Timeline.query.filter_by(id=timeline_id, novel_id=novel_id, user_id=current_user.id).first()
    if not timeline:
        return jsonify({'error': 'Timeline event not found'}), 404
    data = request.get_json()
    if 'title' in data:
        timeline.title = data['title']
    if 'description' in data:
        timeline.description = data['description']
    if 'event_time' in data:
        timeline.event_time = data['event_time']
    if 'order' in data:
        timeline.order = data['order']
    if 'chapter_id' in data:
        timeline.chapter_id = data['chapter_id']
    db.session.commit()
    return jsonify(timeline.to_dict())


@app.route('/api/v1/novels/<int:novel_id>/timelines/<int:timeline_id>', methods=['DELETE'])
@token_required
def delete_timeline(current_user, novel_id, timeline_id):
    """删除时间线事件"""
    novel = Novel.query.filter_by(id=novel_id, user_id=current_user.id).first()
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    timeline = Timeline.query.filter_by(id=timeline_id, novel_id=novel_id, user_id=current_user.id).first()
    if not timeline:
        return jsonify({'error': 'Timeline event not found'}), 404
    db.session.delete(timeline)
    db.session.commit()
    return jsonify({'message': 'Timeline event deleted'})


# ==================== 用户设置接口 ====================

@app.route('/api/v1/users/settings', methods=['GET'])
@token_required
def get_user_settings(current_user):
    """获取用户设置"""
    setting = UserSetting.query.filter_by(user_id=current_user.id).first()
    if not setting:
        # 如果没有设置，创建默认设置
        setting = UserSetting(user_id=current_user.id)
        db.session.add(setting)
        db.session.commit()
    return jsonify(setting.to_dict())


@app.route('/api/v1/users/settings', methods=['PUT'])
@token_required
def update_user_settings(current_user):
    """更新用户设置"""
    setting = UserSetting.query.filter_by(user_id=current_user.id).first()
    if not setting:
        setting = UserSetting(user_id=current_user.id)
        db.session.add(setting)
    
    data = request.get_json()
    if 'theme' in data:
        setting.theme = data['theme']
    if 'auto_save_interval' in data:
        setting.auto_save_interval = data['auto_save_interval']
    if 'ai_provider' in data:
        setting.ai_provider = data['ai_provider']
    if 'custom_api_url' in data:
        setting.custom_api_url = data['custom_api_url']
    if 'custom_api_key' in data:
        setting.custom_api_key = data['custom_api_key']
    if 'default_ai_model' in data:
        setting.default_ai_model = data['default_ai_model']
    
    db.session.commit()
    return jsonify(setting.to_dict())


# ==================== AI写作接口 ====================

# 风格模板
STYLE_TEMPLATES = {
    'serious': '【严肃文学风格】细腻、深沉、富有哲理，注重人物内心描写',
    'humor': '【轻松幽默风格】诙谐、活泼、接地气，对话生动有趣',
    'action': '【热血战斗风格】激情、热血、战斗场面激烈',
    'mystery': '【悬疑推理风格】紧张、烧脑、逻辑严密',
    'romance': '【浪漫言情风格】甜蜜、细腻、情感丰富',
    'scifi': '【科幻未来风格】前沿、想象、科技感强'
}

MODE_TEMPLATES = {
    'continue': '续写以下内容，保持文风一致，情节连贯自然：',
    'polish': '润色以下文字，提升文笔和表达力：',
    'expand': '扩写以下内容，增加细节和描写：',
    'outline': '为一个小说生成详细章节大纲：',
    'summary': '为以下内容生成简要摘要，提取核心要点：'
}


def generate_mock_content(mode, prompt, style='humor'):
    """生成模拟内容"""
    style_desc = STYLE_TEMPLATES.get(style, STYLE_TEMPLATES['humor'])
    mode_desc = MODE_TEMPLATES.get(mode, MODE_TEMPLATES['continue'])
    
    if mode == 'continue':
        return f"""<p>{style_desc}</p>
<p>{mode_desc}</p>
<p>在这个充满未知的时刻，故事迎来了新的转折。</p>
<p>主角站在原地，望着远方的天际线，心中涌起一股难以言喻的情绪。刚才发生的一切仿佛还在眼前回荡，那些惊心动魄的画面挥之不去。</p>
<p>"这...怎么可能..."他喃喃自语，声音中带着几分颤抖。</p>
<p>就在这时，一个神秘的声音在耳边响起，打断了他的思绪。月光透过云层洒落，照亮了前方蜿蜒的小路。</p>
<p>他深吸一口气，迈开了步伐。夜风呼啸而过，带着一丝凉意，却无法冷却他内心翻涌的热血。</p>"""
    
    elif mode == 'polish':
        return f"""<p>{style_desc}</p>
<p>【润色后】</p>
<p>在这个充满未知的时刻，故事迎来了新的转折。</p>
<p>主角静静地伫立在原地，目光投向远方的天际。夕阳的余晖洒在他的脸庞，勾勒出一道金色的轮廓。</p>
<p>方才发生的一切犹如电影般在眼前重现——那些惊心动魄的画面如同烙印般刻在脑海里，挥之不去。</p>
<p>"这……怎么可能……"他低声呢喃，声线中透着几分颤抖，却难掩眼眸深处的坚定。</p>
<p>夜幕渐渐降临，而他即将踏上一段全新的旅程。</p>"""
    
    elif mode == 'expand':
        return f"""<p>{style_desc}</p>
<p>【扩写版】</p>
<p>在这个充满未知的时刻，故事迎来了新的转折。</p>
<p>主角站在原地，目光凝视着远方的天际线。夕阳的余晖如同金色的纱幔，轻轻披在他的肩上。微风拂过，带起他衣角的同时，也带走了白日的喧嚣。</p>
<p>刚才发生的一切如同一场梦，却又如此真实。刀光剑影、惊心动魄的战斗场面还在脑海中回荡。那些熟悉的面孔、那些生死相依的瞬间，都在这一刻变得模糊起来，却又无比珍贵。</p>
<p>他深吸一口气，感受着空气中弥漫的尘土与花草的清香。这是属于这个世界的气息，熟悉又陌生。</p>
<p>"这...真的结束了吗？"他喃喃自语，声音中带着几分不确定。</p>
<p>远方传来一阵马蹄声，打破了傍晚的宁静。他抬起头，目光中闪过一丝期待与警惕。</p>"""
    
    elif mode == 'outline':
        return f"""<p><strong>【小说大纲】</strong></p>
<p><em>主题：{prompt}</em></p>
<p><strong>第一章 命运的起点</strong></p>
<p>• 1.1 平凡的日常 - 介绍主角的背景和性格</p>
<p>• 1.2 意外的相遇 - 命运的转折点</p>
<p>• 1.3 隐藏的秘密 - 为主线埋下伏笔</p>
<p><strong>第二章 觉醒</strong></p>
<p>• 2.1 危机降临 - 平静被打破</p>
<p>• 2.2 力量的觉醒 - 主角发现自己的特殊能力</p>
<p>• 2.3 新的同伴 - 重要配角登场</p>
<p><strong>第三章 挑战</strong></p>
<p>• 3.1 首次考验 - 面对第一个重大挑战</p>
<p>• 3.2 成长的代价 - 付出和牺牲</p>
<p>• 3.3 友情的力量 - 团队协作</p>
<p><strong>第四章 抉择</strong></p>
<p>• 4.1 真相大白 - 揭露重大秘密</p>
<p>• 4.2 艰难的抉择 - 面临人生重要选择</p>
<p>• 4.3 踏上新征程 - 开启新的冒险</p>"""
    
    else:  # summary
        return f"""<p><strong>【内容摘要】</strong></p>
<p><strong>核心要点：</strong></p>
<p>• <strong>背景</strong>：现代都市/奇幻世界</p>
<p>• <strong>主要人物</strong>：主角（身份待揭示）、神秘人物</p>
<p>• <strong>核心冲突</strong>：围绕某个重要秘密或任务展开</p>
<p>• <strong>情节走向</strong>：悬念铺垫，暗示更大的危机即将来临</p>
<p>• <strong>关键信息</strong>：{prompt[:50] if prompt else '暂无'}...</p>
<p><strong>总结：</strong>故事以紧张的氛围开篇，通过细腻的描写展现了主角内心的挣扎与坚定。伏笔的埋设暗示着后续将有更大的冲突和发展。</p>"""


@app.route('/api/v1/ai/generate', methods=['POST'])
@token_required
def ai_generate(current_user):
    """AI生成内容"""
    data = request.get_json()
    mode = data.get('mode', 'continue')
    prompt = data.get('prompt', '')
    style = data.get('style', 'humor')
    
    # 获取用户设置中的AI提供商信息
    setting = UserSetting.query.filter_by(user_id=current_user.id).first()
    ai_provider = setting.ai_provider if setting else 'mock'
    
    # 如果是mock模式或用户未配置自定义API，使用mock内容
    if ai_provider == 'mock' or not setting or not setting.custom_api_key:
        generated_text = generate_mock_content(mode, prompt, style)
    else:
        # 这里可以扩展为调用实际的AI API
        # 目前仍返回mock内容，实际项目中需要调用外部API
        generated_text = generate_mock_content(mode, prompt, style)
    
    return jsonify({
        'generated_text': generated_text,
        'prompt': prompt,
        'mode': mode,
        'style': style
    })


@app.route('/api/v1/ai/modes', methods=['GET'])
def get_ai_modes():
    """获取AI写作模式列表"""
    return jsonify({
        'modes': [
            {'value': 'continue', 'name': '续写', 'icon': '📝', 'desc': '根据已有内容继续创作'},
            {'value': 'polish', 'name': '润色', 'icon': '✨', 'desc': '优化现有文字'},
            {'value': 'expand', 'name': '扩写', 'icon': '📖', 'desc': '扩展深化内容'},
            {'value': 'outline', 'name': '大纲', 'icon': '📋', 'desc': '生成章节大纲'},
            {'value': 'summary', 'name': '摘要', 'icon': '📄', 'desc': '生成内容摘要'}
        ],
        'styles': [
            {'value': 'serious', 'name': '严肃文学'},
            {'value': 'humor', 'name': '轻松幽默'},
            {'value': 'action', 'name': '热血战斗'},
            {'value': 'mystery', 'name': '悬疑推理'},
            {'value': 'romance', 'name': '浪漫言情'},
            {'value': 'scifi', 'name': '科幻未来'}
        ]
    })


# ==================== 公开接口（无需登录） ====================

@app.route('/api/v1/public/novels', methods=['GET'])
def public_novels():
    """公开浏览作品列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    category = request.args.get('category', '')
    
    query = Novel.query
    if category:
        query = query.filter(Novel.description.ilike(f'%{category}%'))
    
    pagination = query.order_by(Novel.last_update.desc()).paginate(page=page, per_page=page_size, error_out=False)
    
    items = []
    for n in pagination.items:
        author = User.query.get(n.user_id)
        chapters = Chapter.query.filter_by(novel_id=n.id).all()
        total_words = sum(c.word_count or 0 for c in chapters)
        items.append({
            'id': n.id,
            'title': n.title,
            'desc': n.description or '',
            'author': author.username if author else '未知',
            'words': total_words,
            'views': len(chapters) * 120 + total_words // 10,
            'category': n.status or 'other',
            'tags': [],
            'status': '连载中' if n.last_update and (datetime.datetime.utcnow() - n.last_update).days < 30 else '已完结',
            'chapters': [{'id': c.id, 'title': c.title} for c in chapters[:5]],
            'coverColor': _novel_color(n.id)
        })
    
    return jsonify({
        'items': items,
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })


def _novel_color(nid):
    colors = [
        'linear-gradient(135deg, #c7d2fe, #a5b4fc)',
        'linear-gradient(135deg, #ddd6fe, #c4b5fd)',
        'linear-gradient(135deg, #bbf7d0, #86efac)',
        'linear-gradient(135deg, #fed7aa, #fdba74)',
        'linear-gradient(135deg, #a5f3fc, #67e8f9)',
        'linear-gradient(135deg, #fecaca, #fca5a5)',
        'linear-gradient(135deg, #fde68a, #fcd34d)',
        'linear-gradient(135deg, #c4b5fd, #a78bfa)',
    ]
    return colors[nid % len(colors)]


@app.route('/api/v1/public/novels/<int:id>', methods=['GET'])
def public_novel_detail(id):
    """公开浏览作品详情"""
    novel = Novel.query.get(id)
    if not novel:
        return jsonify({'error': 'Novel not found'}), 404
    
    author = User.query.get(novel.user_id)
    chapters = Chapter.query.filter_by(novel_id=id).all()
    total_words = sum(c.word_count or 0 for c in chapters)
    
    return jsonify({
        'id': novel.id,
        'title': novel.title,
        'desc': novel.description or '',
        'author': author.username if author else '未知',
        'words': total_words,
        'views': len(chapters) * 120 + total_words // 10,
        'category': novel.status or 'other',
        'tags': [],
        'status': '连载中',
        'coverColor': _novel_color(novel.id),
        'chapters': [{'id': c.id, 'title': c.title} for c in chapters],
        'created_at': novel.created_at.isoformat() if novel.created_at else None
    })


@app.route('/api/v1/public/rank', methods=['GET'])
def public_rank():
    """排行榜"""
    novels = Novel.query.order_by(Novel.last_update.desc()).limit(50).all()
    items = []
    for n in novels:
        author = User.query.get(n.user_id)
        chapters = Chapter.query.filter_by(novel_id=n.id).all()
        total_words = sum(c.word_count or 0 for c in chapters)
        views = len(chapters) * 120 + total_words // 10
        items.append({
            'id': n.id, 'title': n.title, 'author': author.username if author else '未知',
            'words': total_words, 'views': views, 'category': n.status or 'other',
            'tags': []
        })
    items.sort(key=lambda x: x['views'], reverse=True)
    return jsonify({'items': items})


# ==================== 草稿箱接口 ====================

@app.route('/api/v1/drafts', methods=['GET'])
@token_required
def get_drafts(current_user):
    """获取草稿列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    novel_id = request.args.get('novel_id', type=int)
    
    query = Draft.query.filter_by(user_id=current_user.id)
    if novel_id:
        query = query.filter_by(novel_id=novel_id)
    
    pagination = query.order_by(Draft.updated_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return jsonify({
        'items': [d.to_dict() for d in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })


@app.route('/api/v1/drafts', methods=['POST'])
@token_required
def create_draft(current_user):
    """创建草稿"""
    data = request.get_json()
    draft = Draft(
        user_id=current_user.id,
        novel_id=data.get('novel_id'),
        title=data.get('title', '未命名草稿'),
        content=data.get('content', ''),
        tags=','.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else data.get('tags', '')
    )
    db.session.add(draft)
    db.session.commit()
    return jsonify(draft.to_dict()), 201


@app.route('/api/v1/drafts/<int:id>', methods=['GET'])
@token_required
def get_draft(current_user, id):
    """获取草稿详情"""
    draft = Draft.query.filter_by(id=id, user_id=current_user.id).first()
    if not draft:
        return jsonify({'error': 'Draft not found'}), 404
    return jsonify(draft.to_dict())


@app.route('/api/v1/drafts/<int:id>', methods=['PUT'])
@token_required
def update_draft(current_user, id):
    """更新草稿"""
    draft = Draft.query.filter_by(id=id, user_id=current_user.id).first()
    if not draft:
        return jsonify({'error': 'Draft not found'}), 404
    
    data = request.get_json()
    if 'title' in data:
        draft.title = data['title']
    if 'content' in data:
        draft.content = data['content']
    if 'tags' in data:
        draft.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
    draft.version += 1
    
    db.session.commit()
    return jsonify(draft.to_dict())


@app.route('/api/v1/drafts/<int:id>', methods=['DELETE'])
@token_required
def delete_draft(current_user, id):
    """删除草稿"""
    draft = Draft.query.filter_by(id=id, user_id=current_user.id).first()
    if not draft:
        return jsonify({'error': 'Draft not found'}), 404
    db.session.delete(draft)
    db.session.commit()
    return jsonify({'message': 'Draft deleted'})


# ==================== 论坛接口 ====================

@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    """获取帖子列表（公开）"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    category = request.args.get('category', '')
    
    query = Post.query
    if category:
        query = query.filter_by(category=category)
    
    pagination = query.order_by(Post.is_pinned.desc(), Post.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return jsonify({
        'items': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })


@app.route('/api/v1/posts', methods=['POST'])
@token_required
def create_post(current_user):
    """创建帖子"""
    data = request.get_json()
    post = Post(
        user_id=current_user.id,
        title=data.get('title', ''),
        content=data.get('content', ''),
        category=data.get('category', 'discussion')
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@app.route('/api/v1/posts/<int:id>', methods=['GET'])
def get_post(id):
    """获取帖子详情（公开）"""
    post = Post.query.get(id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    post.views += 1
    db.session.commit()
    comments = Comment.query.filter_by(post_id=id).order_by(Comment.created_at.asc()).all()
    result = post.to_dict()
    result['comments'] = [c.to_dict() for c in comments]
    return jsonify(result)


@app.route('/api/v1/posts/<int:id>', methods=['DELETE'])
@token_required
def delete_post(current_user, id):
    """删除帖子"""
    post = Post.query.filter_by(id=id, user_id=current_user.id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    Comment.query.filter_by(post_id=id).delete()
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})


@app.route('/api/v1/posts/<int:id>/like', methods=['POST'])
@token_required
def like_post(current_user, id):
    """点赞帖子"""
    post = Post.query.get(id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    post.likes += 1
    db.session.commit()
    return jsonify({'likes': post.likes})


@app.route('/api/v1/posts/<int:id>/comments', methods=['POST'])
@token_required
def create_comment(current_user, id):
    """创建评论"""
    post = Post.query.get(id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    data = request.get_json()
    comment = Comment(
        post_id=id,
        user_id=current_user.id,
        content=data.get('content', '')
    )
    post.comment_count += 1
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201


# ==================== 数据看板接口 ====================

@app.route('/api/v1/stats/dashboard', methods=['GET'])
@token_required
def stats_dashboard(current_user):
    """数据看板"""
    novels = Novel.query.filter_by(user_id=current_user.id).all()
    
    total_novels = len(novels)
    total_words = 0
    total_chapters = 0
    novel_stats = []
    
    for n in novels:
        chapters = Chapter.query.filter_by(novel_id=n.id).all()
        words = sum(c.word_count or 0 for c in chapters)
        total_words += words
        total_chapters += len(chapters)
        
        # 模拟7天数据
        import random
        daily_views = [random.randint(50, 500) for _ in range(7)]
        novel_stats.append({
            'id': n.id,
            'title': n.title,
            'words': words,
            'chapters': len(chapters),
            'views': words // 10 + len(chapters) * 80,
            'daily_views': daily_views
        })
    
    import random
    # 模拟7天趋势
    dates = [(datetime.datetime.utcnow() - datetime.timedelta(days=6-i)).strftime('%m/%d') for i in range(7)]
    
    return jsonify({
        'summary': {
            'total_novels': total_novels,
            'total_words': total_words,
            'total_chapters': total_chapters,
            'total_views': total_words // 10 + total_chapters * 80
        },
        'trend': {
            'dates': dates,
            'views': [random.randint(200, 800) for _ in range(7)],
            'words': [random.randint(500, 3000) for _ in range(7)]
        },
        'novels': novel_stats,
        'platform_distribution': [
            {'name': '番茄小说', 'value': random.randint(20, 50)},
            {'name': '起点中文网', 'value': random.randint(15, 40)},
            {'name': '七猫小说', 'value': random.randint(10, 30)},
            {'name': '飞卢小说', 'value': random.randint(5, 20)},
        ]
    })


# ==================== API信息端点 ====================

@app.route('/api/info')
def api_info():
    return jsonify({
        'message': '网文创作平台API',
        'version': '0.3.0'
    })


# ==================== 初始化 ====================

with app.app_context():
    db.create_all()
    # 初始化种子课程数据
    if Course.query.count() == 0:
        seed_courses = [
            {'title': '尼尔·盖曼：如何寻找灵感与建立个人风格', 'description': '从日常生活中发掘写作素材，逐步形成独特的个人风格，适合缺乏灵感的新手建立写作信心', 'url': 'https://search.bilibili.com/all?keyword=尼尔盖曼写作课', 'source': 'bilibili', 'category': 'inspiration', 'is_featured': True, 'is_approved': True},
            {'title': '查理老师：人物塑造与场景画面感构建', 'description': '聚焦人物设定、画面感营造以及如何制造故事冲突与节奏感，风趣幽默不枯燥', 'url': 'https://search.bilibili.com/all?keyword=查理老师编剧课', 'source': 'bilibili', 'category': 'craft', 'is_featured': True, 'is_approved': True},
            {'title': '大啊毛君：对话与转场写作实战', 'description': '如何写出自然的对话、流畅的场景转换、细腻的心理描写，全是实战干货', 'url': 'https://search.bilibili.com/all?keyword=大啊毛君写作', 'source': 'bilibili', 'category': 'craft', 'is_featured': True, 'is_approved': True},
            {'title': '扑街懒蚂蚁：核心梗解析与素材方向', 'description': '透彻讲解核心梗，帮你明确素材收集方向，围绕中心点构建故事', 'url': 'https://search.bilibili.com/all?keyword=扑街懒蚂蚁核心梗', 'source': 'bilibili', 'category': 'writing', 'is_featured': True, 'is_approved': True},
            {'title': '老白大师：情绪拉扯写作手法', 'description': '通过具体实例拆解情绪拉扯技巧，有效提升故事吸引力和读者代入感', 'url': 'https://search.bilibili.com/all?keyword=老白大师情绪拉扯', 'source': 'bilibili', 'category': 'craft', 'is_featured': True, 'is_approved': True},
            {'title': '从零开始写网文：大纲与细纲实战', 'description': '完整网文大纲教程，从立意到细纲，目标-结尾-填坑全流程讲解', 'url': 'https://www.bilibili.com/opus/1083531029470248983', 'source': 'bilibili', 'category': 'writing', 'is_featured': True, 'is_approved': True},
            {'title': '0基础入门小说创作', 'description': '冲突与高潮设计、骨架搭建、人物设计与情节推进，新手必看', 'url': 'https://m.bilibili.com/opus/689044072921301028', 'source': 'bilibili', 'category': 'writing', 'is_featured': False, 'is_approved': True},
            {'title': '创作一本小说前期准备（保姆级）', 'description': '不同类型小说的创建前期准备，传统玄幻修真文为例，超详细不藏私版', 'url': 'https://www.bilibili.com/opus/790601130327408720', 'source': 'bilibili', 'category': 'writing', 'is_featured': False, 'is_approved': True},
        ]
        for c in seed_courses:
            course = Course(
                user_id=1,
                title=c['title'], description=c['description'], url=c['url'],
                source=c['source'], category=c['category'],
                is_featured=c['is_featured'], is_approved=c['is_approved'],
                rating_avg=4.5 if c['is_featured'] else 4.2,
                rating_count=0
            )
            db.session.add(course)
        db.session.commit()


# ==================== 前端静态文件服务 ====================

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('static/assets', filename)


# 根路径返回前端首页
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def serve_frontend(path):
    # API请求不走这里
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    # 静态资源
    if path.startswith('assets/'):
        return send_from_directory('static', path)
    # 其他所有路径返回index.html（SPA路由）
    return send_from_directory('static', 'index.html')


# ==================== 关联账号 API ====================

@app.route('/api/v1/accounts', methods=['GET'])
def get_accounts():
    """获取用户的关联账号列表"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    accounts = LinkedAccount.query.filter_by(user_id=user_id).order_by(LinkedAccount.created_at.desc()).all()
    return jsonify([a.to_dict(include_tokens=True) for a in accounts])


@app.route('/api/v1/accounts', methods=['POST'])
def add_account():
    """添加关联账号"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    data = request.get_json()
    if not data or not data.get('platform'):
        return jsonify({'message': '请指定平台'}), 400
    
    # 检查是否已存在同平台账号
    existing = LinkedAccount.query.filter_by(user_id=user_id, platform=data['platform'], account_id=data.get('account_id', '')).first()
    if existing:
        # 更新已有记录
        existing.account_name = data.get('account_name', existing.account_name)
        if data.get('access_token'):
            existing.access_token = data['access_token']
        if data.get('refresh_token'):
            existing.refresh_token = data['refresh_token']
        if data.get('auth_data'):
            existing.auth_data = data['auth_data']
        existing.is_valid = True
        existing.last_verified = datetime.datetime.utcnow()
        db.session.commit()
        return jsonify(existing.to_dict(include_tokens=True))
    
    account = LinkedAccount(
        user_id=user_id,
        platform=data['platform'],
        account_name=data.get('account_name', ''),
        account_id=data.get('account_id', ''),
        access_token=data.get('access_token', ''),
        refresh_token=data.get('refresh_token', ''),
        auth_data=data.get('auth_data', ''),
        is_valid=True,
        last_verified=datetime.datetime.utcnow()
    )
    db.session.add(account)
    db.session.commit()
    return jsonify(account.to_dict(include_tokens=True)), 201


@app.route('/api/v1/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    """更新关联账号"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    account = LinkedAccount.query.filter_by(id=id, user_id=user_id).first()
    if not account:
        return jsonify({'message': '账号不存在'}), 404
    
    data = request.get_json()
    if data.get('account_name'):
        account.account_name = data['account_name']
    if data.get('access_token'):
        account.access_token = data['access_token']
    if data.get('refresh_token'):
        account.refresh_token = data['refresh_token']
    if data.get('auth_data'):
        account.auth_data = data['auth_data']
    if 'is_valid' in data:
        account.is_valid = data['is_valid']
    account.last_verified = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(account.to_dict(include_tokens=True))


@app.route('/api/v1/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    """删除关联账号"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    account = LinkedAccount.query.filter_by(id=id, user_id=user_id).first()
    if not account:
        return jsonify({'message': '账号不存在'}), 404
    
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': '已删除'})


@app.route('/api/v1/accounts/<int:id>/verify', methods=['POST'])
def verify_account(id):
    """验证关联账号是否有效"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    account = LinkedAccount.query.filter_by(id=id, user_id=user_id).first()
    if not account:
        return jsonify({'message': '账号不存在'}), 404
    
    # 简单标记验证时间（实际应根据平台调用验证API）
    account.last_verified = datetime.datetime.utcnow()
    account.is_valid = True
    db.session.commit()
    return jsonify({'is_valid': True, 'last_verified': account.last_verified.isoformat()})


# ==================== 扣子项目同步 API ====================

@app.route('/api/v1/coze-projects', methods=['GET'])
def get_coze_projects():
    """获取用户的扣子项目列表"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    projects = CozeProject.query.filter_by(user_id=user_id).order_by(CozeProject.created_at.desc()).all()
    return jsonify([p.to_dict() for p in projects])


@app.route('/api/v1/coze-projects', methods=['POST'])
def sync_coze_project():
    """同步扣子项目到数据库"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'message': '项目标题不能为空'}), 400
    
    coze_id = data.get('coze_project_id', f'local_{datetime.datetime.utcnow().timestamp()}')
    
    # 查找是否已同步
    existing = CozeProject.query.filter_by(user_id=user_id, coze_project_id=coze_id).first()
    if existing:
        existing.title = data['title']
        existing.description = data.get('description', existing.description)
        existing.project_type = data.get('project_type', existing.project_type)
        existing.sync_data = data.get('sync_data', existing.sync_data)
        if data.get('local_novel_id'):
            existing.local_novel_id = data['local_novel_id']
        existing.last_synced = datetime.datetime.utcnow()
        db.session.commit()
        return jsonify(existing.to_dict())
    
    project = CozeProject(
        user_id=user_id,
        coze_project_id=coze_id,
        title=data['title'],
        description=data.get('description', ''),
        project_type=data.get('project_type', 'novel'),
        sync_data=data.get('sync_data', ''),
        local_novel_id=data.get('local_novel_id'),
        last_synced=datetime.datetime.utcnow()
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201


@app.route('/api/v1/coze-projects/<int:id>', methods=['DELETE'])
def delete_coze_project(id):
    """删除扣子项目同步记录"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    project = CozeProject.query.filter_by(id=id, user_id=user_id).first()
    if not project:
        return jsonify({'message': '项目不存在'}), 404
    
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': '已删除'})


@app.route('/api/v1/coze-projects/<int:id>/sync', methods=['POST'])
def resync_coze_project(id):
    """重新同步扣子项目"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401
    
    project = CozeProject.query.filter_by(id=id, user_id=user_id).first()
    if not project:
        return jsonify({'message': '项目不存在'}), 404
    
    data = request.get_json() or {}
    if data.get('sync_data'):
        project.sync_data = data['sync_data']
    if data.get('title'):
        project.title = data['title']
    project.last_synced = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(project.to_dict())


# ==================== 课程 API ====================

@app.route('/api/v1/courses', methods=['GET'])
def get_courses():
    """获取课程列表（公开）"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    category = request.args.get('category', '')
    source = request.args.get('source', '')
    featured = request.args.get('featured', '')

    query = Course.query.filter_by(is_approved=True)
    if category:
        query = query.filter_by(category=category)
    if source:
        query = query.filter_by(source=source)
    if featured == '1':
        query = query.filter_by(is_featured=True)

    pagination = query.order_by(Course.is_featured.desc(), Course.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return jsonify({
        'items': [c.to_dict() for c in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })


@app.route('/api/v1/courses', methods=['POST'])
def create_course():
    """上传课程（需登录）"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401

    data = request.get_json()
    if not data or not data.get('title') or not data.get('url'):
        return jsonify({'message': '标题和链接不能为空'}), 400

    # 用户上传的课程默认待审核
    source = data.get('source', 'user_upload')
    is_approved = True if source == 'bilibili' else False  # 系统添加的直接通过

    course = Course(
        user_id=user_id,
        title=data['title'],
        description=data.get('description', ''),
        url=data['url'],
        cover=data.get('cover', ''),
        source=source,
        category=data.get('category', 'writing'),
        is_approved=is_approved
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route('/api/v1/courses/<int:id>/rate', methods=['POST'])
def rate_course(id):
    """为课程评分（需登录）"""
    user_id = require_auth()
    if not user_id:
        return jsonify({'message': '请先登录'}), 401

    course = Course.query.get(id)
    if not course:
        return jsonify({'message': '课程不存在'}), 404

    data = request.get_json()
    score = data.get('score', 0)
    if not (1 <= score <= 5):
        return jsonify({'message': '评分需为1-5分'}), 400

    # 更新或创建评分
    existing = CourseRating.query.filter_by(course_id=id, user_id=user_id).first()
    if existing:
        existing.score = score
        existing.review = data.get('review', '')
    else:
        rating = CourseRating(
            course_id=id, user_id=user_id, score=score, review=data.get('review', '')
        )
        db.session.add(rating)

    # 重算平均分
    ratings = CourseRating.query.filter_by(course_id=id).all()
    total = sum(r.score for r in ratings)
    course.rating_avg = total / len(ratings)
    course.rating_count = len(ratings)
    db.session.commit()

    return jsonify({'rating_avg': course.rating_avg, 'rating_count': course.rating_count})


@app.route('/api/v1/courses/<int:id>', methods=['GET'])
def get_course(id):
    """获取课程详情"""
    course = Course.query.get(id)
    if not course:
        return jsonify({'message': '课程不存在'}), 404
    course.views = (course.views or 0) + 1
    db.session.commit()
    return jsonify(course.to_dict())


# 健康检查端点（Render用）
@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=True)
