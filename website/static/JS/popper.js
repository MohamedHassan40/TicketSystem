import * as createPopper  from 'https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js';
import { SIDEBAR_EL } from './constants.js';

class Popper {
  instance = null;
  reference = null;
  popperTarget = null;

  constructor(reference, popperTarget) {
    this.init(reference, popperTarget);
  }

  init(reference, popperTarget) {
    this.reference = reference;
    this.popperTarget = popperTarget;
    this.instance = createPopper(this.reference, this.popperTarget, {
      placement: 'right',
      strategy: 'fixed',
      resize: true,
      modifiers: [
        {
          name: 'computeStyles',
          options: {
            adaptive: false,
          },
        },
        {
          name: 'flip',
          options: {
            fallbackPlacements: ['left', 'right'],
          },
        },
      ],
    });

    document.addEventListener(
      'click',
      (e) => this.clicker(e, this.popperTarget, this.reference),
      false,
    );

    const ro = new ResizeObserver(() => {
      this.instance.update();
    });

    ro.observe(this.popperTarget);
    ro.observe(this.reference);
  }

  clicker(event, popperTarget, reference) {
    if (
      SIDEBAR_EL.classList.contains('collapsed') &&
      !popperTarget.contains(event.target) &&
      !reference.contains(event.target)
    ) {
      this.hide();
    }
  }

  hide() {
    this.instance.state.elements.popper.style.visibility = 'hidden';
  }
}

export default Popper;