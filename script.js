// ===== PREMIUM ANIMATIONS JS =====

const buttons = document.querySelectorAll('.btn.glass');

// ===== CURSOR TRAIL =====
document.addEventListener('mousemove', e => {
    const trail = document.createElement('span');
    trail.className = 'cursorTrail';
    trail.style.left = e.clientX + 'px';
    trail.style.top = e.clientY + 'px';
    document.body.appendChild(trail);
    setTimeout(() => trail.remove(), 500);
});

// ===== FLOATING BACKGROUND SPARKLES =====
for(let i=0;i<20;i++){
    const sparkle = document.createElement('div');
    sparkle.className = 'floatingSparkle';
    sparkle.style.left = Math.random()*window.innerWidth + 'px';
    sparkle.style.top = Math.random()*window.innerHeight + 'px';
    sparkle.style.width = sparkle.style.height = (Math.random()*4 + 2) + 'px';
    sparkle.style.opacity = Math.random()*0.5 + 0.2;
    document.body.appendChild(sparkle);
}

// ===== BUTTON EFFECTS =====
buttons.forEach(btn => {

    // Magnetic hover
    btn.addEventListener('mousemove', e => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x*0.15}px, ${y*0.15}px) scale(1.08) rotateZ(1deg)`;
        btn.style.boxShadow = `0 0 30px rgba(255,200,120,0.8), ${x*0.5}px ${y*0.5}px 40px rgba(255,255,255,0.2)`;
    });

    btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'translate(0,0) scale(1) rotateZ(0deg)';
        btn.style.boxShadow = '0 0 30px rgba(255,200,120,0.8)';
    });

    // Click particles + confetti
    btn.addEventListener('click', e => {
        for(let i=0;i<12;i++){
            const particle = document.createElement('span');
            particle.className = 'clickParticle confettiPiece';
            particle.style.left = e.clientX + 'px';
            particle.style.top = e.clientY + 'px';
            particle.style.setProperty('--dx', (Math.random()*100-50)+'px');
            particle.style.setProperty('--dy', (Math.random()*100-50)+'px');
            particle.style.background = `hsl(${Math.random()*50+30}, 100%, 50%)`;
            document.body.appendChild(particle);
            setTimeout(() => particle.remove(), 600);
        }
    });

    // Micro floating particles on hover
    btn.addEventListener('mouseenter', () => {
        for(let i=0;i<5;i++){
            const micro = document.createElement('span');
            micro.className = 'microParticle';
            const rect = btn.getBoundingClientRect();
            micro.style.left = rect.left + Math.random()*rect.width + 'px';
            micro.style.top = rect.top + Math.random()*rect.height + 'px';
            document.body.appendChild(micro);
            setTimeout(()=>micro.remove(), 1000);
        }
    });

});
 // Add floating particles dynamically on all pages
for(let i=0;i<30;i++){
    const fp = document.createElement('div');
    fp.className = 'floatingParticle';
    fp.style.left = Math.random()*window.innerWidth + 'px';
    fp.style.top = Math.random()*window.innerHeight + 'px';
    fp.style.width = fp.style.height = (Math.random()*4+2) + 'px';
    document.body.appendChild(fp);
}
pill.addEventListener('click', () => {
    pills.forEach(p => p.classList.remove('active'));
    pill.classList.add('active');
    selectedSubject = pill.dataset.sub;

    // ✅ ADD THIS LINE TO SEND SUBJECT TO SERVER
    document.getElementById('subject-input').value = selectedSubject;
});
pill.addEventListener('click', () => {
    pills.forEach(p => p.classList.remove('active'));
    pill.classList.add('active');
    selectedSubject = pill.dataset.sub;

    document.getElementById('subject-input').value = selectedSubject;
});
