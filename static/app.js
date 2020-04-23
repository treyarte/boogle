const form = document.querySelector('#boogle-form');
const highScore = document.querySelector('.high-score-value');
const score = document.querySelector('.score');
const scoreValue = document.querySelector('.score-value');

const playTime = document.querySelector('.play-time');
const wordList = document.querySelector('.word-list');
const messageBar = document.querySelector('.message-bar');
const messageContent = document.querySelector('#message');
const input = document.querySelector("input[type='text']");

//to prevent users from resending the same word
const savedWords = new Set();

let time = 60;
let intervalId;

countDown();
timer();

form.addEventListener('submit', handleWordSubmit);
async function handleWordSubmit(e) {
  e.preventDefault();
  userWord = input.value;
  const response = await axios.get('/check-word', {
    params: {
      'word-input': userWord,
    },
  });

  const { message } = response.data;

  checkWord(message, userWord);
  input.value = '';
}

function checkWord(message, userWord) {
  if (savedWords.has(userWord)) {
    createMessage(`${userWord} has already been used`, 'alert alert-warning');
    return;
  }
  if (message === 'ok') {
    createMessage(`${userWord} is a valid word`, 'alert alert-success');
    calculateScore(userWord);
    savedWords.add(userWord);
    appendWord(userWord);
  } else if (message === 'not-on-board') {
    createMessage(`${userWord} is not on the board`, 'alert alert-warning');
  } else if (message === 'not-word') {
    createMessage(`${userWord} is not a valid word`, 'alert alert-danger');
  }
}

function appendWord(userWord) {
  const li = document.createElement('li');
  li.innerText = userWord;
  wordList.append(li);
}

function createMessage(msg, type) {
  messageContent.innerText = msg;
  messageContent.className = type;
  messageBar.style.display = 'block';
}

function calculateScore(userWord) {
  let oldScore = parseInt(scoreValue.innerText);
  if (isNaN(oldScore)) oldScore = 0;

  scoreValue.innerText = userWord.length + oldScore;
}

function timer() {
  intervalId = setInterval(countDown, 1000);
}

function countDown() {
  if (time === 0) {
    playTime.innerText = time;
    clearInterval(intervalId);
    endGame();
  } else {
    playTime.innerText = time;

    time--;
  }
}

function endGame() {
  createMessage('Game Over', 'alert alert-primary');
  form.style.display = 'none';
  saveScore();
  updatePlays();
}

async function saveScore() {
  const newScore = parseInt(scoreValue.innerText);
  const res = await axios.post('/save-score', { score: newScore });
  const newHighScore = res.data['highscore'];

  highScore.innerText = newHighScore;
}

async function updatePlays() {
  const res = await axios.get('/plays');
  const plays = res.data['plays'];
  document.querySelector('.number-plays span').innerText = plays;
}
