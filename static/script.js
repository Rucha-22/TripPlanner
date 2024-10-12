const images = [
    'url(static/assets/mumbai.jpg)',
    'url(static/assets/delhi.webp)',
    'url(static/assets/hyderabad.jpg)',
    'url(static/assets/Sultan_Tipu_Palace.jpg)',
   'url(static/assets/howrabridge.avif)',
   "url(static/assets/marinabeach.jpg)"
];
const place=["Marine Drive", "Rajpath","Charminar","Tipu Sultan Palace","Howrah Bridge","Marina Beach"]
const locations = ["Mumbai,India","Delhi,India","Hydrabad,India","Banglore,India","Kolkata,India","Chennai,India"];

let currentIndex = 0;
const backgroundContainer = document.querySelector('.background-container');
const loc = document.querySelector('.city-name');
const placename =document.querySelector('#placename');

function changeBackgroundImage() {
    currentIndex = (currentIndex + 1) % images.length;
    backgroundContainer.style.backgroundImage = images[currentIndex];
    loc.innerText = locations[currentIndex];
    placename.innerText = place[currentIndex];
}

setInterval(changeBackgroundImage, 5000); // Change every 5 seconds

// Set the initial background image
backgroundContainer.style.backgroundImage = images[currentIndex];
