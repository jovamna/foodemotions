// Lógica
// 1 - Selecionar elementos que devem ser animados
// 2 - Definir a classe que é adicionada durante a animação
// 3 - Criar função de animação
// 3.1 - Verificar a distância entre a barra de scroll e o topo do site
// 3.2 - Verificar se a distância do 3.1 + Offset é maior do que a distância entre o elemento e o Topo da Página.
// 3.3 - Se verdadeiro adicionar classe de animação, remover se for falso.
// 4 - Ativar a função de animação toda vez que o usuário utilizar o Scroll
// 5 - Otimizar ativação
// Debounce do Lodash
const debounce = function (func, wait, immediate) {
    let timeout;
    return function (...args) {
        const context = this;
        const later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};

const target = document.querySelectorAll('[data-anime]');
const animationClass = 'animate';

function animeScroll() {
    const windowTop = window.pageYOffset + ((window.innerHeight * 3) / 4);
    target.forEach(function (element) {
        if ((windowTop) > element.offsetTop) {
            element.classList.add(animationClass);
        } else {
            element.classList.remove(animationClass);
        }
    })
}

animeScroll();

if (target.length) {
    window.addEventListener('scroll', debounce(function () {
        animeScroll();
    }, 200));
}



// lógica
// 1 - Seleccionar elementos para animar
// 2 - Definir la clase que se agrega durante la animación
// 3 - Crear función de animación
// 3.1 - Verifique la distancia entre la barra de desplazamiento y la parte superior del sitio
// 3.2 - Verifique que la distancia de 3.1 + Offset sea mayor que la distancia entre el elemento y la parte superior de la página.
// 3.3 - Si es verdadero, agregue la clase de animación, elimine si es falso.
// 4 - Activa la función de animación cada vez que el usuario usa Scroll
// 5 - Optimizar la activación
// Lodash Debounce