// ===== LESSON 1 JAVASCRIPT =====

// Toggle hint/solution
function toggleHint() {
    const solution = document.getElementById('solution');
    if (solution.style.display === 'none') {
        solution.style.display = 'block';
    } else {
        solution.style.display = 'none';
    }
}

// Reset code to initial state
function resetCode() {
    const editor = document.getElementById('python-editor');
    editor.value = `import turtle

# Tvůj kód sem:
turtle.forward(100)
turtle.right(90)`;
    clearOutput();
}

// Clear output
function clearOutput() {
    const canvas = document.getElementById('turtle-canvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    document.getElementById('console-output').textContent = '';
    document.getElementById('status').textContent = '';
}

// Run Python code (simplified - you'll need Pyodide or backend API)
async function runPythonCode() {
    const code = document.getElementById('python-editor').value;
    const statusEl = document.getElementById('status');
    
    statusEl.textContent = '⏳ Spouštím...';
    
    try {
        // OPTION 2: Pošli kód na backend API
        const response = await fetch('/api/run-python', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });
        
        const result = await response.json();
        
        if (result.success) {
            statusEl.textContent = '✅ Hotovo!';
            drawTurtleOutput(result.commands);
            checkForSquare(code);
        } else {
            statusEl.textContent = '❌ Chyba!';
            document.getElementById('console-output').textContent = result.error;
        }
        
    } catch (error) {
        statusEl.textContent = '❌ Chyba!';
        document.getElementById('console-output').textContent = error.message;
    }
}

// Draw turtle graphics on canvas
function drawTurtleOutput(commands) {
    const canvas = document.getElementById('turtle-canvas');
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Initial turtle position
    let x = canvas.width / 2;
    let y = canvas.height / 2;
    let angle = 0; // 0 = right, 90 = down, etc.
    
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.strokeStyle = '#3B82F6';
    ctx.lineWidth = 2;
    
    // Execute turtle commands
    commands.forEach(cmd => {
        if (cmd.type === 'forward') {
            const radians = (angle * Math.PI) / 180;
            x += cmd.distance * Math.cos(radians);
            y += cmd.distance * Math.sin(radians);
            ctx.lineTo(x, y);
        } else if (cmd.type === 'right') {
            angle += cmd.degrees;
        } else if (cmd.type === 'left') {
            angle -= cmd.degrees;
        }
    });
    
    ctx.stroke();
}

// Check if user drew a square (simple detection)
function checkForSquare(code) {
    const hasSquare = 
        (code.match(/forward\(100\)/g) || []).length >= 4 &&
        (code.match(/right\(90\)/g) || []).length >= 4;
    
    if (hasSquare) {
        // Show completion section
        setTimeout(() => {
            document.getElementById('completion').style.display = 'block';
            document.getElementById('completion').scrollIntoView({ behavior: 'smooth' });
        }, 1000);
    }
}

// Complete lesson and save progress
async function completeLesson() {
    try {
        const response = await fetch('/api/complete-lesson', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                course: 'python',
                lesson: 1,
                completed: true
            })
        });
        
        if (response.ok) {
            alert('🎉 Lekce dokončena! Můžeš pokračovat dál.');
            window.location.href = '/python-course/lesson-2';
        }
    } catch (error) {
        console.error('Error completing lesson:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Lesson 1 loaded');
});

