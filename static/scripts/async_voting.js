let voteUp = document.querySelector("#vote-up").addEventListener("click", send_vote_up);
let voteUp1 = document.getElementById("vote-up").addEventListener("click", send_vote_up);
let voteDown = document.querySelector("#vote-down").addEventListener("click", send_vote_down);
let voteDown1 = document.getElementById("vote-down").addEventListener("click", send_vote_down);


function makeRequest() {
    fetch('/question/{{ question.id }}/vote-up', "GET").then();
}

async function send_vote_up() {
    const response = await makeRequest;
}

async function send_vote_down() {

}