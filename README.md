# 멋쟁이 사자처럼 at 한국교통대학교 공식 홈페이지

## ! 중요 보안 준수 사항
* 본 Repository는 비공개 상태로 유지된다는 전제 하에 설계되었으므로 신뢰하지 않는 장치에서 소스코드를 Clone 하면 안 된다.
* 만약 소스코드를 공개할 시 반드시 DB 파일 및 SECRET_KEY는 공개 대상에서 제외시키고, 이전 커밋 기록에서도 모두 삭제해야 하며, 기타 DB 쿼리문 및 세션/인증 관련 코드가 노출되면 안 된다.
* Commit 및 Push 시 DB 파일은 항상 제외시키며, SECRET_KEY 파일과 함께 비공개 저장소에 백업한다.
* 만약 SECRET_KEY가 노출되었다면, 빠른 시간 내에 Django Secret Key Generator를 이용해 새 키를 발급받아야 한다.
* 관리자 사이트 로그인은 반드시 TLS 통신을 통해 시도해야 한다.
