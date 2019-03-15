# 멋쟁이 사자처럼 at 한국교통대학교 공식 홈페이지

## 중요 보안 준수 사항
* 커밋은 반드시 DB 파일 및 SECRET_KEY를 제외시켜야 하며, 이전 커밋 기록에서도 모두 삭제해야 한다.
* 기타 DB 쿼리문 및 세션/인증 관련 코드가 노출되면 안 된다.
* 만약 SECRET_KEY가 노출되었다면, 빠른 시간 내에 Django Secret Key Generator를 이용해 새 키를 발급받아야 한다.
* 로그인은 반드시 TLS 통신을 통해 시도해야 한다.


## 외부 라이브러리 사용 명시
* [Bootstrap Theme](https://bootstrapmade.com/) - Free Version
* [objectivehtml/FlipClock](https://github.com/objectivehtml/FlipClock) - MIT License
* [cobrateam/django-htmlmin](https://github.com/cobrateam/django-htmlmin) - [BSD-2-Clause](https://opensource.org/licenses/bsd-license.php)
