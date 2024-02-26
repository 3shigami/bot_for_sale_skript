const readline = require('readline');
const machineId = require('node-machine-id');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function getHWID() {
  return machineId.machineIdSync();
}

async function sendMessage(url, data, callback) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const responseJson = await response.json();
      callback(responseJson);
    } else {
      throw new Error(`Ошибка при отправке сообщения: ${response.status}`);
    }
  } catch (error) {
    console.error(error.message);
  }
}

function isInteger(tgId) {
  return Number.isInteger(tgId);
}

function askForMode() {
  rl.question('Выберите режим (K - ключ, T - TG ID): ', (mode) => {
    if (mode.trim().toLowerCase() === 'k') {
      askAndSendKey();
    } else if (mode.trim().toLowerCase() === 't') {
      askAndSendData();
    } else {
      console.log('Некорректный режим.');
      rl.close();
    }
  });
}

function askAndSendKey() {
  rl.question('Введите ключ: ', (key) => {
    const hwid = getHWID();
    const data = {
      from: 'user_as_key',
      key,
      hwid,
    };

    sendMessage('http://127.0.0.1:80/api/v1/messages', data, (response) => {
      if (response.status == false) {
        console.log(response.message)
        rl.close();
      } else if (response.status == true) {
        console.log(response.message)
        rl.close();
      }else {
        console.log('Ошибка при получении ответа от сервера:', response);
        rl.close();
      }
    });
  });
}

function askAndSendData() {
  rl.question('Введите TG ID: ', (tgId) => {
    tgId = parseInt(tgId);
    if (!isInteger(tgId)) {
      console.log('TG ID должен быть целым числом.');
      rl.close();
      return;
    }

    const hwid = getHWID();
    const path = require('path');
    const scriptName = path.basename(__filename);
    const data = {
      from: 'user_as_add_tg_id',
      telegramm_id: tgId,
      product: scriptName,
      hwid,
    };

    sendMessage('http://127.0.0.1:80/api/v1/messages', data, (response) => {
      if (response.status == false) {
        console.log(response.message)
      } else if (response.success && response.status === true) {
        console.log(response.message)
      }else {
        console.log('Ошибка при получении ответа от сервера:', response);
        rl.close();
      }
    });
  });
}

const hwid = getHWID();
const path = require('path');
const scriptName = path.basename(__filename);
sendMessage('http://192.168.31.186:80/api/v1/messages', {
  from: "user",
  product: scriptName,
  hwid,
}, (response) => {
  if (response.status == 'ask') {
    askForMode();
  } else if (response.status == true) {
    console.log('Доступ разрешен, дней до окончания подписки', response.days);
    rl.close();
  } else if (response.status == 'Block') {
    console.log('Приложение заблокировано.');
    rl.close();
  }
});

