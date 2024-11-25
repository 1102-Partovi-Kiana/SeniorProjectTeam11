tippy('#coding-pets', {
    content: "Enable Coding Pets",
    animation: 'fade',
    onShow(instance) {
      const tooltip = instance.popper.querySelector('.tippy-box');
      if (tooltip) {
        tooltip.classList.add('animate__animated', 'animate__rubberBand');
      }
    },
    onHidden(instance) {
      const tooltip = instance.popper.querySelector('.tippy-box');
      if (tooltip) {
        tooltip.classList.remove('animate__animated', 'animate__rubberBand');
      }
    },
  });
  
tippy('#light-mode', {
    content: "Switch to Light Mode",
    animation: 'fade',
    onShow(instance) {
      const tooltip = instance.popper.querySelector('.tippy-box');
      if (tooltip) {
        tooltip.classList.add('animate__animated', 'animate__tada');
      }
    },
    onHidden(instance) {
      const tooltip = instance.popper.querySelector('.tippy-box');
      if (tooltip) {
        tooltip.classList.remove('animate__animated', 'animate__tada');
      }
    },
  });
  
tippy('#syntax-highlight', {
    content: "Toggle Syntax Highlighting",
    animation: 'fade',
    onShow(instance) {
      const tooltip = instance.popper.querySelector('.tippy-box');
      if (tooltip) {
        tooltip.classList.add('animate__animated', 'animate__bounce');
      }
    },
    onHidden(instance) {
      const tooltip = instance.popper.querySelector('.tippy-box');
      if (tooltip) {
        tooltip.classList.remove('animate__animated', 'animate__bounce');
      }
    },
  });
  
tippy('#autocomplete', {
    content: "Enable Autocomplete",
    animation: 'fade',
    onShow(instance) {
      const tooltip = instance.popper.querySelector('.tippy-box');
      if (tooltip) {
        tooltip.classList.add('animate__animated', 'animate__tada');
      }
    },
    onHidden(instance) {
      const tooltip = instance.popper.querySelector('.tippy-box');
      if (tooltip) {
        tooltip.classList.remove('animate__animated', 'animate__tada');
      }
    },
  });
  
tippy('#hints-button', {
    content: "Show Hints",
    animation: 'fade',
    onShow(instance) {
        const tooltip = instance.popper.querySelector('.tippy-box');
        if (tooltip) {
            tooltip.classList.add('animate__animated', 'animate__jello');
        }
    },
    onHidden(instance) {
        const tooltip = instance.popper.querySelector('.tippy-box');
        if (tooltip) {
            tooltip.classList.remove('animate__animated', 'animate__jello');
        }
    },
});