// Předlekce - Animovaná želva Terry s typewriter efektem

class TypewriterEffect {
    constructor(targetElement, contentElement, options = {}) {
        this.targetElement = targetElement;
        this.contentElement = contentElement;
        this.options = {
            charDelay: options.charDelay || 30,      // Delay mezi znaky (ms)
            paragraphDelay: options.paragraphDelay || 500, // Delay mezi odstavci (ms)
            onComplete: options.onComplete || null
        };
        
        this.isSkipped = false;
        this.isPaused = false;
        this.currentIndex = 0;
        this.elements = [];
    }
    
    async start() {
        // Získat všechny elementy z hidden contentu
        this.elements = Array.from(this.contentElement.children);
        
        // Vymazat cílový element
        this.targetElement.innerHTML = '';
        
        // Postupně vypisovat každý element
        for (let i = 0; i < this.elements.length; i++) {
            if (this.isSkipped) {
                this.showAllRemaining(i);
                break;
            }
            
            await this.typeElement(this.elements[i]);
            
            // Delay mezi odstavci
            if (i < this.elements.length - 1) {
                await this.delay(this.options.paragraphDelay);
            }
        }
        
        // Callback po dokončení
        if (this.options.onComplete) {
            this.options.onComplete();
        }
    }
    
    async typeElement(element) {
        const clone = element.cloneNode(true);
        
        // Pokud je to HR, jen ho přidáme
        if (element.tagName === 'HR') {
            this.targetElement.appendChild(clone);
            await this.delay(this.options.paragraphDelay);
            return;
        }
        
        // Pro textové elementy - nejdřív zobrazíme prázdnou bublinu s borderem
        const text = clone.textContent;
        clone.textContent = '';
        this.targetElement.appendChild(clone);
        
        // Krátká pauza, aby se bublina zobrazila
        await this.delay(300);
        
        // Pak postupně přidávat znaky
        for (let char of text) {
            // Čekáme, pokud je pauza
            while (this.isPaused && !this.isSkipped) {
                await this.delay(100);
            }
            
            if (this.isSkipped) {
                clone.textContent = text;
                break;
            }
            
            clone.textContent += char;
            await this.delay(this.options.charDelay);
        }
    }
    
    pause() {
        this.isPaused = true;
    }
    
    resume() {
        this.isPaused = false;
    }
    
    showAllRemaining(fromIndex) {
        // Zobrazit všechny zbývající elementy najednou
        for (let i = fromIndex; i < this.elements.length; i++) {
            const clone = this.elements[i].cloneNode(true);
            this.targetElement.appendChild(clone);
        }
    }
    
    skip() {
        this.isSkipped = true;
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Inicializace po načtení stránky
document.addEventListener('DOMContentLoaded', () => {
    const targetElement = document.getElementById('typewriter-text');
    const contentElement = document.getElementById('text-content');
    const pauseBtn = document.getElementById('pauseBtn');
    const skipBtn = document.getElementById('skipBtn');
    const continueBtn = document.getElementById('continueBtn');
    
    let isPaused = false;
    
    // Vytvořit typewriter instanci
    const typewriter = new TypewriterEffect(targetElement, contentElement, {
        charDelay: 30,
        paragraphDelay: 300,
        onComplete: () => {
            // Po dokončení zobrazit tlačítko "Pokračovat"
            pauseBtn.style.display = 'none';
            skipBtn.style.display = 'none';
            continueBtn.style.display = 'block';
        }
    });
    
    // Spustit typewriter efekt
    typewriter.start();
    
    // Tlačítko "Pauza/Spustit"
    pauseBtn.addEventListener('click', () => {
        if (isPaused) {
            typewriter.resume();
            pauseBtn.innerHTML = '<i class="fas fa-pause"></i> Pauza';
            isPaused = false;
        } else {
            typewriter.pause();
            pauseBtn.innerHTML = '<i class="fas fa-play"></i> Spustit';
            isPaused = true;
        }
    });
    
    // Tlačítko "Přeskočit"
    skipBtn.addEventListener('click', () => {
        typewriter.skip();
        pauseBtn.style.display = 'none';
        skipBtn.style.display = 'none';
        continueBtn.style.display = 'block';
    });
    
    // Tlačítko "Pokračovat" - přejde na první lekci
    continueBtn.addEventListener('click', () => {
        window.location.href = '/lekce/python/1';
    });
    
    // Animace želvy - přidat speciální efekty
    const terrySvg = document.querySelector('.terry-svg');
    const terryHead = document.querySelector('.terry-head');
    
    // Občas zamávat hlavou více
    setInterval(() => {
        if (Math.random() > 0.7) {
            terryHead.style.animation = 'nod 0.5s ease-in-out 3';
            setTimeout(() => {
                terryHead.style.animation = 'nod 2s ease-in-out infinite';
            }, 1500);
        }
    }, 5000);
    
    // Easter egg - kliknutí na želvu (jen rotace)
    let clickCount = 0;
    terrySvg.addEventListener('click', () => {
        clickCount++;
        
        // Rotace želvy
        terrySvg.style.transform = `rotate(${clickCount * 15}deg)`;
        setTimeout(() => {
            terrySvg.style.transform = 'rotate(0deg)';
        }, 500);
        
        // Reset po 10 kliknutích
        if (clickCount >= 10) {
            clickCount = 0;
        }
    });
});

