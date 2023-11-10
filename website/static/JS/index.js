import { slideToggle, slideUp, slideDown } from './slide.js';
import {
  ANIMATION_DURATION,
  FIRST_SUB_MENUS_BTN,
  INNER_SUB_MENUS_BTN,
  SIDEBAR_EL,
} from './constants.js';
import  Poppers from './poppers.js';

const PoppersInstance = new Poppers();

/**
 * wait for the current animation to finish and update poppers position
 */
// const updatePoppersTimeout = () => {
//   if (typeof PoppersInstance.updatePoppers === 'function') {
//     setTimeout(() => {
//       PoppersInstance.updatePoppers();
//     }, ANIMATION_DURATION);
//   } else {
//     console.error('PoppersInstance does not have an updatePoppers method.');
//   }
// };
/**
 * sidebar collapse handler
 */
document.getElementById('btn-collapse').addEventListener('click', () => {
  SIDEBAR_EL.classList.toggle('collapsed');
  // PoppersInstance.closePoppers(); 
  if (SIDEBAR_EL.classList.contains('collapsed'))
    FIRST_SUB_MENUS_BTN.forEach((element) => {
      element.parentElement.classList.remove('open');
    });

  // updatePoppersTimeout();
});

/**
 * sidebar toggle handler (on break point )
 */
document.getElementById('btn-toggle').addEventListener('click', () => {
  SIDEBAR_EL.classList.toggle('toggled');

  // updatePoppersTimeout();
});

/**
 * toggle sidebar on overlay click
 */
document.getElementById('overlay').addEventListener('click', () => {
  SIDEBAR_EL.classList.toggle('toggled');
});

const defaultOpenMenus = document.querySelectorAll('.menu-item.sub-menu.open');

defaultOpenMenus.forEach((element) => {
  element.lastElementChild.style.display = 'block';
});

/**
 * handle top level submenu click
 */
FIRST_SUB_MENUS_BTN.forEach((element) => {
  element.addEventListener('click', () => {
    if (SIDEBAR_EL.classList.contains('collapsed'))
      PoppersInstance.togglePopper(element.nextElementSibling);
    else {
      /**
       * if menu has "open-current-only" class then only one submenu opens at a time
       */
      const parentMenu = element.closest('.menu.open-current-submenu');
      if (parentMenu)
        parentMenu
          .querySelectorAll(':scope > ul > .menu-item.sub-menu > a')
          .forEach(
            (el) =>
              window.getComputedStyle(el.nextElementSibling).display !==
                'none' && slideUp(el.nextElementSibling)
          );
      slideToggle(element.nextElementSibling);
    }
  });
});

/**
 * handle inner submenu click
 */
INNER_SUB_MENUS_BTN.forEach((element) => {
  element.addEventListener('click', () => {
    slideToggle(element.nextElementSibling);
  });
});


    function hideFlashMessage() {
        setTimeout(function () {
            $('.alert').fadeOut('slow', function () {
                $(this).remove();
            });
        }, 3000); // Adjust the timeout as needed (3 seconds = 3000 milliseconds)
    }

    // Call the hideFlashMessage function when the page loads
    $(document).ready(function () {
        hideFlashMessage();
    });







    function toggleLanguageElements() {
        const selectedLang = localStorage.getItem("lang") || "en"; // Default to English

        // Select the elements for "Department Name" in English and other languages
        const lang1Elements = document.querySelectorAll('.lang1');
        const lang2Elements = document.querySelectorAll('.lang2');

        if (selectedLang === "en") {
            lang1Elements.forEach(element => element.style.display = "table-cell");
            lang2Elements.forEach(element => element.style.display = "none");
            
        } else {
            lang1Elements.forEach(element => element.style.display = "none");
            lang2Elements.forEach(element => element.style.display = "table-cell");
        }
    }

    // Listen for language change and toggle elements when the page loads
    document.addEventListener("DOMContentLoaded", toggleLanguageElements);
    document.addEventListener("changeLanguage", toggleLanguageElements);

    // Trigger the language toggle on initial page load
    toggleLanguageElements();

