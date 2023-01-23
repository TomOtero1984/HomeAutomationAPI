function power_click() {
  fetch('https://www.homeautomationapi.tk/api?api=desklamp&command=power', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  })
    .then(response => response.text())
    .then(text => console.log(text))
}

function hue_click() {
  fetch('https://www.homeautomationapi.tk/api?api=desklamp&command=hue', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  })
    .then(response => response.text())
    .then(text => console.log(text))
}

function brighter_click() {
  fetch('https://www.homeautomationapi.tk/api?api=desklamp&command=brighter', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  })
    .then(response => response.text())
    .then(text => console.log(text))
}

function dimmer_click() {
  fetch('https://www.homeautomationapi.tk/api?api=desklamp&command=dimmer', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  })
    .then(response => response.text())
    .then(text => console.log(text))
}