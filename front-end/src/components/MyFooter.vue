<template>
  <el-footer class="footer">
    <el-container class="page-info" direction="vertical">
      <el-row>
        <p class="author">
          Pages built
          <el-icon><tools /></el-icon>
          by
          <el-link href="https://glowmem.com" type="primary" title="去往开发者的个人网站！">MelodyEcho</el-link>
        </p>
      </el-row>
      <el-row>
        <p class="copyright">
          ©<span id="year">2022</span>&nbsp;
          <span class="text-primary" style="color: var(--el-color-primary);">BLCU 快放暑假 开发组</span>
          &nbsp;All rights reserved.
        </p>
      </el-row>
    </el-container>
  </el-footer>
</template>

<script>

</script>

<style scoped>
.el-footer {
  padding: 0;
  height: 60px;
}

.page-info {
  text-align: center;
  background-color: #ecf5ff;
  border-top: 1px solid var(--el-border-color);
  height: 100%;
  text-align: center;
}

.el-row {
  justify-content: center;
  margin-top: 0.25rem;
}

.el-row:last-child {
  margin-bottom: 0.25rem;
}

.footer {
  font-size: 1rem !important;
}

.footer p {
  height: 1.5rem;
}

.author .el-icon {
  color: #2dcbfa;
  transform: translateY(2px);
}

.page-info .el-link {
  font-size: 1rem;
  text-decoration: none;
  transition: color .2s ease-out, border .2s ease-out, opacity .2s ease-out;
  text-decoration: none;
}

.page-info .author a:hover {
  color: blueviolet !important;
}
</style>