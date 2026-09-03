from fastapi import FastAPI , Request , status , HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate , PostResponse


app = FastAPI(title="Devlog-Blog")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]



@app.get("/", include_in_schema=False , name="home")
@app.get("/posts",  include_in_schema=False , name="posts")
def home(request: Request):
    return templates.TemplateResponse(request,"home.html",{"posts": posts,"title":"home"})

  

@app.get("/posts/{post_id}",include_in_schema=False)
def post_page(request: Request,post_id : int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(request,"post.html",{"post": post,"title":title})
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not Found !!"
    )


@app.get("/api/posts",response_model=list[PostResponse])
def get_posts():
    return posts

@app.post("/api/posts",response_model=PostResponse)
def create_post(post:PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if post else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "April 23, 2025",
    }
    posts.append(new_post)
    return new_post

@app.get("/api/posts/{post_id}",response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not Found !!") 


# this handles the route error - if user goes to route which is not created !
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request , expection: StarletteHTTPException):
    message = (
        expection.detail
        if expection.detail
        else "An error occurred !! Plz Check your request and Try Again!!"
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=expection.status_code,content={"detail":message})

    return templates.TemplateResponse(request,"error.html",{"status_code":expection.status_code,"title": expection.status_code,"message":message},status_code=expection.status_code)


# this handles the validation error - if user enters a string instead of integer
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request , exception:RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,content={"detail":exception.errors()})

    return templates.TemplateResponse(request,"error.html",{"status_code":status.HTTP_422_UNPROCESSABLE_CONTENT,"title": status.HTTP_422_UNPROCESSABLE_CONTENT,"message":"Invalid Request !!"},status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)