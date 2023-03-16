onmessage = function (e) {
  console.log(self.postMessage);
  console.log("hi : ",e.data);
  if (e.type === 'getWorkerUrl') {      
    console.log("worker in");
    console.log('Worker URL:', e.data.url);
  } 
  else if (e.type === 'getToken'){
    console.log('Worker token:', e.data.token);
  }
  executed = true;
  console.log("return message");
  //postMessage('Hello main script!', "http://127.0.0.1/mark/Merge/");
  close();
  
  console.log("close");
};

