export function Render(data, vueObj) {

  function freshVar(self) {
    self.inputNum = '';
    self.cardHeader = '<h2>回答：</h2><h4>注：若结果过多按 ctrl-f 搜索</h4>';
    self.numbers = [];
    self.numberRes = '';
    self.medicalName = '';
  }


  var self = vueObj;
  
  self.answer = self.noAnswerTip = '';
  self.InputErr = self.ReqErr = false;

  if (data.type == 'string') {
    freshVar(self);
    self.noAnswerTip = data.content;
    self.answerReady = false;
  }

  else if (data.type == 'object') {
    freshVar(self);
    if (data.state == 1) {
      self.state = 1;
      self.refillAnswer(data.content.names, 5);
      self.numbers = data.content.numbers;
      self.answerReady = true;
    }

    else if (data.state == 2) {
      self.state = 2;
      self.answer = '该药品含有该特性/物质。'
      self.numbers = data.content.numbers;
      self.answerReady = true;
    }

    else if (data.state == 3) {
      self.state = 3;
      self.refillAnswer(data.content.allObj, 9);
      self.numbers = data.content.numberObj;
      self.medicalName = data.medical;
      self.answerReady = true;
    }
  }

  self.firstDisplay = true;
}