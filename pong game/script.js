document.addEventListener('DOMContentLoaded', () => {
    // Canvas setup
    const canvas = document.getElementById('pong-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 600;
    canvas.height = 400;
    
    // Game elements
    const paddleWidth = 10;
    const paddleHeight = 70;
    const ballSize = 10;
    
    // Game state
    let playerScore = 0;
    let computerScore = 0;
    let gameSpeed = 5;
    
    // Player paddle
    const playerPaddle = {
        x: 20,
        y: canvas.height / 2 - paddleHeight / 2,
        width: paddleWidth,
        height: paddleHeight,
        dy: 7
    };
    
    // Computer paddle
    const computerPaddle = {
        x: canvas.width - 20 - paddleWidth,
        y: canvas.height / 2 - paddleHeight / 2,
        width: paddleWidth,
        height: paddleHeight,
        dy: 5
    };
    
    // Ball
    const ball = {
        x: canvas.width / 2,
        y: canvas.height / 2,
        width: ballSize,
        height: ballSize,
        dx: gameSpeed,
        dy: gameSpeed
    };
    
    // Keyboard control for player paddle
    const keys = {
        ArrowUp: false,
        ArrowDown: false
    };
    
    // Event listeners
    document.addEventListener('keydown', e => {
        if (e.key in keys) {
            keys[e.key] = true;
        }
    });
    
    document.addEventListener('keyup', e => {
        if (e.key in keys) {
            keys[e.key] = false;
        }
    });
    
    // Mouse control for player paddle
    canvas.addEventListener('mousemove', e => {
        const canvasRect = canvas.getBoundingClientRect();
        const mouseY = e.clientY - canvasRect.top;
        playerPaddle.y = mouseY - (paddleHeight / 2);
        
        // Keep paddle within canvas boundaries
        if (playerPaddle.y < 0) {
            playerPaddle.y = 0;
        } else if (playerPaddle.y + paddleHeight > canvas.height) {
            playerPaddle.y = canvas.height - paddleHeight;
        }
    });
    
    // Draw functions
    function drawPaddle(x, y, width, height) {
        ctx.fillStyle = 'white';
        ctx.fillRect(x, y, width, height);
    }
    
    function drawBall(x, y, width, height) {
        ctx.fillStyle = 'white';
        ctx.fillRect(x, y, width, height);
    }
    
    function drawDottedLine() {
        ctx.beginPath();
        ctx.setLineDash([5, 15]);
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.strokeStyle = 'white';
        ctx.stroke();
        ctx.setLineDash([]);
    }
    
    // Update score display
    function updateScores() {
        document.getElementById('player-score').textContent = playerScore;
        document.getElementById('computer-score').textContent = computerScore;
    }
    
    // Check for collisions
    function checkCollision() {
        // Ball collision with top and bottom walls
        if (ball.y <= 0 || ball.y + ball.height >= canvas.height) {
            ball.dy *= -1;
        }
        
        // Ball collision with player paddle
        if (
            ball.x <= playerPaddle.x + playerPaddle.width &&
            ball.y + ball.height >= playerPaddle.y &&
            ball.y <= playerPaddle.y + playerPaddle.height
        ) {
            ball.dx *= -1;
            
            // Adjust ball angle based on where it hits the paddle
            const hitPosition = (ball.y - playerPaddle.y) / playerPaddle.height;
            ball.dy = 6 * (hitPosition - 0.5); // Value between -3 and 3
        }
        
        // Ball collision with computer paddle
        if (
            ball.x + ball.width >= computerPaddle.x &&
            ball.y + ball.height >= computerPaddle.y &&
            ball.y <= computerPaddle.y + computerPaddle.height
        ) {
            ball.dx *= -1;
            
            // Adjust ball angle based on where it hits the paddle
            const hitPosition = (ball.y - computerPaddle.y) / computerPaddle.height;
            ball.dy = 6 * (hitPosition - 0.5); // Value between -3 and 3
        }
        
        // Ball out of bounds (scoring)
        if (ball.x < 0) {
            // Computer scores
            computerScore++;
            updateScores();
            resetBall();
        } else if (ball.x > canvas.width) {
            // Player scores
            playerScore++;
            updateScores();
            resetBall();
        }
    }
    
    // Reset ball to center
    function resetBall() {
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        ball.dx = -ball.dx;
        ball.dy = Math.random() * 6 - 3; // Random direction between -3 and 3
    }
    
    // Update game state
    function update() {
        // Player paddle movement with keyboard
        if (keys.ArrowUp && playerPaddle.y > 0) {
            playerPaddle.y -= playerPaddle.dy;
        } else if (keys.ArrowDown && playerPaddle.y + paddleHeight < canvas.height) {
            playerPaddle.y += playerPaddle.dy;
        }
        
        // Computer AI to follow the ball
        const computerPaddleCenter = computerPaddle.y + computerPaddle.height / 2;
        const ballCenter = ball.y + ball.height / 2;
        
        // Add some delay to make the computer beatable
        if (computerPaddleCenter < ballCenter - 10) {
            computerPaddle.y += computerPaddle.dy;
        } else if (computerPaddleCenter > ballCenter + 10) {
            computerPaddle.y -= computerPaddle.dy;
        }
        
        // Make sure computer paddle stays within boundaries
        if (computerPaddle.y < 0) {
            computerPaddle.y = 0;
        } else if (computerPaddle.y + paddleHeight > canvas.height) {
            computerPaddle.y = canvas.height - paddleHeight;
        }
        
        // Ball movement
        ball.x += ball.dx;
        ball.y += ball.dy;
        
        // Check collisions
        checkCollision();
    }
    
    // Render game
    function render() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw dotted line in middle
        drawDottedLine();
        
        // Draw paddles
        drawPaddle(playerPaddle.x, playerPaddle.y, playerPaddle.width, playerPaddle.height);
        drawPaddle(computerPaddle.x, computerPaddle.y, computerPaddle.width, computerPaddle.height);
        
        // Draw ball
        drawBall(ball.x, ball.y, ball.width, ball.height);
    }
    
    // Game loop
    function gameLoop() {
        update();
        render();
        requestAnimationFrame(gameLoop);
    }
    
    // Start the game
    updateScores();
    gameLoop();
});