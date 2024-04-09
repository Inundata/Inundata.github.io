---
title:  "PyInstaller를 이용하여 *.exe파일을 만들기"
show_date: true
comments: true
layout: single
categories:
  - etc
tags:
toc: true
toc_sticky: false
published: true
---

파이썬 파일을 *.exe 파일로 만들어서 배포하는 경우에 다음의 패키지를 사용하여야 한다. <br/>
```python
pyinstaller
```

이를 이용하면 손쉽게 *.exe 파일을 만들 수 있는데, 헷갈리는 점이 몇 가지가 있어 기록용으로 작성한다. <br/>

## 1. *.exe파일 만들기 기초
당연하지만, *.exe파일을 만들고 싶은 *.py가 있는 경로로 들어가야 한다. <br/>

## 2. *.exe 파일로 만드는 법

```
>>> conda activate (pyinstaller가 실행된 VirtualEnv)
>>> pyinstall --onefile (파일명).py
```

이렇게 하면 *.py파일이 있는 내부에 `build`, `dist`폴더가 생기고, `dist`폴더에 *.exe파일이 생긴다. <br>

## 3. 오류발생

하지만 높은 확률로 에러가 발생할 것인데, 여기서는 그 오류를 정리한다. 그리고 새로운 오류가 생길 경우 업데이트 하겠다. <br/>

우선 내가 *.exe파일을 만들었을 때 사용한 디렉토리는 다음과 같다. <br/>

```
폴더1
|__ MyFile1.py
|
폴더2
|__ MyFile2
```
위의 내용을 설명하면, `폴더1`에 있는 `MyFile1.py`의 프로그램을 *.exe로 만들고 싶은 상황이고, `폴더2`에 있는 `MyFile2.py`은 `MyFile1.py`에 module처럼 사용되고 있는 상황이다. <br/>

### 오류1) module not founded error

해당 오류는 custom module을 찾지 못하겠다는 것이 아니라, pip 혹은 conda를 통해서 설치한 package를 못찾겠다는 에러인데, 나 같은 경우에는 `sklearn`을 못찾는다는 에러가 나왔다. <br/>

이 경우 다음과 같이 수정하면 문제가 해결된다. <br/>

```
>>> pyinstall --onefile --hidden-import sklearn MyFile1.py
```

### 오류2) custom module이 import되지 않는 문제

해당 오류는 `오류1`과 다르게, 내가 만든 모듈이 *.exe파일에 말려들어가지 않는 문제이다. <br/>

이 경우 디렉토리를 다음과 같이 수정을 해줘야 한다. <br/>
```
폴더1
|__ __init__.py # 새로 생성
|__ MyFile1.py
|
폴더2
|__ MyFile2
```

__init__.py은 해당 폴더가 package임을 선언해주는 파일이고, __init__.py은 내용이 아무것도 없어도 무관하다. <br/>
근데 의아한건...폴더2에 만들어야할 것 같은데, 폴더1에 만들어야 된다는 것이다. <br/>

여하튼 돌아가긴 돌아가니까 됐다. <br/>
그리고 *.exe파일을 만드는 것은 위와 동일하게 하면 된다. 하지만, 같은 경로에 있지 않아 못찾는 문제가 발생할 수 있으므로 2가지 버전 모두 기록하겠다.

```
pyinstaller --onefile --hidden-import sklearn MyFile1.py # 아무 문제 없는 경우
```

```
pyinstaller --onefile --hidden-import -p ../폴더2 MyFile1.py # 상대경로로 폴더 2추가
```

이렇게 하면 대부분 문제가 해결될 것이다.
