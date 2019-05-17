from flask import request, g, Blueprint, json, Response
from ..models.blog import Blog, BlogSchema
from ..models.blog_like import BlogLike, BlogLikeSchema
from ..shared.res import custom_response
from ..shared.authentication import Authentication
from ..models.user import UserSchema

blogs_api = Blueprint('blogs_api', __name__)
blog_schema = BlogSchema()
blog_like_schema = BlogLikeSchema()
user_schema = UserSchema()

@blogs_api.route('/', methods=['POST'])
@Authentication.auth_required
@Authentication.info_required
def create():
    req_data = req.get_json()
    req_data['user_id'] = g.user.id
    data, error = blog_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    post = Blog(data)
    post.save()
    return custom_response(blogpost_schema.dump(post).data, 200)

@blogs_api.route('/', methods=['GET'])
@Authentication.auth_required
@Authentication.info_required
def get_all():
    posts = Blog.get_all_blogs()
    print(posts)
    data = blog_schema.dump(posts, many=True).data
    return custom_response(data, 200)

@blogs_api.route('/<int:blog_id>', methods=['GET'])
@Authentication.auth_required
@Authentication.info_required
def get_one(blog_id):
    post = Blog.get_one_blog(blog_id)
    if not post:
        return custom_response({'error': 'post not found'}, status=404)
    data = blog_schema.dump(post).data
    return custom_response(data, 200)

@blogs_api.route('/by-user/<int:user_id>', methods=['GET'])
@Authentication.auth_required
@Authentication.info_required
def get_posts_by_user(user_id):
    posts = Blog.get_blogs_by_user_id(user_id)
    data = blog_schema.dump(posts, many=True).data
    return custom_response(data, 200)

@blogs_api.route('<int:blog_id>/like', methods=['POST'])
@Authentication.auth_required
@Authentication.info_required
def like_post(blog_id):
    user_id = g.user.id
    is_liked = BlogLike.check_is_liked(user_id, blog_id)
    if is_liked:
        return custom_response({'error': 'You has been liked this post'}, 400)
    data, error = blog_like_schema.load({'user_id': user_id, 'blog_id': blog_id})
    if error:
        return custom_response(error, 400)
    blog_like = BlogLike(data)
    blog_like.save()
    return custom_response({'success': 'You has been liked this post'}, 200)

@blogs_api.route('<int:blog_id>/likes', methods=['GET'])
@Authentication.auth_required
@Authentication.info_required
def likes(blog_id):
    likes = BlogLike.get_users_like(blog_id)
    users = user_schema.dump(likes, many=True).data
    return custom_response({'likes': users}, 200)
