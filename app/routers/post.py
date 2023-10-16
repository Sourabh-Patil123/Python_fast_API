from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from pydantic.main import BaseModel

router = APIRouter(prefix="/posts",
                   tags=['Posts'])


# @router.post("/createposts")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title:{payload['title']} content:{payload['content']}"}


# @router.post("/")
# def create_post_2(new_post: schemas.PostCreate):
#     print(new_post.title, new_post.content, new_post.rating, new_post.published)
#     print(new_post.dict())
#     return new_post


@router.post("/", response_model=schemas.Post)
def create_post_3(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict() post_dict['id'] = randrange(0, 100000) my_post.append(post_dict) cursor.execute(
    # f"INSERT INTO posts(title, content, published) VALUES({post.title}, {post.content}, {post.published})")
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # New_posts = cursor.fetchone()
    # conn.commit()
    print(post.dict())
    # print(current_user.email)
    # New_posts = models.Post(**post.dict())
    New_posts = models.Post(**post.dict())
    # New_posts = models.Post(title=post.title, content =post.content, published=post.published)
    db.add(New_posts)
    db.commit()
    db.refresh(New_posts)
    return New_posts


# @app.get("/post")
# def getdata():
#     return {"data": my_post}

# this get api is connected with database get th data form database
@router.get("/",)
def getdata(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# @router.get("/post/latest")
# def get_latest_post():
#     post = my_post[len(my_post) - 1]
#     return {"Details": post}


# @app.get("/sqlAlchemy")
# def test_post(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#
#     return {"data": post}


#
# @router.post("/")
# def getdata(id: int, response: Response, db: Session = Depends(get_db)):
#     # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
#     # post = cursor.fetchone()
#     # print(test_post)
#     # post = find_post(id) # it is old code with find post function
#     # print(post)
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with id {id} was not found"}
#     return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        # if deleted_post == None:
        # if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    # my_post.pop(index)
    post.delete(synchroniz_session=False)
    db.commit()
    return {"message": "This post was Successfully Deleted"}
    # return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s , content =%s, published = %s WHERE id = %s returning *  """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        # if update_post is None:
        # if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_post[index] = post_dict
    post_query.update(updated_post.dict())
    # post_query.update({'title':'this is my updated title','content':his is my updated content'}
    #                     ,synchroniz_session=False)
    db.commit()
    return post_query.first()
