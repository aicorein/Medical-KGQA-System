<template>
  <div>
    <el-main>
      <el-row justify="center">
        <h1>药品知识图谱问答系统</h1>
      </el-row>
      <el-row justify="center" align="middle">
        <el-col :span="12">
          <el-input v-model="inputText" placeholder="输入你想知道的问题~"
            :formatter="(value) => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')"
            :parser="(value) => value.replace(/\$\s?|(,*)/g, '')" 
            @keypress.enter="search()"/>
        </el-col>
        <el-col :span="2">
          <el-button class="search-btn" type="primary" icon="Search" @click="search()">询问</el-button>
        </el-col>
      </el-row>
      <el-row class="tip-row" justify="center">
        <p class="tip">输入问题，如：乌鸡白凤丸的药物成分有什么？</p>
      </el-row>
    </el-main>
  </div>
</template>

<script>
export default {
  emits: [
    'search'
  ],
  data() {
    return {
      inputText: '',
    }
  },
  methods: {
    search() {
      var self = this;
      this.$emit('search', self.inputText);
    }
  }
}
</script>


<style scoped>
.el-main {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

h1 {
  font-size: 2.3rem;
  text-align: center;
}

.el-main .tip-row {
  margin-top: 0;
}

.el-main {
  min-height: calc(100vh - 60px);
  padding: 0;
}

.el-row {
  margin: 2rem 0;
}

.el-col:first-child {
  height: 40px;
}

.el-input {
  height: 100%;
}

.el-input :deep(.el-input__wrapper) {
  font-size: 1rem;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.search-btn {
  height: 40px;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
</style>