export function Render(data, vueObj) {

  function freshVar(self) {
    self.inputNum = '';
    self.cardHeader = '<h2>回答：</h2>';
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
      for (let i = 0; i < data.content.names.length; i++) {
        self.answer += `<p>${data.content.names[i]}</p>`;
      }
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
      for (let i = 0; i < data.content.allObj.length; i=i+2) {
        if (i + 1 >= data.content.allObj.length) self.answer += `<p>${data.content.allObj[i]}</p>`;
        else self.answer += `<p>${data.content.allObj[i]}、${data.content.allObj[i+1]}</p>`;
      }
      self.numbers = data.content.numberObj;
      self.medicalName = data.medical;
      self.answerReady = true;
    }
  }

  self.firstDisplay = true;
}