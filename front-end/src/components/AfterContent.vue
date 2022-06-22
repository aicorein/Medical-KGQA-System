<template>
  <el-main>
    <el-row justify="center">
      <h1>药品知识图谱问答系统</h1>
    </el-row>

    <el-row justify="center" align="middle">
      <el-col :span="12">
        <el-input v-model="inputText" placeholder="输入你想知道的问题~"
          :formatter="(value) => `${value}`.replace(/[^\u4E00-\u9FA5]/g, '')"
          :parser="(value) => value.replace(/\$\s?|(,*)/g, '')" @keypress.enter="search(inputText)" />
      </el-col>
      <el-col :span="2">
        <el-button class="search-btn" type="primary" icon="Search" @click="search(inputText)">询问</el-button>
      </el-col>
    </el-row>

    <el-row justify="center">
      <div v-if="firstDisplay">

        <div class="card-box" v-if="state == 1">
          <el-card class="box-card first-card" v-if="!InputErr && !ReqErr && answerReady" shadow="hover">
            <template #header>
              <div class="card-header" v-html="cardHeader"></div>
            </template>
            <div class="answer" v-html="answer"></div>
          </el-card>
          <el-card class="box-card second-card" v-if="!InputErr && !ReqErr && answerReady" shadow="hover">
            <p>注：由于同名药品可能由不同厂家生产，结果可能存在差别。</p>
            <p>如需精准确认药品是否含有特性/物质，建议您输入国药准字查询：</p>
            <el-row justify="start" align="middle">
              <el-col :span="8">
                <el-input v-model="inputNum" placeholder="输入国药准字"
                  :formatter="(value) => `${value}`.replace(/[^A-Za-z0-9]+/g, '')"
                  :parser="(value) => value.replace(/\$\s?|(,*)/g, '').toUpperCase()"
                  @keypress.enter="verifyNumber()" />
              </el-col>
              <el-col :span="2">
                <el-button class="search-btn" type="primary" @click="verifyNumber()">查询</el-button>
              </el-col>
            </el-row>
            <p v-html="numberRes"></p>
          </el-card>
        </div>

        <div class="card-box" v-if="state == 2">
          <el-card class="box-card first-card" v-if="!InputErr && !ReqErr && answerReady" shadow="hover">
            <template #header>
              <div class="card-header" v-html="cardHeader"></div>
            </template>
            <div class="answer" v-html="answer"></div>
          </el-card>
          <el-card class="box-card second-card" v-if="!InputErr && !ReqErr && answerReady" shadow="hover">
            <p>注：由于同名药品可能由不同厂家生产，结果可能存在差别。</p>
            <p>如需精准确认药品是否含有特性/物质，建议您输入国药准字查询：</p>
            <el-row justify="start" align="middle">
              <el-col :span="8">
                <el-input v-model="inputNum" placeholder="输入国药准字"
                  :formatter="(value) => `${value}`.replace(/[^A-Za-z0-9]+/g, '')"
                  :parser="(value) => value.replace(/\$\s?|(,*)/g, '').toUpperCase()"
                  @keypress.enter="verifyNumber()" />
              </el-col>
              <el-col :span="2">
                <el-button class="search-btn" type="primary" @click="verifyNumber()">查询</el-button>
              </el-col>
            </el-row>
            <p v-html="numberRes"></p>
          </el-card>
        </div>

        <div class="card-box" v-if="state == 3">
          <el-card class="box-card first-card" v-if="!InputErr && !ReqErr && answerReady" shadow="hover">
            <template #header>
              <div class="card-header" v-html="cardHeader"></div>
            </template>
            <div class="answer" v-html="answer"></div>
          </el-card>
          <el-card class="box-card second-card" v-if="!InputErr && !ReqErr && answerReady" shadow="hover">
            <p>注：由于同名药品可能由不同厂家生产，结果可能存在差别。</p>
            <p>如需精准获得某药品的信息，输入国药准字以继续：</p>
            <el-row justify="start" align="middle">
              <el-col :span="8">
                <el-input v-model="inputNum" placeholder="输入国药准字"
                  :formatter="(value) => `${value}`.replace(/[^A-Za-z0-9]+/g, '')"
                  :parser="(value) => value.replace(/\$\s?|(,*)/g, '').toUpperCase()"
                  @keypress.enter="refreshAnswer()" />
              </el-col>
              <el-col :span="2">
                <el-button class="search-btn" type="primary" @click="refreshAnswer()">查询</el-button>
              </el-col>
            </el-row>
            <p v-html="numberRes"></p>
          </el-card>
        </div>

        <el-empty v-if="!answerReady && !InputErr && !ReqErr" :description="noAnswerTip" />
      </div>
    </el-row>


  </el-main>

  <el-backtop :right="100" :bottom="100" />

</template>

<script>
import $ from 'jQuery'
import { Render } from '../js/render.js'

export default {
  data() {
    return {
      inputText: '',
      inputNum: '',
      cardHeader: '<h2>回答：</h2>',
      answer: '',
      numbers: [],
      numberRes: '',
      noAnswerTip: '',

      state: 0,
      medicalName: '',
      answerReady: false,
      firstDisplay: false,
      InputErr: false,
      ReqErr: false,
    }
  },
  methods: {
    async search(question) {
      self.InputErr = self.ReqErr = self.answerReady = false;
      if (question == "") {
        ElMessage({
          message: '非法的输入！',
          grouping: true,
          type: 'error',
        })
        this.InputErr = true;
      }
      else {
        this.inputText = question;
        try {
          var data = await getResult(question);
          dataRender(data, this);
        }
        catch (e) {
          console.error(e);
          ElMessage({
            message: '从服务器获取内容失败，请刷新重试！',
            grouping: true,
            type: 'error',
          })
          this.ReqErr = true;
        }
      }
    },
    verifyNumber() {
      // console.log(this.numbers);
      if (this.numbers.indexOf(this.inputNum) >= 0) {
        this.numberRes = '结果：<span style="color: green">存在对应特性/物质</span>';
      }
      else {
        this.numberRes = '结果：<span style="color: red">不存在对应特性/物质</span>';
      }
    },
    refreshAnswer() {
      var index;
      var findFlag = false;
      for (var i = 0; i < this.numbers.length; i++) {
        if (this.inputNum == this.numbers[i].number) {
          index = i;
          findFlag = true;
        }
      }
      this.answer = '';
      if (findFlag) {
        this.cardHeader = `<h2>${this.medicalName}</h2><h3>国药准字：${this.numbers[index].number}</h3>`
        for (let i = 0; i < this.numbers[index].obj.length; i = i + 2) {
          if (i + 1 >= this.numbers[index].obj.length) this.answer += `<p>${this.numbers[index].obj[i]}</p>`;
          else this.answer += `<p>${this.numbers[index].obj[i]}、${this.numbers[index].obj[i + 1]}</p>`;
        }
        ElMessage({
          message: '已更新对应药品的信息',
          grouping: true,
          type: 'success',
        })
      }
      else {
        this.cardHeader = `<h2>${this.medicalName}</h2><h3>国药准字：${this.inputNum}</h3>`
        this.answer = '该药品不存在，请检查输入的国药准字！'
        ElMessage({
          message: '对应药品不存在',
          grouping: true,
          type: 'error',
        })
      }
    }
  }
}

// 限制每秒钟 1 个请求，同时上一请求未完成，则取消上一请求
setInterval(() => {
  window.xhrCount = 0;
}, 1000)

function getResult(question, xhrObj) {
  return new Promise((resolve, reject) => {
    if (window.xhrCount >= 1) reject('Too many request!');
    else {
      window.xhrCount++;
      if (window.xhrObj) window.xhrObj.abort();
      window.xhrObj = $.ajax({
        url: 'http://localhost/query',
        data: { query: question },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
          window.xhrObj = null;
          resolve(data);
        },
        timeout: 5000,
        error: function (xhr) {
          reject(`Error code: ${xhr.status}`);
        },
      })
    }
  })
}


function dataRender(data, vueObj) {
  Render(data, vueObj);
}
</script>

<style scoped>
[v-cloak] {
  display: none;
}

.answer :deep(p) {
  margin-bottom: 5px;
  padding-left: 40px;
}

.el-main {
  display: flex;
  min-height: calc(100vh - 60px);
  flex-direction: column;
  justify-content: center;
}

h1 {
  font-size: 2.2rem;
}

.card-box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.first-card {
  width: 500px;
  margin-bottom: 30px;
}

.second-card {
  width: 600px;
}

.second-card .el-row {
  margin: 5px 0;
}

.second-card .search-btn {
  width: 100%;
  height: 30px;
}

.second-card .el-row .el-col {
  height: 30px;
}

.el-card {
  flex: 1;
}

:deep(.el-card__header) {
  padding-top: 10px;
  padding-bottom: 10px;
}

:deep(.el-card__body) {
  padding-top: 10px;
  padding-bottom: 10px;
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
