function myScope() {
  const form = document.querySelectorAll(".form-delete");
  const recipes = document.querySelectorAll(".recipe-name");

  if (form) {
    form.forEach((formField, id) => {
      formField.addEventListener("submit", (e) => {
        e.preventDefault();
        recipeName = recipes[id].innerHTML
        deleteText = `Do you really want to delete this recipe? ${recipeName}`;

        const confirmed = confirm(deleteText)

        if (confirmed) {
          formField.submit();
        }
      });
    });
  };
};

myScope();