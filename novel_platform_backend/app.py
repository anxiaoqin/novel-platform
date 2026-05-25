"""
网文创作平台后端 - Flask版本（生产部署）
"""
from flask import Flask, jsonify, request
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

# CORS - 支持前端域名
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

db = SQLAlchemy(app)

# ==================== 数据库模型 ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
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
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'order': self.order,
            'novel_id': self.novel_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class World(db.Model):
    __tablename__ = 'worlds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    world_id = db.Column(db.Integer, db.ForeignKey('worlds.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'world_id': self.world_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ==================== 工具函数 ====================

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
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
        except:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user)
    return decorated

# ==================== 认证接口 ====================

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
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
    novels = Novel.query.filter_by(user_id=current_user.id).all()
    return jsonify([n.to_dict() for n in novels])

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
    db.session.delete(novel)
    db.session.commit()
    return jsonify({'message': 'Novel deleted'})

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
    
    chapter = Chapter(
        title=data.get('title', '新章节'),
        content=data.get('content', ''),
        order=order,
        novel_id=novel_id
    )
    db.session.add(chapter)
    db.session.commit()
    return jsonify(chapter.to_dict()), 201

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
        chapter.content = data['content']
    if 'order' in data:
        chapter.order = data['order']
    
    db.session.commit()
    return jsonify(chapter.to_dict())

# ==================== 世界观接口 ====================

@app.route('/api/v1/worlds', methods=['GET'])
@token_required
def get_worlds(current_user):
    worlds = World.query.filter_by(user_id=current_user.id).all()
    return jsonify([w.to_dict() for w in worlds])

@app.route('/api/v1/worlds', methods=['POST'])
@token_required
def create_world(current_user):
    data = request.get_json()
    world = World(
        name=data.get('name', '新世界'),
        description=data.get('description', ''),
        user_id=current_user.id
    )
    db.session.add(world)
    db.session.commit()
    return jsonify(world.to_dict()), 201

@app.route('/api/v1/worlds/<int:id>', methods=['DELETE'])
@token_required
def delete_world(current_user, id):
    world = World.query.filter_by(id=id, user_id=current_user.id).first()
    if not world:
        return jsonify({'error': 'World not found'}), 404
    db.session.delete(world)
    db.session.commit()
    return jsonify({'message': 'World deleted'})

# ==================== 角色接口 ====================

@app.route('/api/v1/characters', methods=['GET'])
@token_required
def get_characters(current_user):
    characters = Character.query.filter_by(user_id=current_user.id).all()
    return jsonify([c.to_dict() for c in characters])

@app.route('/api/v1/characters', methods=['POST'])
@token_required
def create_character(current_user):
    data = request.get_json()
    character = Character(
        name=data.get('name', '新角色'),
        description=data.get('description', ''),
        world_id=data.get('world_id'),
        user_id=current_user.id
    )
    db.session.add(character)
    db.session.commit()
    return jsonify(character.to_dict()), 201

@app.route('/api/v1/characters/<int:id>', methods=['DELETE'])
@token_required
def delete_character(current_user, id):
    character = Character.query.filter_by(id=id, user_id=current_user.id).first()
    if not character:
        return jsonify({'error': 'Character not found'}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Character deleted'})

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
<p>• <strong>关键信息</strong>：{prompt[:50]}...</p>
<p><strong>总结：</strong>故事以紧张的氛围开篇，通过细腻的描写展现了主角内心的挣扎与坚定。伏笔的埋设暗示着后续将有更大的冲突和发展。</p>"""

@app.route('/api/v1/ai/generate', methods=['POST'])
@token_required
def ai_generate(current_user):
    data = request.get_json()
    mode = data.get('mode', 'continue')
    prompt = data.get('prompt', '')
    style = data.get('style', 'humor')
    
    # 生成内容（实际项目中这里会调用AI API）
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

# ==================== 根路径 ====================

@app.route('/')
def index():
    return jsonify({
        'message': '网文创作平台API',
        'version': '0.1.0'
    })

# ==================== 初始化 ====================

with app.app_context():
    db.create_all()

# 健康检查端点（Render用）
@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=True)
