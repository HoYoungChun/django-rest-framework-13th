# CEOS 13기 백엔드 스터디
## REST API 서버 개발
### 인스타그램 클론

# 유의사항
* 본 레포지토리는 백엔드 스터디 2-3주차의 과제를 위한 레포입니다.
* 따라서 해당 레포를 fork 및 clone 후 local에서 본인의 깃헙 ID 브랜치로 작업한 후 커밋/푸시하고, PR 보낼 때도 `본인의 브랜치-> 본인의 브랜치`로 해야 합니다.

# 2주차 과제 (기한: 3/25 목요일까지)
### 모델 설명
사용자 : 게시글 = 1 : N<br>
게시글 : 사진,동영상 = 1 : N<br>
(좋아요) 사용자 : 게시글 = N : M<br>
(팔로우관계) 사용자 : 사용자 = N : M<br>
<br>
### ERD
![erd](https://user-images.githubusercontent.com/63651422/112450212-8112c080-8d97-11eb-867a-c34842a055c8.png)

### ORM 적용해보기
shell에서 작성한 코드와 그 결과를 보여주세요!<br><br>

User 객체 2개 생성
```python
python manage.py shell
>>> from api.models import *
>>> hy1 = User(nickname="hy1", email="hy@naver.com", phone_number="01011111111", password="1111", username="호영", description="나는호영1")
>>> hy1.save()
>>> hy2 = User(nickname="hy2", email="hy2@naver.com", phone_number="01022222222", password="2222", username="호영2", description="나는호영2")
>>> hy2.save()
>>> User.objects.all()
<QuerySet [<User: hy1>, <User: hy2>]>
```

Follow 객체 1개 생성
```python
>>> Follow.objects.create(following=hy1, followed=hy2)
<Follow: hy1 -> hy2>
```

Post 객체 1개 생성
```python
>>> p1 = Post(title="졸려", content="그냥잘까", author=hy1)
>>> p1.save()
>>> Post.objects.all()
<QuerySet [<Post: 졸려>]>
```

File 객체 2개 생성
```python
>>> File.objects.create(post=p1, file="프사.jpg")
<File: 졸려의 1번째 파일>
>>> File.objects.create(post=p1, file="프사sdf.jpg")
<File: 졸려의 2번째 파일>
>>> File.objects.all()
<QuerySet [<File: 졸려의 1번째 파일>, <File: 졸려의 2번째 파일>]>
```

Heart 객체 2개 생성
```python
>>> Heart.objects.create(post=p1, user=hy1)
<Heart: hy1 ♥ 졸려>
>>> Heart.objects.create(post=p1, user=hy2)
<Heart: hy2 ♥ 졸려>
>>> File.objects.all()
<QuerySet [<File: 졸려의 1번째 파일>, <File: 졸려의 2번째 파일>]>
```

Filter적용
```python
>>> User.objects.filter(nickname__contains='2')
<QuerySet [<User: hy2>]>
>>> Heart.objects.filter(user=hy1)
<QuerySet [<Heart: hy1 ♥ 졸려>]>
```

### 간단한 회고
과제 시 어려웠던 점이나 느낀 점, 좋았던 점 등을 간단히 적어주세요!<br>
->실제 프로젝트에서 ERD를 짤때 고민을 정말 많이해서 만들어야겠다는 생각을 했습니다.

<br>

## 3주차 과제 (기한: 4/1 목요일까지)
### 모델 선택 및 데이터 삽입
선택한 모델의 구조와 데이터 삽입 후의 결과화면을 보여주세요!
```python
#사용자
class User(models.Model):
    # 닉네임, 이메일, 전화번호로 로그인하기 때문에 Unique해야
    nickname = models.CharField(max_length=100, verbose_name="닉네임", unique=True)
    email = models.EmailField(max_length=255, verbose_name="이메일", unique=True)
    phone_number = models.CharField(max_length=100, verbose_name="전화번호", unique=True)

    password = models.CharField(max_length=150, verbose_name="비밀번호", unique=True)
    username = models.CharField(max_length=150, verbose_name="이름", unique=True)
    description = models.TextField(verbose_name="소개")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="가입일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="업데이트일자")

    def __str__(self):
        return self.nickname #표시할때 닉네임으로

#팔로잉 관계
class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_following", verbose_name="팔로우하는 사람")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_followed", verbose_name="팔로우된 사람")

    def __str__(self):
        return self.following.nickname + ' -> ' + self.followed.nickname
```
![image](https://user-images.githubusercontent.com/63651422/113284715-fdbc1680-9324-11eb-9646-76c0755409ad.png)
![image](https://user-images.githubusercontent.com/63651422/113284922-4b388380-9325-11eb-87a8-01808cc7fea8.png)

### 모든 list를 가져오는 API
API 요청한 URL과 결과 데이터를 코드로 보여주세요!
```python
#config/urls.py
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```
```python
#api/urls.py
from django.urls import path
from api import views

urlpatterns = [
    path('users', views.UserList.as_view()),
    path('posts', views.PostList.as_view()),
    path('files', views.FileList.as_view()),
    path('follows', views.FollowList.as_view()),
    path('hearts', views.HeartList.as_view()),
]
```
* User list 가져오기 (url 변경 전)
![image](https://user-images.githubusercontent.com/63651422/113285700-38727e80-9326-11eb-9d95-e859a947a2b7.png)

* Follow list 가져오기 (url 변경 전)
![image](https://user-images.githubusercontent.com/63651422/113285831-5e981e80-9326-11eb-8f69-3256e2f52d83.png)

### 새로운 데이터를 create하도록 요청하는 API
요청한 URL 및 Body 데이터의 내용과 create된 결과를 보여주세요!<br>

* User create (url 변경 전)
![image](https://user-images.githubusercontent.com/63651422/113286840-b1260a80-9327-11eb-90c5-ed1bb56fa6aa.png)

* Follow create (url 변경 전)
![image](https://user-images.githubusercontent.com/63651422/113287003-eaf71100-9327-11eb-9f48-5e10ea1566b9.png)

### 공부한 내용 정리
REST API에서 혼동을 주지 않기 위해 URI 경로의 마지막에는 슬래시(/)를 사용하지 않는다는 점을 알게 되었습니다. <br>그리고 related name을 지을 때 역참조를 생각해서 모델이름을 부여하는게 좋다는 점을 배웠습니다.

### 간단한 회고
처음에 FBV로 하다가, CBV로도 해보면서 이 부분에 대해 정확히 공부를 해야겠다고 생각했습니다. <br>빨리 프론트와 같이 협업하면서 REST API를 사용해보고 싶습니다.

## 4주차 과제 (기한: 4/8 목요일까지)
### 모든 list를 가져오는 API
* URL
```python
127.0.0.1:8000/api/follows
```
* 결과 데이터
```python
[
    {
        "id": 1,
        "following": 1,
        "followed": 2
    },
    {
        "id": 4,
        "following": 2,
        "followed": 1
    }
]
```

### 특정 데이터를 가져오는 API
* URL
```python
127.0.0.1:8000/api/follows/4
```
* 결과 데이터
```python
{
    "id": 4,
    "following": 2,
    "followed": 1
}
```

### 새로운 데이터를 생성하는 API
* URL
```python
127.0.0.1:8000/api/follows
```
* body 데이터의 내용
```python
{
    "following": 6,
    "followed": 1
}
```
* create된 결과<br>
![image](https://user-images.githubusercontent.com/63651422/113921579-252d4a80-9821-11eb-8d8c-c289dd984fe3.png)

### 특정 데이터를 업데이트하는 API
* URL
```python
127.0.0.1:8000/api/follows/1
```
* body 데이터의 내용
```python
{
    "following": 1,
    "followed": 6
}
```
* update된 결과<br>
![image](https://user-images.githubusercontent.com/63651422/113921197-a9cb9900-9820-11eb-9cc8-6cb777514f74.png)



### 특정 데이터를 삭제하는 API
* URL
```python
127.0.0.1:8000/api/follows/4
```
* delete된 결과<br>
![image](https://user-images.githubusercontent.com/63651422/113920347-9e2ba280-981f-11eb-97b3-af6594f98f65.png)

### 공부한 내용 정리
GET, POST, DELETE, PUT 방식에 대해서 알게되었습니다. 이외에도 다른 HTTP 메소드들에 대해서도 살펴보았습니다.

### 간단한 회고
url을 여러가지로 만들지 않고, 하나의 url에서 여러가지 기능들을 처리하는게 정말 편리했습니다. rest api에 대해 더 깊게 공부해야겠다는 생각을 했습니다.

## 5주차 과제 (기한: 5/13 목요일까지)
### 1. Viewset으로 리팩토링하기
```python
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.all()
```

### 2. filter 기능 구현하기
```python
class UserFilter(FilterSet):
    nickname = filters.CharFilter(field_name='nickname', lookup_expr="icontains")
    is_hy1 = filters.BooleanFilter(method='filter_is_hy1')

    class Meta:
        model = User
        fields = ['nickname']

    def filter_is_hy1(self, queryset, name, value):
        filtered_queryset = queryset.filter(nickname__contains="1")
        filtered_queryset2 = queryset.filter(~Q(nickname__contains="1"))
        if value == True:
            return filtered_queryset
        else:
            return filtered_queryset2
        
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
```
![image](https://user-images.githubusercontent.com/63651422/118385768-eb840680-b64c-11eb-80ad-fb29ecc0b7de.png)
```python
http://127.0.0.1:8000/api/user/?is_hy1=false
```
```python
[
    {
        "id": 2,
        "_following": [],
        "_followed": [],
        "_user": [
            {
                "id": 2,
                "post": 1,
                "user": 2
            }
        ],
        "_author": [],
        "nickname": "hy2",
        "email": "hy2@naver.com",
        "phone_number": "01022222222",
        "password": "2222",
        "username": "호영2",
        "description": "나는호영2",
        "created_at": "2021-04-01T02:33:34.230805+09:00",
        "updated_at": "2021-04-01T02:33:34.230805+09:00"
    },
    {
        "id": 6,
        "_following": [
            {
                "id": 7,
                "following": 6,
                "followed": 1
            }
        ],
        "_followed": [
            {
                "id": 1,
                "following": 1,
                "followed": 6
            }
        ],
        "_user": [],
        "_author": [],
        "nickname": "hy5",
        "email": "hy5@naver.com",
        "phone_number": "01055555555",
        "password": "5555",
        "username": "hy5",
        "description": "hy5",
        "created_at": "2021-04-08T03:25:17.209385+09:00",
        "updated_at": "2021-04-08T03:25:17.209385+09:00"
    }
]

```

```python
http://127.0.0.1:8000/api/user/?nickname=2&is_hy1=fasle

```
![image](https://user-images.githubusercontent.com/63651422/118385802-3140cf00-b64d-11eb-96cd-71af6d2da6cc.png)


### 과제를 하면서 알게 된 내용 & 회고
"http://127.0.0.1:8000/api/user/?is_hy1=false"와 같이 접속했을 때 def filter_is_hy1(self, queryset, name, value):에서 parameter로 name=is_hy1, value=false가 들어갔습니다. 이를 통해 좀더 다채로운 처리가 가능할거 같고, lookup_expr의 다양한 조건을 알아두면 프로젝트할 때 도움이 많이 될 것 같습니다.

from django.db.models import Q를 통해 Q객체를 써서 복잡한 질의문을 처리할 수 있어서, 이를 통해 원하는 질의문을 편하게 작성할 수 있었습니다.


## Sum-up
### 모델링
```
ERD를 짤 때, 1:1, 1:N, N:M 관계를 깊이 생각해서 정확히 파악해야 하며,
N:M의 경우 django에서 ManyToManyField를 사용해도 되지만, N:1,1:M으로 중계모델을 만들어줄 수 있습니다.
또, 이때 ERD를 짜면서, 변수명을 정말 신중하게 정해야 합니다.
```

### Django ORM
```python
모델명.objects.all() #모든 객체 조회
모델명.object.create(필드=필드값, ...) #해당 모델 객체 생성
모델명.object.get(필드=필드값) #하나의 instance반환(없으면 에러발생)
모델명.object.get_object_or_404(필드=필드값) #없을때 404예외처리
모델명.object.filter(필드=필드값) #조건 만족하는 객체 필터링
```

### Serializer
```python
django rest framework는 클라이언트의 요청에 대해 JSON 문자열을 돌려줌으로써 소통하는데,
이를 쉽게 가능하도록 해주는 것이 Serializer입니다.
Serializer와 ModelSerializer가 있고, ModelSerializer를 상속했을 때, 더 간단해집니다.

#serializers.py
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
```

### DRF API View
```python
FBV(함수 기반 뷰) vs CBV(클래스 기반 뷰)
FBV: @api_view 데코레이터를 사용합니다.
CBV: APIView를 상속합니다.

@api_view(['GET'])
def group_list(request):
	if request.method == 'GET':
		return Response({"message":"group list"})

class GroupList(APIView):
	def get(self, request, format=None):
		pass

	def post(self, request, format=None):
		pass
```

### ViewSet
```python
APIView ---패턴화---> Generic Views ---구조화---> Viewsets
ModelViewSet은 기본적으로 Retrieve, List, Create, Destroy, Update의 뷰를 제공합니다.

from rest_framework import viewsets

class ModelNameViewSet(viewsets.ModelViewSet):
	serializer_class = ModelNameSerializer
	queryset = ModelName.objects.all()
```

### Filtering
```
filtering은, 어떤 query set에 대하여 원하는 옵션대로 필터를 걸어,
해당 조건을 만족하는 특정 쿼리셋을 만들어내는 작업입니다.

drf의 viewset에서 이러한 filtering을 쉽게 사용할 수 있도록 filterset이라는 속성을 제공합니다.
```

### 배포

### 회고
django를 해봤지만, drf를 사용해본 적이 없었는데, 이번 백엔드 스터디를 통해 RESTful api에 대해 이해할 수 있게 되었습니다.<br>
이후에 drf를 조금 더 깊게 공부한 뒤에 다른 framework들도 경험해보고 싶어졌고,<br>
특히 Spring framework를 공부하고 싶어서, 같이 공부하실 분 있으면 스터디하고 싶어요ㅎㅎ<br>
또, 언제든 뜻이 맞다면 사이드프로젝트를 백엔드분들과 같이 진행해보고 싶습니다~!
