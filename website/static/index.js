currentlyPlaying = false;
timerDuration = 5 * 1000;  // 5s
document.getElementById("timer").value = timerDuration;
document.getElementById("timer").max = timerDuration;


async function runTimerWithArgs(timer, startTime) {
    if(currentlyPlaying) {
        currentTime = (new Date()).getTime();
        elapsedTime = currentTime - startTime;
        if(elapsedTime >= timerDuration) {
            currentlyPlaying = false;
            timer.value = 0
            buttonClicked(null);
        }
        timer.value = timerDuration - elapsedTime;
        setTimeout(runTimerWithArgs, 10, timer, startTime);
    }
}


async function runTimer() {
    startTime = (new Date()).getTime();
    timer = document.getElementById("timer");
    runTimerWithArgs(timer, startTime);
}


async function getNewAnime() {
    // Get data
    site = await fetch("/api/random");
    animeData = await site.json();
    console.log(animeData);

    // Set names
    document.getElementById("anime-data").style.display = "none";
    document.getElementById("name").innerHTML = animeData.name;
    document.getElementById("anime").innerHTML = animeData.anime;

    // Set image
    image = document.getElementById("image");
    image.src = `data:image/png;base64,${animeData.image}`;

    // Show buttons
    document.getElementById("game-buttons").style.display = "block";
    document.getElementById("meta-buttons").style.display = "none";
    document.getElementById("content").style.display = "block";

    // Start timer
    currentlyPlaying = true;
    runTimer();
}


async function buttonClicked(isAIButton) {
    // Stop the timer
    currentlyPlaying = false;

    // Hide the game buttons
    document.getElementById("game-buttons").style.display = "none";
    document.getElementById("meta-buttons").style.display = "block";

    // See if they're right
    imageWasAI = document.getElementById("name").innerHTML == "";
    if(isAIButton === null) {
        document.getElementById("result").innerHTML = "Time ran out :c";
    }
    else if((imageWasAI && isAIButton) || (!imageWasAI && !isAIButton)) {
        document.getElementById("result").innerHTML = "Correct!";
        await updateScore(true);
    }
    else {
        document.getElementById("result").innerHTML = "Wrong!";
        await updateScore(false);
    }
    if(imageWasAI) {
        document.getElementById("name").innerHTML = "Entirely AI Generated";
    }
    document.getElementById("result").style.display = "block";
    document.getElementById("anime-data").style.display = "block";
}


async function updateScore(wasRight) {
    currentScore = document.getElementById("current-score");
    currentScoreInt = parseInt(currentScore.innerHTML);
    if(wasRight) {
        currentScoreInt++;
    }
    else {
        currentScoreInt = 0;
    }
    maxScore = document.getElementById("max-score");
    maxScore.innerHTML = Math.max(parseInt(maxScore.innerHTML), currentScoreInt);
    currentScore.innerHTML = currentScoreInt;
}
