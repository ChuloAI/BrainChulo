document.addEventListener('DOMContentLoaded', () => {
  const messagesContainer = parent.document.querySelector('.main');
  const observer = new MutationObserver(() => {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  });
  observer.observe(messagesContainer, { attributes: true, childList: true, subtree: true });
});