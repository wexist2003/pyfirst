from models import Post, LinkPost, ImagePost, TextPost, User

if __name__ == '__main__':
    # for post in Post.objects:
    #     print(post.title)
    #     print('=' * len(post.title))

    #     if isinstance(post, TextPost):
    #         print(post.content)

    #     if isinstance(post, LinkPost):
    #         print('Link: {}'.format(post.link_url))
    
    
    posts = Post.objects()
    # for post in posts:
    #     print(post.to_json())
    for post in posts:
        print(post.to_mongo().to_dict())
    for post in Post.objects(tags = 'mongodb'):
        print(post.title)    
        
    users = User.objects()
    for post in users:
        print(post.to_mongo().to_dict())   