document.addEventListener('DOMContentLoaded', () => {
    const flashcards = [];
    const flashcardContainer = document.getElementById('flashcard-container');
    const questionElement = document.getElementById('question');
    const answerElement = document.getElementById('answer');
    const toggleAnswerButton = document.getElementById('toggle-answer');
    const prevCardButton = document.getElementById('prev-card');
    const nextCardButton = document.getElementById('next-card');
    let currentCardIndex = 0;

    fetch('sample.txt')
        .then(response => response.text())
        .then(data => {
            const lines = data.split(';');
            lines.forEach(line => {
                const [question, answer] = line.split(',');
                if (question && answer) {
                    flashcards.push({ question: question.trim(), answer: answer.trim() });
                }
            });
            displayFlashcard();
        });

    function displayFlashcard() {
        const flashcard = flashcards[currentCardIndex];
        questionElement.textContent = flashcard.question;
        answerElement.textContent = flashcard.answer;
        answerElement.style.display = 'none';
        toggleAnswerButton.textContent = 'Show Answer';
    }

    toggleAnswerButton.addEventListener('click', () => {
        if (answerElement.style.display === 'none') {
            answerElement.style.display = 'block';
            toggleAnswerButton.textContent = 'Hide Answer';
        } else {
            answerElement.style.display = 'none';
            toggleAnswerButton.textContent = 'Show Answer';
        }
    });

    prevCardButton.addEventListener('click', () => {
        if (currentCardIndex > 0) {
            currentCardIndex--;
            displayFlashcard();
        }
    });

    nextCardButton.addEventListener('click', () => {
        if (currentCardIndex < flashcards.length - 1) {
            currentCardIndex++;
            displayFlashcard();
        }
    });
});