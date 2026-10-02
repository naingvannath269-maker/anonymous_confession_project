document.addEventListener('DOMContentLoaded', function () {
  const simpleTrigger = document.getElementById('simple-trigger');
  const expandedComposer = document.getElementById('expanded-composer');
  const textarea = document.getElementById('confession-content');
  const submitPanel = document.getElementById('submit-whisper');

  if (simpleTrigger && expandedComposer && textarea) {

    // 1. Click the simple view -> show the form
    simpleTrigger.addEventListener('click', function () {
      simpleTrigger.style.display = 'none';
      expandedComposer.style.display = 'block';
      textarea.focus();
    });

    // 2. Click away from textarea -> hide form if empty
    textarea.addEventListener('blur', function () {
      setTimeout(() => {
        if (textarea.value.trim() === "") {
          expandedComposer.style.display = 'none';
          simpleTrigger.style.display = 'flex';
        }
      }, 200);
    });

    // 3. Click outside the whole panel -> hide form if empty
    document.addEventListener('click', function (event) {
      if (!submitPanel.contains(event.target) && textarea.value.trim() === "") {
        expandedComposer.style.display = 'none';
        simpleTrigger.style.display = 'flex';
      }
    });
  }
});