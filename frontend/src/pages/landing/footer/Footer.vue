<template>
  <div class="footer">
    <div class="row">
      <div class="flex md3">
        <div class="d-flex align--end">
          <img src="@/../public/img/landing-page/woori-ai-logo/child-boy.png" alt="logo" class="footer-logo">
          <img src="@/../public/img/landing-page/woori-ai-logo/child-girl.png" alt="logo" class="footer-logo">
          <p class="ml-3 footer-title">우리A.I</p>
        </div>
      </div>
      <div class="flex md5">
        <p class="d-flex justify--start mb-2" style="font-size:1.5rem; font-weight:bold;">Contributors</p>
        <div class="d-flex justify--space-between">
          <div class="d-flex align--center">
            <p class="github-name">김영기</p>
            <a href="http://github.com/" target="_blank"><img src="@/../public/img/landing-page/GithubIcon.png" alt="github" class="github-icon"></a>
          </div>
          <div class="d-flex align--center">
            <p class="github-name">김창민</p>
            <a href="http://github.com/sky6min" target="_blank"><img src="@/../public/img/landing-page/GithubIcon.png" alt="github" class="github-icon"></a>
          </div>
          <div class="d-flex align--center">
            <p class="github-name">반형동</p>
            <a href="http://github.com/bandong92" target="_blank"><img src="@/../public/img/landing-page/GithubIcon.png" alt="github" class="github-icon"></a>
          </div>
        </div>
        <div class="d-flex justify--space-between mt-3">
          <div class="d-flex align--center">
            <p class="github-name">손한기</p>
            <a href="http://github.com/onegi95" target="_blank"><img src="@/../public/img/landing-page/GithubIcon.png" alt="github" class="github-icon"></a>
          </div>
          <div class="d-flex align--center">
            <p class="github-name">이우철</p>
            <a href="http://github.com/dncjf1969" target="_blank"><img src="@/../public/img/landing-page/GithubIcon.png" alt="github" class="github-icon"></a>
          </div>
          <div class="d-flex align--center">
            <p class="github-name">이정원</p>
            <a href="http://github.com/sorrow4468" target="_blank"><img src="@/../public/img/landing-page/GithubIcon.png" alt="github" class="github-icon"></a>
          </div>
        </div>
      </div>
      <div class="flex md4">
        <p class="d-flex justify--center mb-2 align--center" style="font-size:1.25rem; font-weight:bold;">Team 스물다섯 서른하나</p>
        <!-- <img src="@/../public/img/landing-page/DNBBD.png" alt="DNBBD" class="dnbbd"> -->
      </div>
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="scss">

.footer {
  padding-bottom: 2rem;
}

.footer-logo {
  max-width: 70px;
  max-height: 70px;
}

.footer-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #212121;
  text-shadow: 1px 1px 1px gray;
}

.github-icon {
  max-width: 25px;
  margin-left: 0.5rem;
}

.github-name {
  font-weight: bold;
  font-size: 1rem;
}

.dnbbd {
  max-width: 250px;
  border-radius: 1rem;
  box-shadow: 5px 5px 5px #d2d2d2;
}

</style>
