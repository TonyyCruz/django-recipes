(() => {
  const form = document.querySelectorAll('.form-delete');
  const recipes = document.querySelectorAll('.recipe-name');

  if (form) {
    form.forEach((formField, id) => {
      formField.addEventListener('submit', (e) => {
        e.preventDefault();
        recipeName = recipes[id].innerHTML
        deleteText = `Do you really want to delete this recipe? ${recipeName}`;

        const confirmed = confirm(deleteText);

        if (confirmed) {
          formField.submit();
        }
      });
    });
  };
})();


(() => {
  const buttonCloseMenu = document.querySelector('.button-close-menu');
  const buttonShowMenu = document.querySelector('.button-show-menu');
  const menuContainer = document.querySelector('.menu-container');

  const buttonShowMenuVisibleClass = 'button-show-menu-visible';
  const menuHiddenClass = 'menu-hidden';
  const displayNoneClass = 'hidden-text';

  const showMenu = () => {
    buttonShowMenu.classList.remove(buttonShowMenuVisibleClass);
    buttonShowMenu.classList.add(displayNoneClass);
    menuContainer.classList.remove(menuHiddenClass);
  };

  const closeMenu = () => {
    buttonShowMenu.classList.add(buttonShowMenuVisibleClass);
    buttonShowMenu.classList.remove(displayNoneClass);
    menuContainer.classList.add(menuHiddenClass);
  };

  if (buttonShowMenu) {
    buttonShowMenu.removeEventListener('click', showMenu);
    buttonShowMenu.addEventListener('click', showMenu);
  };

  if (buttonCloseMenu) {
    buttonCloseMenu.removeEventListener('click', closeMenu);
    buttonCloseMenu.addEventListener('click', closeMenu);
  };
})();
