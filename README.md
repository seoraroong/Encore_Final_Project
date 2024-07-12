# Encore_Final_Project
데이터엔지니어링 파이널 프로젝트 

#멘토님....................

새로운 에러가... 왔어요.

4. 데이터 베이스 연결 시, SQL 충돌 
5. djongo.exceptions.SQLDecodeError:

    raise SQLDecodeError(f'Unknown token: {tok}')
djongo.exceptions.SQLDecodeError:

        Keyword: Unknown token: TYPE
        Sub SQL: None
        FAILED SQL: ('ALTER TABLE "token_blacklist_blacklistedtoken" ALTER COLUMN "id" TYPE long',)
        Params: ([],)
        Version: 1.3.6

The above exception was the direct cause of the following exception:


1,2 번 둘 다 선택을 해도 계속 이 상태임.

5. 가장 큰 문제 코드 이해 못하고 있음.


# 아래 데이터 베이스 연결 시, SQL 충돌 
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'MyDiary',  # 사용할 MongoDB 데이터베이스 이름
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb+srv://Seora:youlove4154@mydiary.727yxhm.mongodb.net/MyDiary?retryWrites=true&w=majority',  # MongoDB 호스트 주소 (기본적으로는 localhost)
            'username': 'Subhin',
            'password': '1234'
        }
    }
}