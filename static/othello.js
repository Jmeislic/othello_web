const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");
const SIZE = 8;
const CELL = canvas.width / SIZE;

let board = {};             // Current board state
let currentPlayer = "black"; // Track whose turn it is
let blackPlayer = "human";   // Selected player types
let whitePlayer = "computer";

// Draw the 8x8 grid
function drawGrid() {
    ctx.strokeStyle = "black";
    for (let i = 0; i <= SIZE; i++) {
        // Vertical lines
        ctx.beginPath();
        ctx.moveTo(i * CELL, 0);
        ctx.lineTo(i * CELL, canvas.height);
        ctx.stroke();

        // Horizontal lines
        ctx.beginPath();
        ctx.moveTo(0, i * CELL);
        ctx.lineTo(canvas.width, i * CELL);
        ctx.stroke();
    }
}

// Draw pieces on the board
function drawBoard(b) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawGrid();
    for (const key in b) {
        const [r, c] = key.split(",").map(Number);
        const color = b[key]; // "black" or "white"

        const x = c * CELL + CELL / 2;
        const y = r * CELL + CELL / 2;
        const radius = CELL / 2 - 4;

        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.stroke();
    }
}

// Announce winner
function announceWinner(winner) {
    alert(winner);
}

// Refresh board from backend
function refresh() {
    fetch("/board")
        .then(res => res.json())
        .then(data => {
            board = data;
            drawBoard(board);
        })
        .catch(console.error);
}

// Start game with selected players
document.getElementById("startBtn").onclick = () => {
    blackPlayer = document.getElementById("blackPlayer").value;
    whitePlayer = document.getElementById("whitePlayer").value;

    fetch("/start_game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ blackPlayer, whitePlayer })
    })
    .then(res => res.json())
    .then(data => {
        board = data.board;
        currentPlayer = "black";
        drawBoard(board);
        maybeAutoMove(); // if black is AI/computer/random
    })
    .catch(console.error);
};

// Reset game
document.getElementById("resetBtn").onclick = () => {
    fetch("/reset_game", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            board = data.board;
            currentPlayer = "black";
            drawBoard(board);
            maybeAutoMove();
        })
        .catch(console.error);
};

// Handle human click moves
canvas.addEventListener("click", e => {
    const rect = canvas.getBoundingClientRect();
    const col = Math.floor((e.clientX - rect.left) / CELL);
    const row = Math.floor((e.clientY - rect.top) / CELL);

    // Only allow human moves on their turn
    const playerType = currentPlayer === "black" ? blackPlayer : whitePlayer;
    if (playerType !== "human") return;

    fetch("/human_move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ row, col })
    })
    .then(res => res.json())
    .then(data => {
        board = data.board;
        drawBoard(board);

        if (data.end) {
            announceWinner(data.whowon);
            return;
        }

        // Switch turn
        currentPlayer = currentPlayer === "black" ? "white" : "black";
        maybeAutoMove();
    })
    .catch(console.error);
});

// Automatically make a move if current player is AI/Computer/Random
function maybeAutoMove() {
    const playerType = currentPlayer === "black" ? blackPlayer : whitePlayer;
    if (playerType === "human") return;

    setTimeout(() => {
        fetch("/human_move", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ row: -1, col: -1 }) })
            .then(res => res.json())
            .then(data => {
                board = data.board;
                drawBoard(board);

                if (data.end) {
                    announceWinner(data.whowon);
                    return;
                }

                currentPlayer = currentPlayer === "black" ? "white" : "black";
                maybeAutoMove();
            })
            .catch(console.error);
    }, 500); // delay for effect
}

// Initial board draw
refresh();
