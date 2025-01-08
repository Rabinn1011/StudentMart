var swiper = new Swiper(".mySwiper", {
    spaceBetween: 30,
    centeredSlides: true,
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

//dropdown menu on clivk action

const profileIcon = document.getElementById('profile-icon');
const dropdownMenu = document.getElementById('dropdown-menu');

// Toggle the dropdown menu on click
profileIcon.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default anchor behavior
    e.stopPropagation(); // Prevent event from bubbling up
    dropdownMenu.style.display =
        dropdownMenu.style.display === 'block' ? 'none' : 'block';
});

// Hide the dropdown menu when clicking outside
document.addEventListener('click', () => {
    dropdownMenu.style.display = 'none';
});
