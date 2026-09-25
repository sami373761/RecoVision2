$('a[data-toggle="pill"]').on('shown.bs.tab', function (e) {
    if ($(e.target).attr('href') === '#content4') {
        console.log("Şifre Değiştir Sekmesi Yüklendi");
    }
});




(function() {
const slides = document.querySelectorAll('.myCarousel-slide');
const prevBtn = document.querySelector('.myCarousel-prev');
const nextBtn = document.querySelector('.myCarousel-next');
const indicators = document.querySelector('.myCarousel-indicators');

let currentIndex = 0;
const totalSlides = slides.length;

// Alttaki noktaları (dot) oluşturalım
for (let i = 0; i < totalSlides; i++) {
    const dot = document.createElement('div');
    dot.classList.add('myCarousel-dot');
    if (i === 0) dot.classList.add('myCarousel-active');
    
    dot.addEventListener('click', () => {
    currentIndex = i;
    updateCarousel();
    });
    indicators.appendChild(dot);
}

function updateCarousel() {
    slides.forEach((slide, index) => {
    let distance = index - currentIndex;
    
    // Orta (aktif) slayt
    if (distance === 0) {
        slide.style.transform = "translateX(0) translateZ(200px) scale(1)";
        slide.style.opacity = "1";
        slide.style.zIndex = "2";
    
    // Solundaki slayt
    } else if (distance === -1 || distance === (totalSlides - 1)) {
        slide.style.transform = "translateX(-150px) translateZ(0px) rotateY(15deg) scale(0.9)";
        slide.style.opacity = "0.5";
        slide.style.zIndex = "1";
    
    // Sağındaki slayt
    } else if (distance === 1 || distance === -(totalSlides - 1)) {
        slide.style.transform = "translateX(150px) translateZ(0px) rotateY(-15deg) scale(0.9)";
        slide.style.opacity = "0.5";
        slide.style.zIndex = "1";
    
    // Diğerleri arkada
    } else {
        slide.style.transform = "translateX(0) translateZ(-200px) scale(0.8)";
        slide.style.opacity = "0";
        slide.style.zIndex = "0";
    }
    });

    // Noktaları güncelle
    const dots = indicators.querySelectorAll('.myCarousel-dot');
    dots.forEach((dot, i) => {
    dot.classList.remove('myCarousel-active');
    if (i === currentIndex) {
        dot.classList.add('myCarousel-active');
    }
    });
}

// Buton olayları
prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    updateCarousel();
});

nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % totalSlides;
    updateCarousel();
});

updateCarousel();
})();




