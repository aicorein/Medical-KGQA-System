<script setup>
import indexCss from './css/index.css'
import MyFooter from './components/MyFooter.vue'
import MainContent from './components/MainContent.vue'
</script>

<template>
  <div class="common-layout">
    <el-container direction="vertical">
      <main-content class="wrapper"></main-content>
      <my-footer></my-footer>
    </el-container>
  </div>
</template>

<style lang="css" scoped>
.wrapper {
  width: 1000px;
  margin: 0 auto;
  min-height: calc(100vh - 60px);
}
</style>
