// ===== LESSON 2 JAVASCRIPT =====

// Initial code templates
const CODE_TEMPLATES = {
    square: `import turtle

# Zkus loop!
for i in range(4):
    turtle.forward(100)
    turtle.right(90)`,
    
    spiral: `import turtle
turtle.speed(0)  # super rychlá želva!

for i in range(100):
    turtle.forward(i * 2)
    turtle.right(91)`
};

// Load spiral example
function loadSpiralExample() {
    const editor = document.getElementById('python-editor');
    editor.value = CODE_TEMPLATES.spiral;
    document.getElementById('status').textContent = '✨ Spirála načtena! Klikni na Spustit kód';
}

// Show spiral preview video/image
function showSpiralVideo() {
    const preview = document.getElementById('spiral-preview');
    preview.style.display = preview.style.display === 'none' ? 'block' : 'none';
}

// Reset code to initial state
function resetCode() {
    const editor = document.getElementById('python-editor');
    editor.value = CODE_TEMPLATES.square;
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

// Run Python code
async function runPythonCode() {
    const code = document.getElementById('python-editor').value;
    const statusEl = document.getElementById('status');
    
    statusEl.textContent = '⏳ Spouštím...';
    
    try {
        const response = await fetch('/api/run-python', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });
        
        const result = await response.json();
        
        if (result.success) {
            statusEl.textContent = '✅ Hotovo!';
            drawTurtleOutput(result.commands);
            checkForSpiral(code);
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
    let angle = 0;
    
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.strokeStyle = '#3B82F6';
    ctx.lineWidth = 2;
    
    // Execute turtle commands
    commands.forEach((cmd, index) => {
        if (cmd.type === 'forward') {
            const radians = (angle * Math.PI) / 180;
            x += cmd.distance * Math.cos(radians);
            y += cmd.distance * Math.sin(radians);
            ctx.lineTo(x, y);
            
            // Cycle through colors for spiral effect
            if (commands.length > 50) {
                const hue = (index * 360 / commands.length) % 360;
                ctx.strokeStyle = `hsl(${hue}, 70%, 50%)`;
            }
        } else if (cmd.type === 'right') {
            angle += cmd.degrees;
        } else if (cmd.type === 'left') {
            angle -= cmd.degrees;
        }
    });
    
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Check if user created a spiral
function checkForSpiral(code) {
    const hasLoop = code.includes('for') && code.includes('range');
    const hasLargeRange = code.match(/range\((\d+)\)/);
    const rangeValue = hasLargeRange ? parseInt(hasLargeRange[1]) : 0;
    
    const hasForwardWithI = code.includes('i') && code.includes('forward');
    const hasSpiral = hasLoop && rangeValue >= 50 && hasForwardWithI;
    
    if (hasSpiral) {
        setTimeout(() => {
            document.getElementById('completion').style.display = 'block';
            document.getElementById('completion').scrollIntoView({ behavior: 'smooth' });
        }, 1500);
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
                lesson: 2,
                completed: true
            })
        });
        
        if (response.ok) {
            // Show achievement notification
            showAchievement('Loop Master', '🏆');
            
            setTimeout(() => {
                window.location.href = '/python-course/lesson-3';
            }, 2000);
        }
    } catch (error) {
        console.error('Error completing lesson:', error);
    }
}

// Show achievement notification
function showAchievement(name, icon) {
    const notification = document.createElement('div');
    notification.className = 'achievement-notification';
    notification.innerHTML = `
        <div class="achievement-content">
            <span class="achievement-icon">${icon}</span>
            <div>
                <div class="achievement-title">Odznák odemčen!</div>
                <div class="achievement-name">${name}</div>
            </div>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Lesson 2 loaded - Ready to create spirals!');
});

