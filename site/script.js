// Находим панель и переменные состояния
const sidebar = document.querySelector('.sidebar');
let inside = false;

/*
Следим за движением мыши.
Если курсор ближе к левому краю — показываем меню.
Если уходит далеко и мышь не над панелью — прячем.
*/
document.addEventListener('mousemove', (e) => {
    if (e.clientX < 20) sidebar.classList.add('show');
    else if (e.clientX > sidebar.offsetWidth + 20 && !inside)
        sidebar.classList.remove('show');
});

// Фиксируем наведение на панель
sidebar.addEventListener('mouseenter', () => inside = true);
sidebar.addEventListener('mouseleave', () => { inside = false; sidebar.classList.remove('show'); });

const pages = {
    home: "<h1>Главная</h1><p>Добро пожаловать на главную страницу!</p>",
    feed: "<h1>Лента</h1><p>Здесь отображается ваша лента новостей.</p>",
    chats: "<h1>Чаты</h1><p>Ваши сообщения и чаты будут здесь.</p>",
    profile: "<h1>Профиль</h1><p>Просмотрите и отредактируйте свой профиль.</p>"
}

const content = document.getElementById("content");
document.querySelectorAll(".sidebar button").forEach(btn => {
    btn.addEventListener("click", () => {
        const page = btn.dataset.page;
        content.innerHTML = pages[page];
    });
});