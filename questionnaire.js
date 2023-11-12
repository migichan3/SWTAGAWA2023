const SELECT_ANSWER = ["はい", "いいえ"];

const QUESTIONS = [
    "もの忘れがひどい、または集中力に欠ける",
    "甘いものが我慢できない",
    "食後1時間ぐらいたつと、疲れや眠気を感じる",
    "食事を抜くとイライラする",
    "急に立つと、めまいがする",
      "食生活は肉や魚をあまり食べず、野菜中心",
      "ダイエットをしているのにやせない",
      "同じことを何度も話していると指摘される",
      "下半身の筋肉が衰えてきた",
      "つまらないことでクヨクヨしてしまう",
      "インスタント食品や冷凍食品をよく食べる",
      "イラついたり落ち込んだり感情の起伏が激しい",
      "首や背中の筋肉が痛む",
      "よくまぶたがピクピク痙攣する",
      "運動や睡眠中に足がつりやすい",
      "スイーツや清涼飲料水をよくとる",
      "下痢や便秘をしやすい",
      "ニキビや湿疹ができやすい",
      "おなかが張ってガスがたまりやすい",
      "お酒、コーヒーや栄養ドリンクをよく飲む",
];

// ローディングメッセージ点滅用のタイマーID
let loadingInterval;

const form = document.getElementById('questionForm');
const questionsDiv = document.getElementById('questions');
console.log(form);
console.log(questionsDiv);

if (questionsDiv) {
    QUESTIONS.forEach((question, index) => {
        const questionId = `q${index + 1}`;

        const questionDiv = document.createElement('div');
        const questionDivId = `questionSpace`; // id名を作成

        questionDiv.id = questionDivId; // id属性に値を設定
        questionDiv.innerHTML = `
            <label for="${questionId}" class="question">${question}</label>
            <div class="radio-group">
                <input type="radio" id="${questionId}Yes" name="${question}" value="はい" onclick="answerQuestion(${index}, true)">
                <label for="${questionId}Yes">はい</label>
                <input type="radio" id="${questionId}No" name="${question}" value="はい" onclick="answerQuestion(${index}, false)">
                <label for="${questionId}No">いいえ</label>
            </div>
        `;

        questionsDiv.appendChild(questionDiv);
    });
} else {
    console.error('QuestionsDiv not found.');
}

let answers = new Array(questions.length).fill(null);

function answerQuestion(index, answer) {
    answers[index] = answer;
}

function reloadPage() {
    location.reload();
}

// ローディングメッセージを0.5秒ごとに点滅させる関数
function startLoadingAnimation() {
    const loadingMessage = document.getElementById('loading');
    let count = 0;
    loadingInterval = setInterval(() => {
        loadingMessage.style.display = (loadingMessage.style.display === 'none') ? 'block' : 'none';
        count++;
        if (count === 50) {
            // 5回繰り返したら点滅停止
            stopLoadingAnimation();
        }
    }, 500);
}

// ローディングメッセージの点滅を停止する関数
function stopLoadingAnimation() {
    clearInterval(loadingInterval);
    const loadingMessage = document.getElementById('loading');
    loadingMessage.style.display = 'none';
}

async function submitForm() {
    const form = document.getElementById('questionForm');
    const formData = new FormData(form);

    const answers = {};
    formData.forEach((value, key) => {
        answers[key] = value;
    });

    // 質問内容を消す
    form.style.display = 'none';

    // ローディングメッセージ表示と点滅開始
    const loadingMessage = document.getElementById('loading');
    loadingMessage.style.display = 'block';
    startLoadingAnimation();

    try {
        const url = 'http://127.0.0.1:8000/submit';
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors',
            body: JSON.stringify(answers),
        });

        if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
        }

        // ローディングメッセージ非表示
        loadingMessage.style.display = 'none';
        // 点滅停止
        stopLoadingAnimation();

        const data = await res.json();

        result1 = data[0];
        result2 = data[1];

        // 結果を表示
        const resultRecommendNabeDiv = document.getElementById('resultRecommendNabe');
        const resultDivRecommendFoodDiv = document.getElementById('resultRecommendFood');
        const buttonToBuyDiv = document.getElementById('buttonToBuy');
        const buttonToStartDiv = document.getElementById('buttonToStart');
        resultRecommendNabeDiv.innerHTML = `<div id="resultRecommendNabe">あなたへのおすすめの鍋<div id="resultRecommendNabeName">${result1}</div>\ 
                                            <div id="resultRecommendNabeNameImg"><img src="img/${result1}.jpg" alt="${result1}"></div></div> `;
        resultDivRecommendFoodDiv.innerHTML = `<div id="resultDivRecommendFood">あなたへのおすすめ食材<ul id="resultDivRecommendFoodName">${result2.map(item => `<li>${item}</li>`).join('')}</ul></div>`;
        // 遷移先決める
        buttonToBuyDiv.innerHTML = `<button id="buttonToBuyBox" type="button" onclick="">購入する</button>`
        buttonToStartDiv.innerHTML = `<button type="button" onclick="reloadPage()">もう一度お勧めしてもう</button>`

    } catch (error) {
        // エラーメッセージ表示
        const resultDiv = document.getElementById('result');
        resultDiv.innerText = `Error: ${error.message}`;
        console.error('Error:', error);

        // ローディングメッセージ非表示
        loadingMessage.style.display = 'none';
        // 点滅停止
        stopLoadingAnimation();
    }
}

